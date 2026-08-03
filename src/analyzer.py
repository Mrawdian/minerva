"""
Semantic filtering and relevance scoring of Gitee repos.

Strategy: multilingual embeddings (sentence-transformers) instead of keyword matching.
For each repo we compare the embedding of the text (`full_name. description. language`) to
the embedding of each domain definition (dense paragraph, in config/domains.json).
Cosine similarity drives the scoring and the admission threshold.

Hard upstream filters (score forced to 0):
  - third_party_* repos (ports of third-party libraries)
  - mirrors/* repos outside watched_owners (international mirrors)

Output schema preserved for compat with translator.generate_fiche, build_dashboard,
build_newsletter, etc.: score_total, scores_par_domaine, mots_cles_matches (empty in
semantic mode), domaine_principal. Additional field: best_similarity (float).
"""

import json
import logging
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

import embedder
import translator

log = logging.getLogger("minerva.analyzer")


CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"
DEFAULT_DOMAINS_FILE = CONFIG_DIR / "domains.json"

RECENCE_MOIS = 6

# HYBRID scoring: a repo is admitted if one of the conditions is true:
#   (a) high semantic similarity (>= HIGH_SIM_THRESHOLD) — semantic-strong path
#   (b) at least 1 discriminating keyword matched — keyword-anchored path
# Empirical calibration on 3621 repos: HIGH_SIM=0.55 too strict (86 retained,
# loses the real embedded ones at sim 0.40-0.55), HIGH_SIM=0.45 sweet spot (371 retained).
# Edge AI keywords previously tightened (cf. config/domains.json) to exclude
# the generic ML ones (ai/ml/transformer/image…) that were seeding ML research noise.
HIGH_SIM_THRESHOLD = 0.45

# Admission v2 — contrastive anti-domain margin: a repo is rejected when
# best_anti_similarity > best_similarity + ANTI_MARGIN. Calibrated on a live
# 12-repo good/bad set (2026-07-30): 0.02 falsely cut alibaba/MNN (gap +0.066,
# its description says "deep learning framework" which leans research-y);
# 0.08 keeps every true positive while still cutting clear off-wedge dominance.
ANTI_MARGIN = 0.08

# Admission v2 — generalist orgs (big tech whose output is mostly off-wedge):
# a curated keyword match is MANDATORY, plus this moderate semantic floor.
# Calibration insight: the big-tech noise (ERNIE-300B, flink-connectors,
# lowcode, weex, PaddleNLP…) matches ZERO curated keywords and entered via the
# semantic-only path (sim ≥ 0.45); the true wedge positives from the same orgs
# (MNN, PaddleOCR) all carry curated keywords but sit at sim 0.36-0.42. Hence:
# keyword required, floor below HIGH_SIM but above noise.
GENERALIST_MIN_SIM = 0.35

# Global bonuses (unchanged vs keyword scoring).
# Utility repos (docs/download-data/toolchain-binaries/helper-tools): demoted,
# not excluded — see score_repo. Pattern mirrors the builders' vitrine rule.
UTILITY_RE = re.compile(r"(docs?$|download|toolchain|tools$)")
UTILITY_PENALTY = 25

BONUS_STARS_100 = 10
BONUS_FORKS_50 = 5
BONUS_ACTIVITE_RECENTE = 5
BONUS_CJK = 3
BONUS_NON_MIROIR = 5
BONUS_WATCHED_OWNER = 8

# Process-local cache of domain embeddings (key = tuple (nom, definition)).
# The disk cache (output/embeddings_cache.json) is managed by embedder.py.
_domain_embeddings_cache: dict[tuple, np.ndarray] = {}


def load_domains(path: Path = DEFAULT_DOMAINS_FILE) -> list[dict]:
    """Loads the domain config from config/domains.json."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["domains"]


def load_anti_domains(path: Path = DEFAULT_DOMAINS_FILE) -> list[dict]:
    """Loads the anti-domain definitions (admission v2) from config/domains.json.

    Anti-domains are OFF-wedge categories (generic ML research, web/app dev,
    cloud/big-data infra). A repo whose similarity to the best anti-domain beats
    its similarity to the best wedge domain (+ margin) is rejected — this targets
    generic big-tech noise without touching the score formula.
    Returns [] if the key is absent (backward compatible)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("anti_domains", [])


def _contains_cjk(text: str) -> bool:
    """True if the text contains at least one unified CJK character (U+4E00..U+9FFF)."""
    return any("一" <= c <= "鿿" for c in text)


def _keyword_in_text(keyword: str, text: str) -> bool:
    """CJK match as substring, ASCII match with ASCII word boundaries, case-insensitive.

    Kept for backward compatibility (tests, offline fallback, etc.). No longer used
    by score_repo in semantic mode but may serve other tools.
    """
    if _contains_cjk(keyword):
        return keyword in text
    pattern = r"\b" + re.escape(keyword) + r"\b"
    return bool(re.search(pattern, text, re.IGNORECASE | re.ASCII))


def _parse_iso_datetime(s: str | None) -> datetime | None:
    if not s:
        return None
    s = s.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def _is_recent(dt: datetime | None, months: int = RECENCE_MOIS) -> bool:
    if dt is None:
        return False
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt) <= timedelta(days=months * 30)


def _is_hard_filtered(repo: dict, watched_owners: list | None) -> str | None:
    """Returns the reason for the hard filtering, or None if not filtered.

    Rejects upstream (score forced to 0):
      - 'third_party': third_party_* repos (ports of third-party libraries)
      - 'mirror_unwatched': mirrors/* repos outside watched_owners
      - 'archived': repos with no push for > 2 years (translator.is_archived)
    """
    full_name = repo.get("full_name") or ""
    if "third_party_" in full_name:
        return "third_party"
    if full_name.startswith("mirrors/"):
        owner = full_name.split("/", 1)[0]
        if not watched_owners or owner not in set(watched_owners):
            return "mirror_unwatched"
    if translator.is_archived(repo):
        return "archived"
    return None


def _match_keywords(repo: dict, domains: list[dict]) -> list[str]:
    """Returns the list of keywords (all domains) matched in the repo text.

    Target text = full_name + description (language excluded to avoid false
    positives like 'C' that matches everywhere). Match via _keyword_in_text (CJK
    substring + ASCII word boundaries, case-insensitive).
    """
    full_name = repo.get("full_name") or ""
    description = repo.get("description") or ""
    text = f"{full_name} {description}"
    # Repo names carry signal but use _ and / as separators, which are word
    # characters for \b — 'unitree_ros' would never match \bros\b. We therefore
    # also match against a normalized copy where _ and / become spaces
    # (hyphens are kept: curated keywords like 'risc-v' contain them).
    normalized = text.replace("_", " ").replace("/", " ")
    matched: list[str] = []
    for d in domains:
        for kw in d.get("mots_cles", []):
            if _keyword_in_text(kw, text) or _keyword_in_text(kw, normalized):
                matched.append(kw)
    return matched


def _build_repo_text(repo: dict) -> str:
    """Source text for the embedding: full_name + description + language.

    We prefix with the name because it often carries signal (e.g. 'esp-idf' → ESP32).
    """
    full_name = repo.get("full_name") or ""
    description = repo.get("description") or ""
    language = repo.get("language") or ""
    parts: list[str] = []
    if full_name:
        parts.append(full_name)
    if description:
        parts.append(description)
    if language:
        parts.append(f"(langage : {language})")
    return ". ".join(parts) if parts else ""


def _domain_embeddings(domains: list[dict]) -> tuple[list[str], np.ndarray]:
    """Computes (or retrieves) the embeddings of the domain definitions.

    Process-local cache indexed by tuple (nom, definition) — invalidated if the
    definition of a domain changes.
    """
    cache_key = tuple((d["nom"], d.get("definition", "")) for d in domains)
    if cache_key in _domain_embeddings_cache:
        return [d["nom"] for d in domains], _domain_embeddings_cache[cache_key]

    e = embedder.get_embedder()
    defs = [
        d.get("definition") or " ".join(d.get("mots_cles", []))
        for d in domains
    ]
    mat = e.embed_batch(defs)
    _domain_embeddings_cache[cache_key] = mat
    return [d["nom"] for d in domains], mat


def score_repo(repo: dict, domains: list[dict], watched_owners: list | None = None) -> dict:
    """Computes the semantic score of a repo via cosine similarity against the domains.

    Hard filters applied upstream (score forced to 0):
      - repos containing 'third_party_' in the full_name
      - repos under 'mirrors/' outside watched accounts

    Args:
        repo: raw Gitee JSON (full_name, description, language, stargazers_count,
            forks_count, pushed_at).
        domains: list of domains with their 'definition' (dense paragraph).
        watched_owners: list of watched accounts. The repo owner is compared
            case-insensitively; if match, +8 watched bonus.

    Returns:
        dict with score_total (0-100), scores_par_domaine (per-domain similarity ×100),
        mots_cles_matches (list of matched discriminating keywords, all domains),
        domaine_principal (top sim), best_similarity (float [0, 1]).
    """
    full_name = repo.get("full_name") or ""

    hard_filter = _is_hard_filtered(repo, watched_owners)
    if hard_filter is not None:
        if hard_filter == "third_party":
            log.info(f"third_party filtré : {full_name}")
        elif hard_filter == "archived":
            log.info(f"archivé (>2 ans) filtré : {full_name}")
        else:
            log.info(f"mirror non surveillé filtré : {full_name}")
        empty_scores = {d["nom"]: 0 for d in domains}
        return {
            "repo_full_name": full_name,
            "score_total": 0,
            "scores_par_domaine": empty_scores,
            "mots_cles_matches": [],
            "domaine_principal": next(iter(empty_scores), "(aucun)"),
            "best_similarity": 0.0,
        }

    matched_keywords = _match_keywords(repo, domains)

    # ─── Semantic scoring ────────────────────────────────────────────────
    text = _build_repo_text(repo)
    e = embedder.get_embedder()
    repo_vec = e.embed(text)  # shape (D,) L2-normalized

    domain_names, domain_mat = _domain_embeddings(domains)  # (N_domains, D)
    sims = domain_mat @ repo_vec  # (N_domains,) — dot product = cosine since normalized

    scores_par_domaine: dict[str, int] = {}
    for name, sim in zip(domain_names, sims):
        scores_par_domaine[name] = max(0, round(100 * float(sim)))

    domaine_principal = max(scores_par_domaine, key=scores_par_domaine.get)
    best_similarity = float(sims.max())
    semantic_score = scores_par_domaine[domaine_principal]

    # ─── Global bonuses (unchanged vs keyword scoring) ───────────────────
    bonus = 0
    description = repo.get("description") or ""
    if (repo.get("stargazers_count") or 0) > 100:
        bonus += BONUS_STARS_100
    if (repo.get("forks_count") or 0) > 50:
        bonus += BONUS_FORKS_50
    if _is_recent(_parse_iso_datetime(repo.get("pushed_at"))):
        bonus += BONUS_ACTIVITE_RECENTE
    if _contains_cjk(description):
        bonus += BONUS_CJK
    if not full_name.startswith("mirrors/"):
        bonus += BONUS_NON_MIROIR

    if watched_owners:
        owner_lc = full_name.split("/", 1)[0].lower()
        watched_lc = {w.lower() for w in watched_owners}
        if owner_lc in watched_lc:
            bonus += BONUS_WATCHED_OWNER

    score_total = min(100, semantic_score + bonus)

    # ─── Utility demotion (owner decision 2026-07-31) ────────────────────
    # Docs mirrors, download-data blobs, toolchain binaries and helper tools
    # are legitimate corpus members but NOT decision-grade projects; a
    # submodule installer must never outrank an inference framework. Targeted
    # demotion — not an exclusion, and the rest of the formula is untouched.
    # Same pattern as the vitrine-curation rule in the builders (keep in sync).
    repo_part = full_name.split("/", 1)[-1].lower()
    if UTILITY_RE.search(repo_part):
        score_total = max(0, score_total - UTILITY_PENALTY)

    return {
        "repo_full_name": full_name,
        "score_total": score_total,
        "scores_par_domaine": scores_par_domaine,
        "mots_cles_matches": matched_keywords,
        "domaine_principal": domaine_principal,
        "best_similarity": best_similarity,
    }


def filter_repos(
    repos: list[dict],
    domains: list[dict],
    min_score: int,
    watched_owners: list | None = None,
    anti_domains: list[dict] | None = None,
    generalist_owners: list | None = None,
) -> list[dict]:
    """Scores each repo, applies the HYBRID admission logic (v2).

    Base admission (at least one condition):
      (a) `best_similarity ≥ HIGH_SIM_THRESHOLD` (0.45) — semantic-strong
      (b) `len(mots_cles_matches) ≥ 1` — keyword-anchored (recovers the sparse-desc)
    Plus the score threshold: `score_total ≥ min_score` (default 15 in sources.json).
    Plus the upstream hard filters (third_party, mirrors outside watched).

    Admission v2 tightening (anti big-tech-noise, both config-driven):
      1. CONTRASTIVE anti-domain filter (all repos): if `anti_domains` are
         provided, a repo is rejected when its best similarity to an anti-domain
         (generic ML research, web/app dev, cloud/big-data infra) exceeds its
         best wedge-domain similarity by more than ANTI_MARGIN. The score
         formula is untouched — this only gates admission.
      2. GENERALIST orgs need BOTH signals: for owners listed in
         `generalist_owners` (big-tech orgs whose output is mostly off-wedge),
         admission requires (a) AND (b), not (a) OR (b). Wedge/vendor orgs keep
         the OR rule.

    Optimization: pre-batch the embeddings of all non-hard-filtered repos in
    ONE single call to model.encode() — divides the inference time by ~10× vs
    unit calls.

    Returns:
        List of the score_info of the retained repos, sorted by descending score.
        Each score_info carries `best_anti_similarity` for transparency.
    """
    # Pre-warm the embedding cache via batch (1 model call instead of N).
    e = embedder.get_embedder()
    texts_to_warm: list[str] = []
    for r in repos:
        if not _is_hard_filtered(r, watched_owners):
            texts_to_warm.append(_build_repo_text(r))
    if texts_to_warm:
        log.info(f"Pré-batch embeddings : {len(texts_to_warm)} textes à encoder…")
        e.embed_batch(texts_to_warm)
        e.save_cache()

    # Pre-warm the domain (and anti-domain) definitions too.
    _domain_embeddings(domains)
    anti_mat = None
    if anti_domains:
        _, anti_mat = _domain_embeddings(anti_domains)

    generalist_lc = {g.lower() for g in (generalist_owners or [])}

    scored = []
    for r in repos:
        s = score_repo(r, domains, watched_owners=watched_owners)
        # Contrastive signal (cache hit: repo text was batch-encoded above).
        if anti_mat is not None and s["score_total"] > 0:
            vec = e.embed(_build_repo_text(r))
            s["best_anti_similarity"] = float((anti_mat @ vec).max())
        else:
            s["best_anti_similarity"] = 0.0
        scored.append(s)

    retained: list[dict] = []
    for s in scored:
        full_name = s["repo_full_name"]
        if not full_name:
            continue

        semantic_strong = s["best_similarity"] >= HIGH_SIM_THRESHOLD
        keyword_anchored = len(s["mots_cles_matches"]) >= 1

        # v2 rule 1 — contrastive rejection: clearly closer to an off-wedge
        # category than to any wedge domain. Applies ONLY to keyword-less
        # repos: calibration showed the noise enters via the semantic-only
        # path (all confirmed offenders had zero curated keywords), while a
        # curated keyword anchor is a high-precision human signal that a
        # statistical similarity should not override (e.g. sophgo/tpu-mlir,
        # whose "Machine learning compiler" description leans ML-research).
        if anti_mat is not None and not keyword_anchored and (
            s["best_anti_similarity"] > s["best_similarity"] + ANTI_MARGIN
        ):
            log.info(
                f"Filtré (anti-domaine {s['best_anti_similarity']:.2f} > "
                f"wedge {s['best_similarity']:.2f}) : {full_name}"
            )
            continue

        # v2 rule 2 — generalist orgs: curated keyword MANDATORY + moderate
        # semantic floor (the semantic-only path is where big-tech noise
        # entered; the true wedge positives all carry curated keywords).
        owner_lc = full_name.split("/", 1)[0].lower()
        if owner_lc in generalist_lc:
            admitted = (keyword_anchored
                        and s["best_similarity"] >= GENERALIST_MIN_SIM)
            reason = (
                f"généraliste : mot-clé requis ({len(s['mots_cles_matches'])}) "
                f"+ sim {s['best_similarity']:.2f} ≥ {GENERALIST_MIN_SIM}"
            )
        else:
            admitted = semantic_strong or keyword_anchored
            reason = (
                f"sim {s['best_similarity']:.2f} < {HIGH_SIM_THRESHOLD} "
                f"ET 0 mot-clé"
            )

        if not admitted:
            log.info(f"Filtré ({reason}) : {full_name}")
            continue
        if s["score_total"] < min_score:
            continue
        retained.append(s)

    retained.sort(key=lambda s: s["score_total"], reverse=True)
    return retained


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    domains = load_domains()
    print(f"Domaines chargés : {[d['nom'] for d in domains]}")
    print(f"Définitions présentes : {[bool(d.get('definition')) for d in domains]}")

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    test_repos = [
        {
            "full_name": "openharmony/kernel_liteos_a",
            "description": "Huawei LiteOS kernel for embedded devices 华为轻量级物联网操作系统",
            "language": "C",
            "stargazers_count": 2284,
            "forks_count": 1087,
            "pushed_at": "2025-09-15T10:30:00+08:00",
        },
        {
            "full_name": "openharmony/third_party_icu",
            "description": "ICU library port for OpenHarmony",
            "language": "C++",
            "stargazers_count": 5,
            "forks_count": 2,
            "pushed_at": "2025-12-01T10:30:00+08:00",
        },
        {
            "full_name": "ByteDance/xgplayer",
            "description": "A HTML5 video player",
            "language": "JavaScript",
            "stargazers_count": 200,
            "forks_count": 40,
            "pushed_at": "2026-04-01T00:00:00+00:00",
        },
        {
            "full_name": "Tencent/ncnn",
            "description": "高性能神经网络前向计算框架, optimized for mobile",
            "language": "C++",
            "stargazers_count": 19000,
            "forks_count": 4000,
            "pushed_at": "2026-03-01T00:00:00+00:00",
        },
    ]

    scored = filter_repos(test_repos, domains, min_score=15, watched_owners=["openharmony", "tencent"])
    for s in scored:
        print(f"\n{s['repo_full_name']}")
        print(f"  score: {s['score_total']}  sim: {s['best_similarity']:.3f}")
        print(f"  domaine: {s['domaine_principal']}")
        print(f"  scores_par_domaine: {s['scores_par_domaine']}")

    print(f"\nRetenus : {len(scored)}/{len(test_repos)} (xgplayer doit être hors)")
