# Night worklog — product hardening

> Running log of decisions taken during the autonomous product-hardening pass.
> Goal: make Minerva measurably more **publishable, credible, demonstrable and
> sellable** by tomorrow morning — **without changing its DNA** (Chinese
> open-source tech watch over Gitee + GitHub, semantic scoring, bilingual fiches,
> dashboard, newsletter, incremental pipeline).
>
> Format per entry: **What / Why / Impact / Open**.

## Guardrails I held myself to

- No redefinition of the project; no new risky data sources; no scope creep into
  verticals we don't control.
- Every change tested against: *"Does this make Minerva more understandable,
  credible, demonstrable and sellable tomorrow — without breaking its identity?"*
- Prefer publishable V1 clarity over impressive-but-fragile machinery.
- Preserve the passing test suite and the working pipeline throughout.

## Priority order followed

1. Preserve DNA & invariants.
2. Clarify the value proposition.
3. Make the demo more desirable & credible.
4. Strengthen assets useful for future monetization / resale.
5. Only then, secondary technical polish.

---

## Entries

### 0. Baseline captured
- **What:** Surveyed repo. Apache-2.0, 78 passing tests, English-default bilingual
  output already in place (README/CHANGELOG bilingual, 176 EN + 176 FR fiches,
  dashboard/newsletter/site in English). No `docs/`, no `ROADMAP`, no `CONTRIBUTING`.
- **Why:** Know exactly what exists before adding, to avoid reinvention.
- **Impact:** Confirmed the work is *packaging & positioning*, not rebuilding.
- **Open:** Old newsletters and demo artifacts could be tidied.

### 1. Product docs suite (`docs/`)
- **What:** Added [POSITIONING](POSITIONING.md), [BUSINESS](BUSINESS.md),
  [SOURCES](SOURCES.md), [ARCHITECTURE](ARCHITECTURE.md); plus top-level
  [ROADMAP](../ROADMAP.md) and [CONTRIBUTING](../CONTRIBUTING.md).
- **Why:** A buyer/partner/technical evaluator can't judge value from code alone.
  These make the market, the money logic, the data provenance and the design
  legible in minutes — the assets that make a project *sellable*, not just usable.
- **Impact:** Turns "a repo" into "a product with a thesis". SOURCES.md in
  particular removes the #1 B2B objection (data provenance/compliance).
- **Open:** Pricing in BUSINESS.md is a thesis aligned to the existing Pro page,
  not a committed plan.

### 2. Value-proposition clarity
- **What:** One-line value prop ("decision-ready intelligence, not a repo list";
  Western-equivalent mapping as the bridge) defined in POSITIONING and threaded
  through README, README.fr and the dashboard hero.
- **Why:** Priority #2. A visitor must grasp *who it's for* and *why it matters* in
  10 seconds. The old README led with mechanics; buyers lead with value.
- **Impact:** Consistent, differentiated framing across every surface.
- **Open:** Could add a short demo GIF/screenshot once a render surface is available.

### 3. README reframed product-first
- **What:** New README: value prop + honest architecture diagram
  (`docs/assets/pipeline.svg`) + "Who it's for" + use cases + "What you get" +
  docs index + badges — technical depth preserved below the fold.
- **Why:** The README is the single highest-traffic asset for GitHub accroche.
- **Impact:** Reads as a product, not a script, without losing engineering credibility.
- **Open:** Badges are static (no repo slug yet); wire real CI badge on publish.

### 4. Demo credibility (dashboard)
- **What:** Sharpened the hero to the value prop (Gitee **and** GitHub;
  Western-equivalent mapping), added a footer **sources & method** trust line
  (official APIs, public metadata, links back, "to be confirmed" honesty).
- **Why:** The dashboard is the live demo; trust signals raise perceived
  credibility for a B2B/technical audience.
- **Impact:** Demo now states its provenance and honesty posture on the page.
- **Open:** A live-hosted, always-fresh dashboard is the next credibility step (roadmap).

### 5. Repo hygiene
- **What:** Diagram asset under `docs/assets/`; `.gitignore` comments translated to
  English (English-default consistency); confirmed demo artifacts are tracked so
  the no-token demo works on a fresh clone.
- **Why:** A clean, coherent repo reads as maintained and trustworthy.
- **Impact:** Fewer rough edges for a first-time visitor.
- **Open:** Old per-date newsletters left in place (harmless history; not deleting
  artifacts I didn't create).

### 6. Publishable-V1 deliverables (per the explicit deliverables mandate)
- **What:** (a) Created [`data-sources-and-compliance.md`](../data-sources-and-compliance.md)
  — a per-source register (access method / API-vs-scraping / risks / decision) for
  Gitee, GitHub, Anthropic **and** candidate Chinese sources (GitCode, GitLink,
  AtomGit, vendor portals) with an explicit integration rule. (b) Restructured
  `ROADMAP.md` into **MVP / V1 / V2** with explicit TODOs. (c) Added a transparent
  **confidence score** (`fiche_schema.confidence_tier` + `Fiche.confidence`,
  surfaced as a dashboard badge, documented in [SCORING.md](SCORING.md)). (d)
  README status note + docs index + confidence in "What you get".
- **Why:** The mandate named these deliverables explicitly; most of the product
  already existed, so the job was to fill the *named* gaps and make the compliance
  story and the confidence signal first-class — the two things a discovery product
  is judged on (trust in sources, trust in each entry).
- **Impact:** Every requested V1 deliverable now maps to a concrete, tested asset.
  Confidence spread is real and honest (108 High / 68 Medium across 176 fiches),
  driven by enrichment depth + metadata + recency + unverified-flag.
- **Open:** Confidence is presentation-layer (not stored in the markdown, no fiche
  regeneration); a multi-factor "confidence v2" is parked in the roadmap. Candidate
  sources are documented but not integrated (deliberate — API/ToS review first).

### Reconciliation note (strategic, decided without interrupting)
- The mandate framed Minerva as a *general* Chinese-OSS discovery platform; the
  prior invariant kept it a *vertical* (embedded/IoT/robotics/edge-AI) product.
  **Decision:** keep the vertical as the V1 scope (it's a differentiation strength
  and the corpus is densest there), present the *architecture* as source- and
  domain-general, and list domain broadening as an explicit **V2** option. This
  honors both mandates without a risky scope explosion.

### 7. Response to the independent external audit (Grok, 2026-07-30)
- **What:** Independently re-verified every major claim of the external audit,
  then fixed all confirmed P1 "truth alignment" findings: stale test counts
  (→96), stale LLM cost (→$0.01/pair), false "updated this week" badge (→honest
  last-run date), obsolete anti-GitHub FAQ, Gitee-only landing wording, Phase-0
  artifact fiche, stale [MODIFIÉ] badges, README org-coverage honesty note, CI
  secret guard. Logged the structural findings (corpus skew 77% Alibaba+ByteDance,
  15/27 orgs at zero fiches, rescore EN-only drift, mixed scores schema) as
  explicit ROADMAP TODOs rather than hiding them.
- **Verification notes:** audit was accurate overall; two calibrations — zero-fiche
  orgs are 15/27 (worse than the audit's 13/22), hollow "Chinese specificity" is
  57/176 EN fiches (~32%, audit said ~45%). Confirmed 0 secrets in deliverable
  artifacts.
- **Why:** An external audit is only valuable if its findings are verified, then
  either fixed or explicitly owned. Truth-alignment items were cheap and
  publication-blocking; corpus rebalancing is a strategic scope/cost decision left
  to the owner (documented in ROADMAP).
- **Open:** P0 secrets rotation is a user action (keys live in the local `.env`);
  P2 corpus rebalancing + fresh pipeline run awaits a product decision.

### 8. Corpus recalibration — admission v2 (option 2, approved by owner)
- **What:** Tightened admission (contrastive anti-domains for keyword-less repos
  + mandatory curated keyword for generalist orgs), expanded/pruned the keyword
  lists, fixed keyword matching for `_`-separated names, made GitHub seeds
  override stale same-slug mirrors. Fresh full run (3,660 repos). Corpus:
  176 → 43 fiches, big-tech 77% → 30%, 15 owners, all 4 GitHub vendor seeds in.
- **Calibration journey (5 runs, deliberately iterative):** run 1 over-cut to 40
  (killed MNN/PaddleOCR/seeds) → measured gaps on a live 12-repo set → learned
  the noise enters keyword-less via the semantic path → inverted the rule
  (keyword mandatory for generalists, contrastive only for keyword-less) → runs
  3–4 exposed two more real bugs (`sdk`/`control`/`motion`/`量化` keyword noise;
  stale Gitee mirrors shadowing GitHub seeds) → run 5 froze at 43. Every
  adjustment was driven by a measured false positive/negative, not taste.
- **Structural discovery:** 2,313/3,660 watched Gitee repos are stale >2 years
  (OpenHarmony alone 1,617 — the ecosystem moved to AtomGit/GitCode; vendors are
  on GitHub). The audit's "zero-fiche orgs" were dead mirrors, not fetch bugs.
  Gitee alone no longer carries the fresh wedge supply → coverage path is the
  GitHub harvest (token) + AtomGit/GitCode connector (register priorities raised).
- **Impact:** The corpus now visibly matches the pitch (Embedded 23 + Edge AI 20
  of 43; vendors at the center). Smaller but honest — quality-over-quantity is
  the recalibration's explicit trade.
- **Open:** ~2 borderline admits remain (alibaba/collabobot via a literal "robot"
  description, alibaba-rsocket-broker via a literal IoT claim) — documented,
  acceptable. GitHub org harvest still needs a token. `rescore.py` FR-drift TODO
  unchanged.

### 9. Security hardening (priority #1 after recalibration validated)
- **What:** Full secret sweep (keys only in gitignored `.env`, nowhere in logs or
  artifacts); hardened `.gitignore` (all `.env.*` + secret shapes, verified by
  git simulation); added `.env.example`, `scripts/secret_scan.py` (local + CI,
  self-tested), `SECURITY.md` with a required pre-first-push checklist.
- **Why:** The one publication-blocking item from the external audit. Making leak
  prevention mechanical (scan + CI guard) matters more than a one-time cleanup.
- **Boundary held:** key **rotation is a user action** — I cannot (and must not)
  revoke/regenerate the user's Gitee/Anthropic keys; SECURITY.md flags it as
  step 1 before any public push.
- **Open:** user must rotate dev keys + add a least-privilege `GITHUB_TOKEN`.

### 10. GitHub harvest (priority #2)
- **What:** Reconnaissance first (enumerate 5 orgs = 221 repos, apply v2 admission
  locally, no LLM): **67 wedge-pure repos** would be admitted (Unitree 31,
  Sophgo 24, Bouffalo 9, Kendryte 3) — corpus 43 → ~106, filling Robotics.
  Launched the full harvest in background (anonymous GitHub, ~1-1.5h throttled;
  incremental protects the 43 Gitee fiches; ~$0.67 LLM).
- **Why:** Explicitly the #2 priority; non-destructive; the recon proved it's
  high-value and on-wedge before spending anything.
- **Open:** a read-only `GITHUB_TOKEN` would cut the run from ~1.5h to ~5 min;
  offered as an acceleration, not a blocker.

### 11. Pre-launch arbitrations (owner, 2026-07-31) — the four blockers

Following a full independent project audit, the owner arbitrated the four
launch-blocking subjects before any push:

1. **Weekly run operator → scheduled GitHub Actions CI** ("hosted freshness").
   `.github/workflows/scheduled-run.yml`: Monday cron, explicit guard that
   no-ops green until repo secrets exist (inert pre-launch), pipeline →
   build_history → rebuild → secret-scan → tests → auto-commit. The newsletter
   SEND stays a manual owner gesture.
2. **Newsletter → owner-controlled Buttondown account + manual send.**
   Blocking fix shipped: `MINERVA_NEWSLETTER` now has NO default — unset handle
   renders a **disabled** form ("Email sign-up opens at launch") instead of a
   live form posting to an unowned account. Same degrade philosophy as the URL
   placeholder; asymmetry closed.
3. **Editorial promise → "weekly" kept, backed by the CI.** Standing owner
   commitment: the *send* remains manual until V1.1 automation.
4. **Public scoring → reformulate + curate the vitrine; formula stays frozen.**
   Hero slots (Featured / Runners-up / landing proof) only front decision-rich
   fiches — utility repos (docs/download-data/toolchain/helper-tools, e.g.
   `esp-gitee-tools` which ranked #4) stay in the corpus and explorer but no
   longer carry the proof. Displayed ranks remain TRUE corpus ranks (no cosmetic
   renumbering). Score/confidence legend added (fiche pages + dashboard
   tooltips). Real formula rework = V1.1 backlog, calibrated on the fresh-run
   corpus.

**Visible-trust fixes shipped in the same pass:** `legal.html` (privacy,
provenance, maintainer corrections/removals, licensing, contact) linked from
every footer; false "EU-hosted" claim corrected (Buttondown is US-based);
**106 FR fiche twin pages** (`f/<slug>.fr.html`, localized decision surface,
hreflang pairs, EN↔FR toggle) making the "EN + FR" trust-line verifiable;
score legend; stale figures purged (dashboard: "$0.005/fiche"→"$0.01/pair",
"weekly incremental execution" removed, "140 fiches" corpus figure, keyword-era
scoring description → semantic+admission); watched-orgs conflation fixed
(27 watched vs 15 with fiches, computed from config); Pro page de-dated
("Launching Q3 2026" → "when it's ready", roadmap Now/Next/Later/Exploring);
dashboard toolbar sticky-under-nav bug fixed; OG fiche-count parametrized.

### 12. Stop-ship doctrine + cadence-follows-operator + utility demotion (owner, 2026-07-31)

Owner reframed the pre-launch phase around a single objective: **make the vitrine
worthy of the doctrine** — growth topics wait. Stop-ship while any of four
honesty betrayals exists (unbacked time promise, uncontrolled email capture,
false/fuzzy numeric claims, absurd public ranking). Three decisions sharpened
beyond §11:

- **Cadence follows the REAL operator, structurally.** Default builds promise no
  cadence anywhere ("after each corpus run", EN+FR); the word "weekly" is
  produced ONLY by the weekly CI workflow itself via `MINERVA_CADENCE=weekly` in
  its rebuild step. A local/manual build cannot over-promise by construction.
  This reconciles arbitration §11-1/3 (CI + weekly kept) with the doctrine "never
  narrate a habit that doesn't exist yet": the launch build says "as of / per
  run"; the weekly wording appears exactly when the weekly operator takes over.
- **Score formula re-opened, minimally**: `UTILITY_PENALTY = 25` in
  `analyzer.score_repo` for repos matching `docs$|download|toolchain|tools$` —
  demotion, not exclusion (a submodule installer must never outrank an inference
  framework). Applied by the fresh run (no intermediate rescore — avoids the
  known `rescore.py` FR-drift). +3 penalty-isolated tests (113 total). Manual
  top-10 sanity check after the fresh run is a pre-push review step.
- **Paid tiers requalified as "Planned scope"**: removed "guaranteed",
  "10k req/month", "99.5% SLA" and "Daily newsletter" as stated facts; Pro and
  Enterprise feature lists explicitly labeled planned/subject-to-change; the
  −30% waitlist pledge kept as a pledge, not a guarantee.

Definition of "ready to publish" (7 checkboxes) recorded in `docs/DEPLOYMENT.md`
§6. Explicitly deferred by the owner: wedge repositioning, console/map/timeline,
Pro build-out, re-opening the visual direction, AtomGit/GitCode, retention
machinery.

### 13. Launch-run QA — laugh test GO (owner, 2026-07-31)

Owner cross-checked the fresh-run report on disk (dashboard vitrine, state.json,
forms) and returned a **binary GO on the laugh test**: post-demote top-10 is
credible for a hardware person (noted nuance, not a stop: double 100 and esp-at
at 84 are fine-calibration debates, not ridicule). §6 grid: all boxes checked on
the public surface — email box held by forms-off; ranking box checked under this
GO. Verdict: **surface push authorized under forms-off** (or real Buttondown),
with one standing condition: `MINERVA_CADENCE=weekly` must never be activated
before the first genuinely successful CI cycle. Key rotation / domain remain
owner prerequisites for the hosted machine. `scripts/collect_public.py` built
and verified (218-file allowlist, zero internals) so the deploy manifest is now
executable, not just written.

## What I deliberately did NOT do (scope discipline)

- Did not add new data sources or verticals, or touch the pipeline invariants.
- Did not build a hosted backend / API / auth this pass — noted in the roadmap as
  the next monetization step rather than half-built tonight.
- Did not fabricate a screenshot (would hurt credibility); used an honest diagram.
- Did not redefine positioning — only sharpened and documented the existing one.
