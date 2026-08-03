"""Tests for scripts/build_history.compute_history — the Track 2 history foundation.

Pure-function tests on synthetic data only: they never read state.json, never touch
output/, and never generate the real ledger/history (that must wait for the fresh
launch run). They pin the two encoded honesty guardrails (bootstrap first_seen,
DELETED tombstone) plus new/modified detection and first_seen preservation.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_history import compute_history  # noqa: E402


def _item(full_name, pushed_at, score=50, source_url="https://gitee.com/x"):
    return {
        "full_name": full_name,
        "pushed_at": pushed_at,
        "score": score,
        "domaine_primary": "Embedded",
        "confidence": "High",
        "stars": 100,
        "date": pushed_at[:7],
        "gitee_url": source_url,
    }


def test_bootstrap_claims_no_new():
    """Guardrail 1: first run sets first_seen=build_date as baseline, new=[]."""
    items = [_item("a/one", "2026-07-30T00:00:00+00:00"),
             _item("b/two", "2026-07-30T00:00:00+00:00")]
    ledger, run = compute_history({}, items, "2026-07-30T10:00:00+00:00")

    assert run["bootstrap"] is True
    assert run["new"] == [] and run["modified"] == [] and run["removed"] == []
    assert run["corpus_size"] == 2
    assert ledger["a/one"]["first_seen"] == "2026-07-30"
    assert ledger["a/one"]["last_changed"] == "2026-07-30"
    assert ledger["a/one"]["removed"] is None


def test_incremental_new_modified_unchanged():
    prior = {
        "a/one": {"first_seen": "2026-07-01", "last_changed": "2026-07-01",
                  "removed": None, "pushed_at": "2026-06-01T00:00:00+00:00"},
        "b/two": {"first_seen": "2026-07-01", "last_changed": "2026-07-01",
                  "removed": None, "pushed_at": "2026-06-01T00:00:00+00:00"},
    }
    items = [
        _item("a/one", "2026-06-01T00:00:00+00:00"),          # unchanged pushed_at
        _item("b/two", "2026-07-15T00:00:00+00:00"),          # modified
        _item("c/three", "2026-07-20T00:00:00+00:00"),        # new
    ]
    ledger, run = compute_history(prior, items, "2026-07-30T10:00:00+00:00")

    assert run["bootstrap"] is False
    assert run["new"] == ["c/three"]
    assert run["modified"] == ["b/two"]
    assert run["removed"] == []
    # unchanged repo keeps its old last_changed; new/modified stamp build_date
    assert ledger["a/one"]["last_changed"] == "2026-07-01"
    assert ledger["b/two"]["last_changed"] == "2026-07-30"
    assert ledger["c/three"]["first_seen"] == "2026-07-30"
    # first_seen is preserved across runs for pre-existing repos
    assert ledger["a/one"]["first_seen"] == "2026-07-01"


def test_removed_becomes_tombstone_not_dropped():
    """Guardrail 2: a removed repo is kept with a `removed` date, never deleted."""
    prior = {
        "a/one": {"first_seen": "2026-07-01", "last_changed": "2026-07-01",
                  "removed": None, "pushed_at": "2026-06-01T00:00:00+00:00"},
        "gone/repo": {"first_seen": "2026-07-01", "last_changed": "2026-07-01",
                      "removed": None, "pushed_at": "2026-06-01T00:00:00+00:00"},
    }
    items = [_item("a/one", "2026-06-01T00:00:00+00:00")]
    ledger, run = compute_history(prior, items, "2026-07-30T10:00:00+00:00")

    assert run["removed"] == ["gone/repo"]
    assert "gone/repo" in ledger                       # not dropped
    assert ledger["gone/repo"]["removed"] == "2026-07-30"  # tombstoned
    # a tombstoned repo is excluded from the live set on the next run
    ledger2, run2 = compute_history(ledger, items, "2026-08-06T10:00:00+00:00")
    assert "gone/repo" not in run2["removed"]           # already tombstoned, not re-removed


def test_returning_repo_keeps_first_seen_clears_tombstone():
    prior = {
        "back/repo": {"first_seen": "2026-05-01", "last_changed": "2026-06-01",
                      "removed": "2026-07-01", "pushed_at": "2026-06-01T00:00:00+00:00"},
    }
    items = [_item("back/repo", "2026-07-25T00:00:00+00:00")]
    ledger, run = compute_history(prior, items, "2026-07-30T10:00:00+00:00")

    assert run["new"] == ["back/repo"]                  # reappears as new in the run line
    assert ledger["back/repo"]["removed"] is None        # tombstone cleared
    assert ledger["back/repo"]["first_seen"] == "2026-05-01"  # original first_seen kept


def test_source_detection_github_vs_gitee():
    items = [
        _item("gh/repo", "2026-07-30T00:00:00+00:00", source_url="https://github.com/gh/repo"),
        _item("ge/repo", "2026-07-30T00:00:00+00:00", source_url="https://gitee.com/ge/repo"),
    ]
    ledger, _ = compute_history({}, items, "2026-07-30T10:00:00+00:00")
    assert ledger["gh/repo"]["source"] == "github"
    assert ledger["ge/repo"]["source"] == "gitee"
