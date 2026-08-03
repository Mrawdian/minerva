"""Builds Minerva's committed, machine-readable run history — the Track 2 foundation.

Produces the single source of truth that a future signal layer, briefings and
rankings all read from (see docs/HISTORY_ARTIFACT.md). It replaces the git-ignored,
markdown `output/diff_*.md` and the last-run-only `state.json` with two committed
files:

  output/repo_ledger.json   durable per-repo state (first_seen, last_changed,
                            removed tombstone, score, domaine, confidence, stars,
                            pushed_at, source) — the current truth per repo.
  output/history.jsonl      append-only, one JSON object per run: new / modified /
                            removed lists + build_date + corpus_size + bootstrap.

Honesty guardrails encoded here (docs/HISTORY_ARTIFACT.md):
  1. first_seen is bootstrapped: on the very first run (no prior ledger), every
     current repo gets first_seen = build_date as a BASELINE and the run line is
     marked bootstrap=true with new=[]. No "NEW" is claimed on day one.
  2. DELETED is a tombstone: a removed repo is KEPT in the ledger with a `removed`
     date, never dropped, so briefs/UI can say "X removed at run Y" honestly.

Determinism: build_date and the run stamp come from state.json's `last_run`, never
from wall-clock — the artifact is tied to the run, not to when this script executes.

USAGE (do NOT run before the fresh launch run — bootstrapping on a
soon-to-be-superseded snapshot would waste the baseline):
    python scripts/build_history.py            # write ledger + append history line
    python scripts/build_history.py --dry-run  # compute & print, write nothing

This module is import-safe: `compute_history` is pure and pulls no heavy deps;
the fiche/state readers are imported lazily inside main().
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output"
STATE_FILE = OUT_DIR / "state.json"
LEDGER_FILE = OUT_DIR / "repo_ledger.json"
HISTORY_FILE = OUT_DIR / "history.jsonl"


# ============================================================================
# PURE CORE (no I/O, no heavy imports — unit-tested on synthetic data)
# ============================================================================

def _pushed(item: dict) -> str:
    """Raw pushed_at (ISO) used to detect MODIFIED; '' if absent."""
    return item.get("pushed_at") or ""


def is_mass_removal(prior_live_count: int, removed_count: int) -> bool:
    """Tripwire mirror of pipeline._deletion_collapse (post-mortem 2026-08-03):
    >50% of the live ledger tombstoned in one run = presumed collection
    collapse, not world movement. The history artifact must never record a
    failure as signal."""
    return prior_live_count >= 10 and removed_count > 0.5 * prior_live_count


def _source_of(item: dict) -> str:
    return "github" if "github.com" in (item.get("gitee_url") or "").lower() else "gitee"


def compute_history(prior_ledger: dict, current_items: list, run_iso: str):
    """Diff the current corpus against the prior ledger and return the updated
    (ledger, run_line). Pure: no file access, no clock.

    prior_ledger : {full_name: entry}  (entry may carry a `removed` date = tombstone)
    current_items: list of dicts from build_site.build_items (full_name, score,
                   domaine_primary, confidence, stars, pushed_at, date, gitee_url)
    run_iso      : state.json `last_run` (ISO); build_date = run_iso[:10]
    """
    build_date = (run_iso or "")[:10]
    bootstrap = not prior_ledger  # first run ever → no honest NEW to claim

    cur = {it["full_name"]: it for it in current_items}
    prior_live = {n: e for n, e in prior_ledger.items() if not e.get("removed")}

    if bootstrap:
        new_l, mod_l, rem_l = [], [], []
    else:
        new_l = sorted(n for n in cur if n not in prior_live)
        rem_l = sorted(n for n in prior_live if n not in cur)
        mod_l = sorted(
            n for n in cur
            if n in prior_live and _pushed(cur[n]) != prior_live[n].get("pushed_at")
        )

    changed = set(new_l) | set(mod_l)
    ledger = dict(prior_ledger)  # carry tombstones + untouched entries forward

    for name, it in cur.items():
        prev = prior_ledger.get(name) or {}
        first_seen = prev.get("first_seen") or build_date
        if bootstrap or name in changed:
            last_changed = build_date
        else:
            last_changed = prev.get("last_changed") or build_date
        ledger[name] = {
            "first_seen": first_seen,
            "last_changed": last_changed,
            "removed": None,  # a returning repo clears its old tombstone
            "score": it.get("score"),
            "domaine": it.get("domaine_primary") or it.get("domaine"),
            "confidence": it.get("confidence"),
            "stars": it.get("stars"),
            "pushed_at": _pushed(it),
            "pushed_at_month": it.get("date"),
            "source": _source_of(it),
        }

    # DELETED → tombstone (keep the entry, stamp the removal date)
    for name in rem_l:
        if name in ledger:
            ledger[name] = {**ledger[name], "removed": build_date}

    run_line = {
        "run": run_iso,
        "build_date": build_date,
        "corpus_size": len(cur),
        "bootstrap": bootstrap,
        "new": new_l,
        "modified": mod_l,
        "removed": rem_l,
    }
    return ledger, run_line


# ============================================================================
# I/O
# ============================================================================

def load_ledger(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    ap = argparse.ArgumentParser(description="Build Minerva run-history artifact.")
    ap.add_argument("--dry-run", action="store_true",
                    help="compute and print the diff; write nothing.")
    ap.add_argument("--allow-mass-removal", action="store_true",
                    help="record a >50%% removal anyway (only if the corpus REALLY shrank).")
    args = ap.parse_args()

    if not STATE_FILE.is_file():
        print(f"ERROR: {STATE_FILE} not found", file=sys.stderr)
        return 1

    # Lazy imports: keep the module import-safe for unit tests.
    sys.path.insert(0, str(ROOT / "scripts"))
    from build_site import build_items  # noqa: E402

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    repos = state.get("repos", {})
    last_run = state.get("last_run", "")
    if not last_run:
        print("ERROR: state.json has no last_run — cannot date the artifact",
              file=sys.stderr)
        return 1

    items, _ = build_items(repos)
    prior = load_ledger(LEDGER_FILE)
    ledger, run_line = compute_history(prior, items, last_run)

    prior_live = sum(1 for e in prior.values() if not e.get("removed"))
    if is_mass_removal(prior_live, len(run_line["removed"])) and not args.allow_mass_removal:
        print(
            f"TRIPWIRE: {len(run_line['removed'])}/{prior_live} live repos would be "
            "tombstoned in one run (>50%) — presumed collection collapse; nothing "
            "written. Fix the cause and re-run (--allow-mass-removal only if the "
            "corpus really shrank).",
            file=sys.stderr,
        )
        return 2

    tag = "BOOTSTRAP baseline" if run_line["bootstrap"] else "incremental"
    print(f"History run ({tag}) — as of {run_line['build_date']}")
    print(f"  corpus_size : {run_line['corpus_size']}")
    print(f"  new         : {len(run_line['new'])}")
    print(f"  modified    : {len(run_line['modified'])}")
    print(f"  removed     : {len(run_line['removed'])} (kept as tombstones)")

    if args.dry_run:
        print("\n--dry-run: nothing written.")
        return 0

    LEDGER_FILE.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with HISTORY_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(run_line, ensure_ascii=False) + "\n")
    print(f"\nOK : {LEDGER_FILE.relative_to(ROOT)} ({len(ledger)} repos)")
    print(f"OK : {HISTORY_FILE.relative_to(ROOT)} (+1 run line)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
