# Roadmap

Honest, staged view: **MVP** (what already works), **V1** (the publishable public
release), **V2** (where it grows). Priorities favor publication credibility and
product value over feature count.

Legend: ✅ done · 🔜 remaining for this stage · 💡 idea (parked, not committed)

---

## MVP — the working engine ✅

The core discovery + curation + translation loop, already functional and tested:

- ✅ **Collect** from **Gitee (priority) + GitHub**, official APIs only, curated org
  list + seeds (Gitee search is broken server-side — documented workaround).
- ✅ **Score** each repo semantically across 4 domains; filter mirrors, forks,
  third-party ports and archived repos.
- ✅ **Translate/enrich** into structured **bilingual EN/FR fiches** (Problem
  solved, How it works, Chinese specificity, **Western equivalent**, Maturity),
  republishing only the minimal set + a link back to the source.
- ✅ **Present**: interactive dashboard (search/filter/listing), HTML + text
  newsletter, static site with per-fiche pages.
- ✅ **Incremental**: `state.json` diff (NEW/MODIFIED/DELETED); LLM only for changes.
- ✅ **Quality**: 96 tests + CI; offline `$0` rescoring.

## V1 — publishable public release 🔜

Making the MVP a credible, understandable, testable public project:

- ✅ Product docs: positioning, business, architecture.
- ✅ **Source compliance register** — [`data-sources-and-compliance.md`](data-sources-and-compliance.md)
  (per-source access/API/risk/decision, incl. candidate sources).
- ✅ Product-first README + honest architecture diagram; landing page + demo.
- ✅ **Confidence score** surfaced per fiche (data-quality signal, transparent).
- ✅ **Native bilingual pipeline** — `python src/pipeline.py` generates and
  maintains BOTH the EN and FR sets per run (one EN generation + one EN→FR prose
  translation per repo — same facts, zero drift; bootstrap requires both fiches,
  self-healing if either is missing; orphan cleanup covers both sets).
- 🔜 **Hosted freshness** — DECIDED (owner, 2026-07-31): weekly GitHub Actions
  cron (`.github/workflows/scheduled-run.yml`, inert until repo secrets exist).
  Cadence-follows-operator rule: "weekly" wording appears ONLY in builds produced
  by this workflow (`MINERVA_CADENCE=weekly` set there and nowhere else); default
  builds promise no cadence. Newsletter *send* stays manual until V1.1.
  Activates at public launch (secrets added post key-rotation).
- 🔜 **Real CI badge + repo metadata** (topics, description, social preview) on publish.

## V1.1 — the honest signal layer 🔜

Turning the validated landing + dashboard into a light **intelligence surface**
without simulating live. Static-first; every change signal is dated
("as of {last_run}") and data-backed. Full detail and rationale in
[`docs/UX_REDESIGN.md`](docs/UX_REDESIGN.md). Protected surfaces stay protected —
no rebrand, no surface proliferation, navigation unchanged.

**Foundation first — history artifact (before any signal UI):**

- 🔜 A committed, **machine-readable run artifact** (append-only) as the single
  source of truth for signal, briefings and rankings. It carries `first_seen`,
  `last_changed`, `last_run`, `modified_flag`, full `score` and a build date.
  The gitignored markdown diffs and last-run-only `state.json` cannot feed an
  honest signal layer — this artifact is the architectural lock.

**Then, in order:**

- 🔜 **Signal strip** on the dashboard (NEW / MODIFIED / DELETED for the last run)
  + "recently changed" sort + vendor/org facet in Explore, all reading the
  artifact, all stamped "as of {last_run}". No new top-level page.
- 🔜 **Fiches → dossiers** — related repos (domain/owner), confidence /
  Western-equivalent / Chinese-specificity foregrounded, source links. No user
  notes, no watchlist.
- 🔜 **Briefings** — a simple web brief from the *same* artifact as the newsletter
  (one run, one selection, no double truth).

**Honesty guardrails (non-negotiable):**

- `first_seen` bootstrapped as a build-date baseline (no "NEW" on day one).
- DELETED handled with a tombstone or brief-only mention, never a dangling badge.
- **Admission hysteresis BEFORE any signal UI** (hard precondition, 2026-07-31):
  admission breathes at the threshold (`bearpi-hm_nano` left the corpus with no
  real-world change). The signal layer must not report threshold noise as world
  movement — sticky admission (a repo needs to fall clearly below the bar to
  exit), a dead band around `min_score`, or an explicit "left threshold" label
  distinct from "removed". Without one of these, NEW/REMOVED is partly fiction.
- Vendor sections only for orgs with ≥ ~5 fiches; prefer a section over a new page.
- A fresh pipeline run right before the public push so "as of" is credible.

**Explicitly not in V1.1** (→ V2): relational map, multi-run timeline, persistent
watchlists, personal workspace, any "live"/"real-time" wording.

## V2 — growth 💡

V2 becomes legitimate only once two things exist for real: **regular hosted runs**
and an **accumulated history**. The V1.1 history artifact is the seed that makes
these features true instead of cosmetic.

- **Structured data feed / API** — expose fiches as documented JSON.
- **New authorized sources** — GitLink/Trustie and GitCode (API-first, per the
  compliance register), widening coverage beyond Gitee/GitHub.
- **Dashboard language toggle** — EN/FR in one page.
- **Timeline view** — "what's new this week/month" (needs accumulated history).
- **Saved watchlists + alerts** — custom competitor/org watch, per-watchlist
  digests (backend-dependent).
- **Relational map** — repo↔repo / vendor clustering (embeddings-based), *only if*
  it answers a real question and the corpus is dense enough to be worth it.
- **Automatic newsletter delivery** — SMTP / Buttondown.
- **Auto-discovery** — propose new relevant orgs (forks of watched orgs, recurring
  contributors) as candidates.
- **Domain broadening** — extend beyond embedded/IoT/robotics/edge-AI *only after*
  the vertical is a proven product (keeps the V1 focus a strength, not a limit).
- **Confidence v2** — multi-factor score (source reliability × freshness ×
  enrichment depth × corroboration).

---

## Explicit TODOs (not finished yet)

- [x] **Corpus rebalancing** — DONE 2026-07-30 (admission v2: contrastive
      anti-domain filter + generalist keyword requirement + wedge keyword
      expansion; fresh pipeline run; see `docs/SCORING.md` and CHANGELOG 0.15.0).
      Per-org diagnosis result: the "zero-fiche orgs" were not fetch failures —
      **2,313/3,660 Gitee repos are stale >2 years** (OpenHarmony alone: 1,617;
      the ecosystem migrated toward AtomGit/GitCode, vendors publish on GitHub).
- [x] **GitHub org harvest** — DONE 2026-07-30. Authenticated harvest of the 5
      vendor orgs added **63 wedge-pure repos** (Unitree 31, Sophgo 24, Bouffalo 9,
      Kendryte 3), taking the corpus 43 → **106** and dropping big-tech share to
      **12%**. Robotics went 2 → 9.
- [ ] **AtomGit/GitCode connector (next coverage lever):** recover the OpenHarmony
      ecosystem and other vendors that left Gitee (candidates in the compliance
      register). This is now the main remaining corpus-growth path.
- [x] **History artifact (V1.1 foundation)** — *implemented AND bootstrapped 2026-07-31* (105 repos, baseline first_seen, first history.jsonl line, bootstrap:true).
      `scripts/build_history.py` writes a committed `output/repo_ledger.json`
      (durable per-repo: `first_seen`, `last_changed`, `removed` tombstone, score,
      domaine, confidence, stars, `pushed_at`, source) and appends
      `output/history.jsonl` (one line per run). Pure core unit-tested (+5, 110
      total). **To be bootstrapped by the fresh launch run** so the baseline isn't
      wasted — must precede any signal UI. Schema: `docs/HISTORY_ARTIFACT.md`;
      deploy rules: `docs/DEPLOYMENT.md`.
- [ ] Stand up a scheduled/hosted run for a permanently-fresh public demo
      (the corpus is a static snapshot dated by `state.json` last_run until the
      next run). This is the bridge that unlocks the V2 living console.
- [x] `scripts/rescore.py` — DONE 2026-07-31: now syncs the FR twin with the same
      score/domain (plus fixed a latent raw-domain-name corruption bug; localized
      per fiche language).
- [x] `state.json["scores"]` — normalized 2026-07-31 (fresh run + rescore pass;
      105 uniform entries).
- [ ] Add a real GitHub Actions status badge once the repo slug exists.
- [ ] Evaluate GitLink/Trustie API for a third integrated source (see register).
- [ ] Optional: JSON export endpoint/schema for the data feed.

## Known limitations (kept honest)

- Gitee `/search/repositories` is broken server-side → curated org list + seeds.
- A full multi-org GitHub run needs a `GITHUB_TOKEN` (anonymous = 60 req/h).
- LLM enrichment can be imperfect → "to be confirmed" convention + source link.
- Coverage is intentionally narrow (embedded/IoT/robotics/edge-AI) — a V1
  positioning choice, broadening is a V2 option.
