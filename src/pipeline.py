"""
Minerva's weekly orchestrator.

Chains: fetcher.list_all_repos_by_owner → analyzer.filter_repos → translator.generate_fiche.
Any error on a given repo is logged but never breaks the pipeline.

Usage:
    python src/pipeline.py [--token <gitee_token>] [--dry-run]
"""

import argparse
import json
import logging
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import analyzer  # noqa: E402
import fetcher  # noqa: E402
import github_fetcher  # noqa: E402
import translator  # noqa: E402


CONFIG_DIR = ROOT / "config"
OUTPUT_DIR = ROOT / "output"
FICHES_DIR = OUTPUT_DIR / "fiches"        # English set (default language)
FICHES_FR_DIR = OUTPUT_DIR / "fiches_fr"  # French set (language 2), same slugs
LOGS_DIR = OUTPUT_DIR / "logs"
STATE_FILE = OUTPUT_DIR / "state.json"
ENV_FILE = ROOT / ".env"

log = logging.getLogger("minerva")


def _load_dotenv(path: Path = ENV_FILE) -> None:
    """Loads a minimal .env file (KEY=VALUE per line) into os.environ.

    - Ignores comments (#...) and empty lines.
    - Overrides the variables already defined in the environment (python-dotenv convention):
      avoids an old key persisted at the OS level (Windows User scope, for example)
      masking the file's up-to-date value.
    - Strips single/double quotes around the value.
    """
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


def load_config() -> dict:
    """Loads config/sources.json and config/domains.json."""
    sources = json.loads((CONFIG_DIR / "sources.json").read_text(encoding="utf-8"))
    domains_data = json.loads((CONFIG_DIR / "domains.json").read_text(encoding="utf-8"))
    return {
        "sources": sources,
        "domains": domains_data["domains"],
        "anti_domains": domains_data.get("anti_domains", []),
    }


def setup_logging(log_dir: str | Path = LOGS_DIR) -> str:
    """Configures the 'minerva' logger to stdout + timestamped file."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"minerva_{timestamp}.log"

    logger = logging.getLogger("minerva")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.propagate = False

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return str(log_file)


def _fetch_accounts(comptes: list[str]) -> tuple[dict[str, dict], set[str]]:
    """For each account, list_all_repos_by_owner + deduplication by full_name.

    The detail of the result (HTTP, count) is logged by fetcher itself.

    Returns:
        (repos, failed_owners) — failed_owners contains the owners for which
        enumeration partially failed. Their repos will be protected against
        a false deletion detection.
    """
    repos: dict[str, dict] = {}
    failed_owners: set[str] = set()
    for compte in comptes:
        try:
            found = fetcher.list_all_repos_by_owner(compte)
            for r in found:
                full_name = r.get("full_name")
                if full_name and full_name not in repos:
                    repos[full_name] = r
        except fetcher.FetchPaginationError as exc:
            log.error(
                f"{exc} — repos de [{compte}] protégés contre fausse détection de suppression"
            )
            failed_owners.add(compte.lower())
        except Exception as exc:
            log.error(f"Erreur lors de la récupération de {compte} : {exc}")
            failed_owners.add(compte.lower())
    return repos, failed_owners


def _fetch_github_accounts(
    comptes: list[str], repos: dict[str, dict]
) -> set[str]:
    """Like _fetch_accounts but on the GitHub side, with merge into the `repos` dict.

    The GitHub repos are added only if their full_name does not already exist
    (Gitee takes priority in case of an unlikely owner/repo slug collision).

    Returns:
        github_failed_owners — GitHub owners (lowercased) with partial
        enumeration, to be protected against a false deletion detection. Same
        form as fetcher on the Gitee side (bare lowercased owner) because the protection
        compares `full_name.split('/')[0].lower()`.
    """
    github_failed: set[str] = set()
    for compte in comptes:
        try:
            found = github_fetcher.list_all_repos_by_owner(compte)
            for r in found:
                full_name = r.get("full_name")
                if full_name and full_name not in repos:
                    repos[full_name] = r
        except github_fetcher.GitHubPaginationError as exc:
            log.error(
                f"{exc} — repos GitHub de [{compte}] protégés contre fausse "
                f"détection de suppression"
            )
            github_failed.add(compte.lower())
        except Exception as exc:
            log.error(f"Erreur lors de la récupération GitHub de {compte} : {exc}")
            github_failed.add(compte.lower())
    return github_failed


def _fetch_github_seeds(seeds: list[str], repos: dict[str, dict]) -> int:
    """Like _fetch_seeds but on the GitHub side. Returns the number of new repos.

    Unlike account enumeration (where Gitee wins on slug collision), a GitHub
    seed REPLACES an already-present copy when its pushed_at is more recent:
    several vendors (Kendryte, Bouffalo…) have a dead Gitee mirror while their
    live development is on GitHub — an explicit hand-curated seed must not be
    shadowed by a stale mirror (which the archived hard-filter would then cut,
    silently losing the repo entirely)."""
    if not seeds:
        return 0
    added = 0
    for slug in seeds:
        if "/" not in slug:
            log.warning(f"Seed GitHub invalide (manque '/') : {slug}")
            continue
        owner, name = slug.split("/", 1)
        try:
            r = github_fetcher.fetch_repo(owner, name)
            if r is None:
                log.warning(f"Seed GitHub introuvable : {slug}")
                continue
            full_name = r.get("full_name") or slug
            existing = repos.get(full_name)
            if existing is None:
                repos[full_name] = r
                added += 1
                log.info(f"Seed GitHub ajouté : {full_name}")
            elif (r.get("pushed_at") or "") > (existing.get("pushed_at") or ""):
                repos[full_name] = r
                log.info(
                    f"Seed GitHub remplace une copie plus ancienne (miroir stale) : {full_name}"
                )
        except Exception as exc:
            log.error(f"Erreur seed GitHub {slug} : {exc}")
    log.info(f"Seeds GitHub : {added} nouveaux repos ajoutés sur {len(seeds)} demandés")
    return added


def _search_keywords(mots_cles: list[str], token: str | None, repos: dict[str, dict]) -> None:
    """Skip — Gitee's /search/repositories API is broken (systematically returns []).

    Diagnosis 2026-04-25: the endpoint responds HTTP 200 with an empty array for
    any request, including common keywords (linux, redis, etc.). The sibling
    endpoints (/search/users, /search/issues) work with the same token,
    so it is not an auth problem but a server bug on the Gitee side.

    Replacement mechanism: sources.json["seeds_gitee"], see _fetch_seeds().
    """
    if mots_cles:
        log.info(
            f"Recherche par mot-clés ({len(mots_cles)} keywords) skipée — "
            f"endpoint Gitee /search/repositories cassé (renvoie [] systématiquement). "
            f"Utiliser sources.json['seeds_gitee'] à la place."
        )


def _fetch_seeds(seeds: list[str], repos: dict[str, dict]) -> int:
    """For each 'owner/repo' slug in seeds, fetch_repo and add if new.

    Replacement mechanism for keyword search. Allows explicitly including
    repos outside the watched accounts.

    Returns:
        Number of new repos added.
    """
    if not seeds:
        return 0
    added = 0
    for slug in seeds:
        if "/" not in slug:
            log.warning(f"Seed invalide (manque '/') : {slug}")
            continue
        if slug in repos:
            continue
        owner, name = slug.split("/", 1)
        try:
            r = fetcher.fetch_repo(owner, name)
            if r is None:
                log.warning(f"Seed introuvable : {slug}")
                continue
            full_name = r.get("full_name") or slug
            if full_name not in repos:
                repos[full_name] = r
                added += 1
                log.info(f"Seed ajouté : {full_name}")
        except Exception as exc:
            log.error(f"Erreur seed {slug} : {exc}")
    log.info(f"Seeds : {added} nouveaux repos ajoutés sur {len(seeds)} demandés")
    return added


def _load_state(path: Path = STATE_FILE) -> dict:
    """Loads state.json. Returns {last_run: None, repos: {}} if absent/unreadable."""
    if not path.is_file():
        return {"last_run": None, "repos": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        log.warning(f"state.json illisible ({exc}) — repart de zéro")
        return {"last_run": None, "repos": {}}


def _save_state(repos_state: dict[str, str],
                skipped: dict[str, dict] | None = None,
                path: Path = STATE_FILE) -> None:
    """Saves state.json with last_run UTC + repos dict.

    Preserves the 'scores' key (fed by scripts/rescore.py) if it exists
    in the previous state.json. Filters out the score entries corresponding to
    repos that are no longer tracked, to avoid drift.

    Also persists 'skipped' (mapping full_name → {reason, at_pushed, at_run})
    which remembers the repos discarded via _looks_like_empty_fiche to avoid
    re-paying the LLM on subsequent runs as long as pushed_at has not changed.
    """
    existing: dict = {}
    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = {}

    state = {
        "last_run": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repos": repos_state,
    }

    prev_scores = existing.get("scores")
    if isinstance(prev_scores, dict):
        state["scores"] = {k: v for k, v in prev_scores.items() if k in repos_state}

    if skipped:
        state["skipped"] = skipped

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _parse_pushed_at(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def _classify(current_pa: str | None, prev_pa: str | None) -> str:
    """Returns 'NEW' / 'MODIFIED' / 'UNCHANGED' according to the evolution of pushed_at."""
    if prev_pa is None:
        return "NEW"
    cur = _parse_pushed_at(current_pa)
    prev = _parse_pushed_at(prev_pa)
    if cur is None or prev is None:
        return "UNCHANGED"
    if cur > prev:
        return "MODIFIED"
    return "UNCHANGED"


def _fiche_path(repo_full_name: str, lang_dir: Path | None = None) -> Path:
    """Computes the fiche path for a slug. Must match translator.save_fiche.

    `lang_dir=None` resolves to FICHES_DIR at call time (not at import time),
    so tests can monkeypatch the module-level directories."""
    slug = re.sub(r"[^A-Za-z0-9_\-]", "_", repo_full_name.replace("/", "_"))
    base = lang_dir if lang_dir is not None else FICHES_DIR
    return base / f"{slug}_fiche.md"


def _both_fiches_exist(repo_full_name: str) -> bool:
    """True only if BOTH the EN and FR fiches are on disk.

    Used by the BOOTSTRAP short-circuit: if either language is missing, the repo
    goes through NEEDS_LLM so the pair is regenerated together (self-healing —
    the two sets can never silently drift apart)."""
    return (_fiche_path(repo_full_name, FICHES_DIR).exists()
            and _fiche_path(repo_full_name, FICHES_FR_DIR).exists())


def _add_modified_badge(fiche: str, full_name: str) -> str:
    """Adds [MODIFIÉ] in the H2 title of the fiche."""
    return fiche.replace(f"## {full_name}\n", f"## {full_name} [MODIFIÉ]\n", 1)


LLM_WORKERS = int(os.environ.get("MINERVA_LLM_WORKERS", "8"))


def _classify_only(score_info: dict, repo: dict, prev_pa: str | None,
                   prev_skipped: dict | None = None) -> dict:
    """Initial triage without I/O. Returns a dict with status for the parallel splitting.

    Possible statuses:
      - ARCHIVED         : pushed_at > 2 years, archived flag, or status=关闭 (definitive skip)
      - UNCHANGED        : pushed_at identical to the previous one (carry-forward state)
      - SKIPPED_EMPTY    : already skipped on the previous run AND pushed_at unchanged (LLM saving)
      - BOOTSTRAP        : NEW but BOTH EN+FR fiches already on disk (skip LLM, keep state)
      - NEEDS_LLM        : to be processed in parallel (NEW with either fiche missing,
                           or MODIFIED)
    """
    full_name = score_info["repo_full_name"]
    if translator.is_archived(repo):
        return {"full_name": full_name, "status": "ARCHIVED"}

    current_pa = repo.get("pushed_at") or ""

    # Short-circuit: if we have already skipped this repo (LLM signaled empty) AND pushed_at
    # has not changed, we avoid the costly LLM call. If pushed_at changes → we retry.
    if prev_skipped and full_name in prev_skipped:
        prev_skipped_pa = prev_skipped[full_name].get("at_pushed")
        if prev_skipped_pa and prev_skipped_pa == current_pa:
            return {"full_name": full_name, "status": "SKIPPED_EMPTY",
                    "current_pa": current_pa}

    status = _classify(current_pa, prev_pa)

    if status == "UNCHANGED":
        return {"full_name": full_name, "status": "UNCHANGED",
                "pushed_at": prev_pa or current_pa}

    if status == "NEW" and _both_fiches_exist(full_name):
        return {"full_name": full_name, "status": "BOOTSTRAP",
                "pushed_at": current_pa}

    return {"full_name": full_name, "status": "NEEDS_LLM",
            "sub_status": status, "current_pa": current_pa, "prev_pa": prev_pa}


def _process_llm(score_info: dict, repo: dict, sub_status: str,
                 current_pa: str, prev_pa: str | None, dry_run: bool) -> dict:
    """Heavy I/O processing: fetch README + Claude calls + save the EN+FR pair.

    Bilingual is a native property of the run: translator.generate_fiche_pair
    produces both fiches from a single source of facts (one EN generation + one
    EN→FR prose translation), and both are saved together — so the two sets can
    never drift apart.

    Called from a ThreadPoolExecutor — must be thread-safe (the functions
    fetcher.fetch_readme and translator.generate_fiche_pair are, via _rate_lock
    and via the Anthropic SDK which is thread-safe).
    """
    full_name = score_info["repo_full_name"]
    parts = full_name.split("/", 1)
    if len(parts) != 2:
        return {"full_name": full_name, "status": "ERROR", "reason": "full_name invalide"}
    owner, repo_name = parts
    branch = repo.get("default_branch") or "master"
    source_fetcher = (
        github_fetcher if repo.get("_minerva_source") == "github" else fetcher
    )

    readme: str | None = None
    try:
        readme = source_fetcher.fetch_readme(owner, repo_name, branch)
    except Exception as exc:
        log.warning(f"Erreur README pour {full_name} : {exc}")

    try:
        fiche_en, fiche_fr = translator.generate_fiche_pair(repo, readme, score_info)
    except Exception as exc:
        log.error(f"Erreur génération fiche pour {full_name} : {exc}")
        return {"full_name": full_name, "status": "ERROR", "reason": str(exc)}

    if fiche_en is None:
        # The LLM itself signaled empty content (cf. _looks_like_empty_fiche).
        # We mark skipped to avoid re-paying the LLM on subsequent runs as long as
        # the repo has not been repushed (cf. _classify_only).
        log.info(f"Fiche écartée (signal vide post-LLM) : {full_name}")
        return {"full_name": full_name, "status": "SKIPPED_EMPTY",
                "current_pa": current_pa, "prev_pa": prev_pa}

    if sub_status == "MODIFIED":
        fiche_en = _add_modified_badge(fiche_en, full_name)
        fiche_fr = _add_modified_badge(fiche_fr, full_name)

    if not dry_run:
        try:
            translator.save_fiche(fiche_en, full_name, str(FICHES_DIR))
            translator.save_fiche(fiche_fr, full_name, str(FICHES_FR_DIR))
        except Exception as exc:
            log.error(f"Erreur sauvegarde fiche pour {full_name} : {exc}")
            return {"full_name": full_name, "status": "ERROR", "reason": str(exc)}

    log.info(f"Fiche générée EN+FR [{sub_status}] : {full_name}")
    return {"full_name": full_name, "status": sub_status,
            "current_pa": current_pa, "prev_pa": prev_pa}


def _generate_fiches(
    scored: list[dict],
    repos: dict[str, dict],
    prev_repos_state: dict[str, str],
    dry_run: bool,
    prev_skipped: dict | None = None,
) -> dict:
    """Orchestration: fast sequential triage + parallelization of the LLM calls.

    Phase 1 (sequential, no I/O): classify each repo into ARCHIVED /
    UNCHANGED / BOOTSTRAP / NEEDS_LLM.

    Phase 2 (parallel, heavy I/O): for the NEEDS_LLM, launch fetch_readme +
    generate_fiche in a ThreadPoolExecutor (MINERVA_LLM_WORKERS, default 8).

    Returns:
        dict with fiches_count, new/modified/bootstrap counts, lists, new_state_repos.
    """
    new_state_repos: dict[str, str] = {}
    new_skipped_empty: dict[str, dict] = {}  # feeds the state['skipped'] key
    skipped_archived = 0
    skipped_unchanged = 0
    skipped_empty = 0
    bootstrap_count = 0
    new_count = 0
    modified_count = 0
    new_list: list[str] = []
    modified_list: list[tuple[str, str | None, str | None]] = []
    error_count = 0

    # ─── Phase 1: fast triage ────────────────────────────────────────────
    needs_llm: list[tuple[dict, dict, str, str, str | None]] = []
    for score_info in scored:
        full_name = score_info["repo_full_name"]
        repo = repos.get(full_name)
        if not repo:
            continue

        prev_pa = prev_repos_state.get(full_name)
        triage = _classify_only(score_info, repo, prev_pa, prev_skipped=prev_skipped)
        st = triage["status"]

        if st == "ARCHIVED":
            log.info(f"Ignoré (archivé) : {full_name}")
            skipped_archived += 1
        elif st == "UNCHANGED":
            log.info(f"Ignoré (inchangé) : {full_name}")
            skipped_unchanged += 1
            new_state_repos[full_name] = triage["pushed_at"]
        elif st == "SKIPPED_EMPTY":
            log.info(f"Ignoré (skipped:empty_fiche, pushed_at inchangé) : {full_name}")
            skipped_empty += 1
            # Carry-forward of the existing skipped entry (no new timestamp)
            if prev_skipped and full_name in prev_skipped:
                new_skipped_empty[full_name] = prev_skipped[full_name]
        elif st == "BOOTSTRAP":
            log.info(f"Bootstrap (fiche déjà sur disque) : {full_name}")
            bootstrap_count += 1
            new_state_repos[full_name] = triage["pushed_at"]
        elif st == "NEEDS_LLM":
            needs_llm.append((score_info, repo, triage["sub_status"],
                              triage["current_pa"], triage["prev_pa"]))

    log.info(
        f"Triage : {len(needs_llm)} fiches à générer (LLM), "
        f"{bootstrap_count} bootstrap, {skipped_unchanged} inchangées, "
        f"{skipped_archived} archivées"
    )

    # ─── Phase 2: parallelization of the LLM calls ───────────────────────
    if needs_llm:
        log.info(f"Lancement parallèle : {len(needs_llm)} repos × {LLM_WORKERS} workers")
        with ThreadPoolExecutor(max_workers=LLM_WORKERS) as ex:
            futures = {
                ex.submit(_process_llm, si, r, ss, cpa, ppa, dry_run): si["repo_full_name"]
                for (si, r, ss, cpa, ppa) in needs_llm
            }
            for fut in as_completed(futures):
                full_name = futures[fut]
                try:
                    res = fut.result()
                except Exception as exc:
                    log.error(f"Worker exception pour {full_name} : {exc}")
                    error_count += 1
                    continue

                st = res.get("status")
                if st == "NEW":
                    new_count += 1
                    new_list.append(res["full_name"])
                    new_state_repos[res["full_name"]] = res["current_pa"]
                elif st == "MODIFIED":
                    modified_count += 1
                    modified_list.append((res["full_name"], res["prev_pa"], res["current_pa"]))
                    new_state_repos[res["full_name"]] = res["current_pa"]
                elif st == "SKIPPED_EMPTY":
                    skipped_empty += 1
                    new_skipped_empty[res["full_name"]] = {
                        "reason": "empty_fiche",
                        "at_pushed": res["current_pa"],
                        "at_run": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    }
                else:
                    error_count += 1

    fiches_count = new_count + modified_count

    # Deterministic sort for the reports (the as_completed order is non-deterministic)
    new_list.sort()
    modified_list.sort(key=lambda x: x[0])

    if skipped_archived:
        log.info(f"{skipped_archived} repos ignorés car archivés (pushed_at > 2 ans, flag archived ou status=关闭)")
    if skipped_unchanged:
        log.info(f"{skipped_unchanged} repos ignorés car inchangés depuis le dernier run")
    if skipped_empty:
        log.info(f"{skipped_empty} repos écartés car le LLM a signalé un contenu vide (skipped:empty_fiche)")
    if bootstrap_count:
        log.info(f"{bootstrap_count} repos bootstrappés (fiches déjà sur disque, pas d'appel LLM)")
    if error_count:
        log.warning(f"{error_count} repos en erreur de traitement")

    return {
        "fiches_count": fiches_count,
        "new_count": new_count,
        "modified_count": modified_count,
        "bootstrap_count": bootstrap_count,
        "skipped_archived": skipped_archived,
        "skipped_unchanged": skipped_unchanged,
        "skipped_empty": skipped_empty,
        "new_list": new_list,
        "modified_list": modified_list,
        "new_state_repos": new_state_repos,
        "new_skipped_empty": new_skipped_empty,
    }


def _write_diff_report(
    new_list: list[str],
    modified_list: list[tuple[str, str | None, str | None]],
    deleted_list: list[str],
    skipped_unchanged: int,
    bootstrap_count: int,
    prev_last_run: str | None,
) -> Path:
    """Writes output/diff_YYYYMMDD.md summarizing the changes since the last run."""
    today = datetime.now().strftime("%Y%m%d")
    out_path = OUTPUT_DIR / f"diff_{today}.md"
    total_updated = len(new_list) + len(modified_list)

    lines: list[str] = []
    lines.append(f"# Diff Minerva — {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")
    if prev_last_run:
        lines.append(f"Comparaison avec le run du **{prev_last_run}**.")
    else:
        lines.append("**Premier run** — aucun état précédent à comparer.")
    lines.append("")
    lines.append("## Résumé")
    lines.append(f"- 🆕 Nouveaux repos : **{len(new_list)}**")
    lines.append(f"- 🔄 Repos modifiés : **{len(modified_list)}**")
    lines.append(f"- 🗑️ Repos supprimés : **{len(deleted_list)}**")
    lines.append(f"- ✅ Inchangés (skipés) : **{skipped_unchanged}**")
    if bootstrap_count:
        lines.append(f"- 📦 Bootstrappés (fiche pré-existante) : **{bootstrap_count}**")
    lines.append(f"- 📊 Total fiches mises à jour : **{total_updated}**")

    if new_list:
        lines.append("")
        lines.append(f"## 🆕 Nouveaux ({len(new_list)})")
        for fn in sorted(new_list):
            lines.append(f"- {fn}")

    if modified_list:
        lines.append("")
        lines.append(f"## 🔄 Modifiés ({len(modified_list)})")
        for fn, prev_pa, cur_pa in sorted(modified_list):
            prev_short = (prev_pa or "?")[:10]
            cur_short = (cur_pa or "?")[:10]
            lines.append(f"- {fn} (push {prev_short} → {cur_short})")

    if deleted_list:
        lines.append("")
        lines.append(f"## 🗑️ Supprimés ({len(deleted_list)})")
        for fn in sorted(deleted_list):
            lines.append(f"- {fn}")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def run_pipeline(token: str | None = None, dry_run: bool = False) -> dict:
    """Runs the complete pipeline with diff vs the previous run."""
    log.info("=== Minerva Pipeline démarré ===")
    if dry_run:
        log.info("Mode DRY-RUN activé (pas de sauvegarde, pas de state.json, pas de diff)")
    log.info(f"Mode {'authentifié (token Gitee)' if token else 'anonyme'}")

    fetcher.configure(token)

    prev_state = _load_state()
    prev_repos_state = prev_state.get("repos", {})
    prev_last_run = prev_state.get("last_run")
    if prev_last_run:
        log.info(f"State précédent chargé : {len(prev_repos_state)} repos (run du {prev_last_run})")
    else:
        log.info("State précédent absent — premier run, mode bootstrap")

    config = load_config()
    sources = config["sources"]
    domains = config["domains"]
    min_score = int(sources.get("min_score", 15))
    comptes_gitee = sources.get("comptes_gitee", [])
    comptes_github = sources.get("comptes_github", [])
    # The scoring "watched owner" bonus applies to the official orgs of both
    # platforms: we merge the lists for the analyzer.
    watched_owners = list(comptes_gitee) + list(comptes_github)
    log.info(f"Seuil pertinence : {min_score} (watched) / {min_score + 5} (non-watched)")

    repos, failed_owners = _fetch_accounts(comptes_gitee)
    _search_keywords(sources.get("mots_cles_surveillance", []), token, repos)
    _fetch_seeds(sources.get("seeds_gitee", []), repos)

    # ─── GitHub connector (Chinese orgs absent from Gitee) ───────────────
    if comptes_github or sources.get("seeds_github"):
        github_token = os.environ.get("GITHUB_TOKEN")
        github_fetcher.configure(github_token)
        log.info(
            f"GitHub : {len(comptes_github)} orgs surveillées "
            f"({'authentifié' if github_token else 'anonyme, 60 req/h'})"
        )
        github_failed = _fetch_github_accounts(comptes_github, repos)
        _fetch_github_seeds(sources.get("seeds_github", []), repos)
        failed_owners |= github_failed

    log.info(f"Total repos uniques : {len(repos)}")
    if failed_owners:
        log.warning(
            f"{len(failed_owners)} owners avec fetch incomplet : {sorted(failed_owners)} "
            f"— leurs repos sont exemptés de détection de suppression ce run"
        )

    # Deletion detection: a repo is marked deleted only if its owner
    # was completely enumerated (otherwise = fetch bug, not a real deletion).
    deleted_list: list[str] = []
    protected_count = 0
    for fn in prev_repos_state:
        if fn in repos:
            continue
        owner = fn.split("/", 1)[0].lower()
        if owner in failed_owners:
            protected_count += 1
            continue
        deleted_list.append(fn)
    for fn in deleted_list:
        log.info(f"Repo supprimé : {fn}")
    if protected_count:
        log.info(f"{protected_count} repos préservés du diff (owner avec fetch incomplet)")

    scored = analyzer.filter_repos(
        list(repos.values()),
        domains,
        min_score=min_score,
        watched_owners=watched_owners,
        anti_domains=config.get("anti_domains") or None,
        generalist_owners=sources.get("generalist_orgs") or None,
    )
    log.info(f"Repos pertinents : {len(scored)} / {len(repos)} total")

    prev_skipped = prev_state.get("skipped", {}) or {}
    if prev_skipped:
        log.info(f"State précédent : {len(prev_skipped)} repos en skipped:empty_fiche")

    stats = _generate_fiches(scored, repos, prev_repos_state, dry_run, prev_skipped=prev_skipped)

    # Carry-forward: the repos of the failed owners (incomplete pagination) stay
    # in state.json with their old pushed_at, otherwise they would be lost.
    if failed_owners:
        carried = 0
        for fn, prev_pa in prev_repos_state.items():
            if fn in stats["new_state_repos"]:
                continue
            owner = fn.split("/", 1)[0].lower()
            if owner in failed_owners:
                stats["new_state_repos"][fn] = prev_pa
                carried += 1
        if carried:
            log.info(f"{carried} entrées state préservées (owners avec fetch incomplet)")

    if not dry_run:
        _save_state(stats["new_state_repos"], skipped=stats.get("new_skipped_empty"))
        log.info(
            f"state.json sauvegardé : {len(stats['new_state_repos'])} repos"
            + (f", {len(stats.get('new_skipped_empty') or {})} skipped" if stats.get('new_skipped_empty') else "")
        )
        diff_path = _write_diff_report(
            new_list=stats["new_list"],
            modified_list=stats["modified_list"],
            deleted_list=deleted_list,
            skipped_unchanged=stats["skipped_unchanged"],
            bootstrap_count=stats["bootstrap_count"],
            prev_last_run=prev_last_run,
        )
        log.info(f"Rapport diff écrit : {diff_path}")

    log.info(
        f"=== Pipeline terminé : {stats['new_count']} nouveaux, "
        f"{stats['modified_count']} modifiés, {stats['skipped_unchanged']} inchangés, "
        f"{len(deleted_list)} supprimés, {stats['bootstrap_count']} bootstrappés, "
        f"{stats['skipped_empty']} skipped:empty_fiche ==="
    )
    return {
        "total_repos": len(repos),
        "pertinents": len(scored),
        "new": stats["new_count"],
        "modified": stats["modified_count"],
        "unchanged_skipped": stats["skipped_unchanged"],
        "deleted": len(deleted_list),
        "bootstrap": stats["bootstrap_count"],
        "fiches_generees": stats["fiches_count"],
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(description="Pipeline Minerva")
    parser.add_argument("--token", help="Access token Gitee (ou via env GITEE_TOKEN)")
    parser.add_argument("--dry-run", action="store_true", help="N'écrit pas de fiche sur disque")
    args = parser.parse_args()

    _load_dotenv()

    log_file = setup_logging()
    log.info(f"Log file : {log_file}")

    token = args.token or os.environ.get("GITEE_TOKEN")
    stats = run_pipeline(token=token, dry_run=args.dry_run)

    print("\n" + json.dumps(stats, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
