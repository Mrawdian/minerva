"""Tests de src/pipeline.py — bilingue natif : la paire EN+FR à travers
NEW / MODIFIED / BOOTSTRAP / SKIPPED_EMPTY, sans réseau ni LLM (tout mocké)."""

from pathlib import Path

import pipeline
import translator


REPO = {
    "full_name": "rtthread/rt-thread",
    "description": "RTOS for IoT devices",
    "language": "C",
    "pushed_at": "2026-06-01T00:00:00+00:00",
    "stargazers_count": 5000,
    "forks_count": 2000,
    "default_branch": "master",
}
SCORE = {
    "repo_full_name": "rtthread/rt-thread",
    "score_total": 90,
    "scores_par_domaine": {"Embarqué": 80, "IoT": 40, "Edge AI": 10},
    "domaine_principal": "Embarqué",
    "mots_cles_matches": ["rtos"],
    "best_similarity": 0.8,
}

FICHE_EN = "---\n## rtthread/rt-thread\n**Type:** RTOS\n---\n"
FICHE_FR = "---\n## rtthread/rt-thread\n**Type :** RTOS\n---\n"


def _patch_dirs(monkeypatch, tmp_path: Path) -> tuple[Path, Path]:
    en_dir = tmp_path / "fiches"
    fr_dir = tmp_path / "fiches_fr"
    monkeypatch.setattr(pipeline, "FICHES_DIR", en_dir)
    monkeypatch.setattr(pipeline, "FICHES_FR_DIR", fr_dir)
    return en_dir, fr_dir


def _patch_io(monkeypatch, pair=(FICHE_EN, FICHE_FR)):
    monkeypatch.setattr(pipeline.fetcher, "fetch_readme",
                        lambda owner, repo, branch="master": "# readme")
    monkeypatch.setattr(pipeline.translator, "generate_fiche_pair",
                        lambda repo, readme, score_info: pair)


# ─── _process_llm : la paire est écrite ──────────────────────────────────────

def test_process_llm_new_writes_both_languages(monkeypatch, tmp_path):
    en_dir, fr_dir = _patch_dirs(monkeypatch, tmp_path)
    _patch_io(monkeypatch)

    res = pipeline._process_llm(SCORE, REPO, "NEW", REPO["pushed_at"], None,
                                dry_run=False)

    assert res["status"] == "NEW"
    en_file = en_dir / "rtthread_rt-thread_fiche.md"
    fr_file = fr_dir / "rtthread_rt-thread_fiche.md"
    assert en_file.is_file() and fr_file.is_file()
    assert "**Type:** RTOS" in en_file.read_text(encoding="utf-8")
    assert "**Type :** RTOS" in fr_file.read_text(encoding="utf-8")


def test_process_llm_modified_badges_both_languages(monkeypatch, tmp_path):
    en_dir, fr_dir = _patch_dirs(monkeypatch, tmp_path)
    _patch_io(monkeypatch)

    res = pipeline._process_llm(SCORE, REPO, "MODIFIED", REPO["pushed_at"],
                                "2026-01-01T00:00:00+00:00", dry_run=False)

    assert res["status"] == "MODIFIED"
    for d in (en_dir, fr_dir):
        text = (d / "rtthread_rt-thread_fiche.md").read_text(encoding="utf-8")
        assert "## rtthread/rt-thread [MODIFIÉ]" in text


def test_process_llm_empty_pair_marks_skipped_and_writes_nothing(monkeypatch, tmp_path):
    en_dir, fr_dir = _patch_dirs(monkeypatch, tmp_path)
    _patch_io(monkeypatch, pair=(None, None))

    res = pipeline._process_llm(SCORE, REPO, "NEW", REPO["pushed_at"], None,
                                dry_run=False)

    assert res["status"] == "SKIPPED_EMPTY"
    assert not en_dir.exists() or not list(en_dir.glob("*.md"))
    assert not fr_dir.exists() or not list(fr_dir.glob("*.md"))


def test_process_llm_dry_run_writes_nothing(monkeypatch, tmp_path):
    en_dir, fr_dir = _patch_dirs(monkeypatch, tmp_path)
    _patch_io(monkeypatch)

    res = pipeline._process_llm(SCORE, REPO, "NEW", REPO["pushed_at"], None,
                                dry_run=True)

    assert res["status"] == "NEW"
    assert not en_dir.exists() and not fr_dir.exists()


# ─── _classify_only : BOOTSTRAP exige les DEUX fiches ────────────────────────

def _write_pair(en_dir: Path, fr_dir: Path, en=True, fr=True):
    if en:
        en_dir.mkdir(parents=True, exist_ok=True)
        (en_dir / "rtthread_rt-thread_fiche.md").write_text(FICHE_EN, encoding="utf-8")
    if fr:
        fr_dir.mkdir(parents=True, exist_ok=True)
        (fr_dir / "rtthread_rt-thread_fiche.md").write_text(FICHE_FR, encoding="utf-8")


def test_classify_bootstrap_when_both_fiches_exist(monkeypatch, tmp_path):
    en_dir, fr_dir = _patch_dirs(monkeypatch, tmp_path)
    _write_pair(en_dir, fr_dir, en=True, fr=True)

    triage = pipeline._classify_only(SCORE, REPO, prev_pa=None)
    assert triage["status"] == "BOOTSTRAP"


def test_classify_needs_llm_when_fr_fiche_missing(monkeypatch, tmp_path):
    """EN présent mais FR absent → NEEDS_LLM (auto-guérison, pas de drift)."""
    en_dir, fr_dir = _patch_dirs(monkeypatch, tmp_path)
    _write_pair(en_dir, fr_dir, en=True, fr=False)

    triage = pipeline._classify_only(SCORE, REPO, prev_pa=None)
    assert triage["status"] == "NEEDS_LLM"


def test_classify_needs_llm_when_en_fiche_missing(monkeypatch, tmp_path):
    en_dir, fr_dir = _patch_dirs(monkeypatch, tmp_path)
    _write_pair(en_dir, fr_dir, en=False, fr=True)

    triage = pipeline._classify_only(SCORE, REPO, prev_pa=None)
    assert triage["status"] == "NEEDS_LLM"


def test_classify_unchanged_untouched_by_bilingual_logic(monkeypatch, tmp_path):
    """pushed_at identique → UNCHANGED, sans regarder le disque."""
    _patch_dirs(monkeypatch, tmp_path)  # répertoires vides

    triage = pipeline._classify_only(SCORE, REPO, prev_pa=REPO["pushed_at"])
    assert triage["status"] == "UNCHANGED"


# ─── Seeds GitHub : remplacement des miroirs stales ──────────────────────────

def test_github_seed_replaces_stale_mirror(monkeypatch):
    """Un seed GitHub plus récent remplace la copie Gitee stale du même slug
    (sinon le miroir mort masque le vrai repo et le hard-filter l'élimine)."""
    stale = {"full_name": "kendryte/nncase", "pushed_at": "2022-01-01T00:00:00+00:00",
             "description": "old mirror"}
    fresh = {"full_name": "kendryte/nncase", "pushed_at": "2026-07-01T00:00:00Z",
             "description": "live repo", "_minerva_source": "github"}
    repos = {"kendryte/nncase": dict(stale)}
    monkeypatch.setattr(pipeline.github_fetcher, "fetch_repo",
                        lambda owner, name: dict(fresh))
    pipeline._fetch_github_seeds(["kendryte/nncase"], repos)
    assert repos["kendryte/nncase"]["_minerva_source"] == "github"


def test_github_seed_does_not_replace_fresher_copy(monkeypatch):
    """Si la copie en place est plus récente ou égale, le seed ne l'écrase pas."""
    existing = {"full_name": "kendryte/nncase", "pushed_at": "2026-08-01T00:00:00+00:00",
                "description": "fresher"}
    older = {"full_name": "kendryte/nncase", "pushed_at": "2026-07-01T00:00:00Z",
             "description": "older", "_minerva_source": "github"}
    repos = {"kendryte/nncase": dict(existing)}
    monkeypatch.setattr(pipeline.github_fetcher, "fetch_repo",
                        lambda owner, name: dict(older))
    pipeline._fetch_github_seeds(["kendryte/nncase"], repos)
    assert repos["kendryte/nncase"]["description"] == "fresher"
