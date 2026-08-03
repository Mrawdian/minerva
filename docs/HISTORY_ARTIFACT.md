# History artifact — the Track 2 foundation

> The architectural lock that makes "what changed / where's the signal" **true**
> instead of a UI illusion. It must exist **before** any signal layer, and be
> produced by the **fresh launch run** so it starts accumulating from day one.
> Status: **design, awaiting owner sign-off on the schema** (no generator wired yet).

## Why it exists

Today the pipeline emits a per-run `output/diff_*.md` (git-ignored, markdown,
unreadable by the static site) and a `state.json` that keeps only the *last*
`pushed_at`/score. Neither can honestly feed a signal strip, briefings or
rankings. The history artifact is a **committed, machine-readable memory of runs**
— the single source of truth all three read from.

## Two files (both committed — unlike `diff_*.md`)

### 1. `output/repo_ledger.json` — durable per-repo state

The current truth per repo, carried across runs.

```json
{
  "sophgo/tpu-mlir": {
    "first_seen":  "2026-07-30",
    "last_changed":"2026-07-30",
    "removed":     null,
    "score":       97,
    "domaine":     "Edge AI",
    "confidence":  "High",
    "stars":       412,
    "pushed_at":   "2026-07",
    "source":      "github"
  }
}
```

- `first_seen` — first run this repo entered the corpus (drives an honest **NEW**).
- `last_changed` — last run it was flagged MODIFIED (drives **recently-changed** sort).
- `removed` — `null` while live; a date string once it drops out (tombstone, see below).

### 2. `output/history.jsonl` — append-only, one line per run

```json
{"run":"2026-07-30T10:08:58+00:00","build_date":"2026-07-30","corpus_size":106,"bootstrap":true,"new":[],"modified":[],"removed":[]}
{"run":"2026-08-06T09:00:00+00:00","build_date":"2026-08-06","corpus_size":109,"bootstrap":false,"new":["sophgo/foo","unitreerobotics/bar"],"modified":["rtthread/rt-thread"],"removed":["kendryte/old-sdk"]}
```

- The **last line** = "current run": feeds the signal strip ("as of {build_date}",
  NEW/MODIFIED/REMOVED) and the briefing selection.
- The **whole file** = history: feeds V2 timelines / momentum. Small (~a few hundred
  bytes/run), safe to commit indefinitely.

## Producer

A single step at the **end of a pipeline run** (standalone `scripts/build_history.py`,
or a `pipeline.py` post-step): diff the fresh `state.json` against the previous
`repo_ledger.json`, then

1. compute `new` / `modified` / `removed`,
2. update the ledger (`first_seen` for genuinely-new repos; `last_changed` for
   modified; a `removed` date for those that left),
3. append one run line to `history.jsonl`.

It reuses the pipeline's existing NEW/MODIFIED/DELETED logic — no new detection,
just persistence.

## Consumers (later phases, not now)

| Consumer | Reads | Produces |
|---|---|---|
| Signal strip (Phase 3) | last `history.jsonl` line + ledger | NEW/MODIFIED/REMOVED "as of {build_date}" |
| Recently-changed sort | ledger `last_changed` | Explore ordering / facet |
| Briefings (Phase 5) | **same** last line + ledger | web brief + newsletter (one source of truth) |
| V2 timeline / momentum | full `history.jsonl` | trends over runs |

## The four honesty guardrails, encoded here

1. **`first_seen` bootstrapped.** On the very first run (no prior ledger), every
   current repo gets `first_seen = build_date` as a **baseline** and the run line is
   marked `"bootstrap": true` with `new: []`. **No NEW badge is emitted on day one.**
   From the next run on, a repo absent from the ledger is genuinely new.
2. **DELETED handled cleanly.** A removed repo is **kept in the ledger** with a
   `removed` date (tombstone), not dropped. The signal layer may show a light "X
   removed at run Y" or mention it in the brief only — never a dangling badge.
3. **Vendor mass** is a consumer-side rule (≥ ~5 fiches), unaffected by the schema,
   but the ledger's per-owner counts make the gate trivial to enforce.
4. **Fresh run before launch.** The bootstrap line must be produced by the **fresh
   launch run**, so the first public "as of {build_date}" is genuinely recent.

## Where it slots into the launch sequence

```
Track 1 hygiene  ✅ (done, local)
   → wire build_history.py                 (implement on owner go)
   → FRESH launch run                       (produces bootstrap ledger + first line)
   → review
   → public push
   → Phase 3 signal strip reads the artifact (first real "what changed")
```

The generator is wired **before** the fresh run; it is **not** run now, because
bootstrapping on the current (soon-to-be-superseded) snapshot would waste the
baseline. No signal UI ships until at least one non-bootstrap run exists.

## Open decision for the owner

- **Schema sign-off** — the two files and fields above.
- **Producer placement** — standalone `scripts/build_history.py` (my recommendation:
  non-invasive, independently testable) vs a `pipeline.py` post-step.
- **Commit policy** — both files committed (recommended; they are the durable
  memory). `diff_*.md` stays git-ignored.
