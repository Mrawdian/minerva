# Changelog
**Language:** 🇬🇧 English · [Français](CHANGELOG.fr.md)

All notable changes to the Minerva project are recorded here.
Format inspired by [Keep a Changelog](https://keepachangelog.com/).

## [0.25.2] — 2026-08-03

### Fixed — Collection-collapse tripwire (post-mortem of the first CI cycle)

The first scheduled cycle ran with corrupted secrets (values pasted with a
trailing newline → HTTP 401 on every Gitee AND GitHub call). Every owner
"enumerated" empty, and the pipeline concluded the whole corpus had vanished:
**105/105 repos marked deleted**, state wiped, 105 tombstones recorded. Nothing
reached the public repo/site only because the rebuild step happened to crash on
the empty corpus — an accidental firewall, not a designed one. Now designed:

- **Fetchers (Gitee + GitHub)**: a hard error on page 1 with zero repos
  collected (401/403/5xx/network) now raises the pagination error so the owner
  joins `failed_owners` and its repos are protected from false deletion —
  previously it returned an empty list ("normal behavior"). 404 and genuinely
  empty accounts unchanged.
- **Pipeline tripwire**: if >50% of tracked repos would be deleted in one run
  (corpus ≥10), abort with `CollectionCollapseError` (exit 2) — state, fiches
  and diff untouched. A mass deletion is a collection failure until proven
  otherwise.
- **`build_history` mirror guard**: refuses to tombstone >50% of the live
  ledger (`--allow-mass-removal` to override deliberately) — the history
  artifact must never record a failure as signal.
- +5 tests (**118** total). The admission-hysteresis lesson (bearpi) arrived at
  maximum scale on cycle #1 — and is now mechanized at all three layers.

## [0.25.1] — 2026-07-31

### Changed — Precision-aesthetic softening (owner verdict, point 2)

The calm-instrument frame implied measurement precision the score doesn't have.
Softened without a redesign: dropped the solemn "top N% of corpus" from the fiche
readout (EN+FR); legend rewritten to plain truth — "a coarse triage signal …
a sort key, not a measurement of the ecosystem"; dashboard tooltip aligned;
"most relevant" → "highest-scored" (a score fact, not a world claim).
`docs/SCORING.md` gains an **Honest limits** section stating the two structural
caveats plainly: score provenance is partly circular today (rescore embeds the
fiche's own LLM prose — source-first rescore is the planned fix) and admission
breathes at the threshold (bearpi case). ROADMAP V1.1 guardrails gain a hard
precondition: **admission hysteresis before any signal UI** (sticky admission,
dead band, or explicit "left threshold" labeling). 113 tests; publish/ rebuilt.

## [0.25.0] — 2026-07-31

### Added / Fixed — Fresh launch run + history bootstrap + corpus-wide demotion

- **Fresh pipeline run** (3,868 repos enumerated): 0 new, 6 modified pairs
  regenerated, 99 unchanged, corpus **106 → 105** — `bearpi/bearpi-hm_nano`
  fell below the admission threshold this run (borderline score, not a fetch
  deletion); its EN+FR fiches and pages cleaned/purged.
- **`rescore.py` fixed then applied corpus-wide**: (a) the known EN-only drift —
  the FR twin now receives the SAME score/domain as the EN scoring (101 FR
  synced); (b) a latent domain-corruption bug — it wrote RAW config domain
  names ("Embarqué") into fiches; now localized per fiche language via
  `_translate_domain`. 99 scores + 41 domain labels updated, 0 parse errors,
  `state.json["scores"]` normalized (105 entries — closes the mixed-schema TODO).
- **Utility demotion is live in the corpus**: `esp-gitee-tools` #4 → **#92**
  (86 → 52); all 7 utility repos now rank #92–#105. New explorer top-10 is
  fully decision-grade (rt-thread, ESP8266_RTOS_SDK, unitree_ros, esp-idf,
  ncnn, xr_teleoperate, esp-at, nncase, LuatOS, esp-iot-solution).
- **History artifact bootstrapped** (dry-run then real): `repo_ledger.json`
  (105 repos, `first_seen` = 2026-07-31 baseline) + first `history.jsonl` line
  (`bootstrap: true`, no NEW claimed — guardrail 1 honored).
- Domain rebalance from prose-based rescoring: primary domains now
  Embedded 59 / Edge AI 23 / Robotics 17 / IoT 6 (landing numbers are computed
  from data at build time, so the page follows automatically).
- **`scripts/collect_public.py`** — the deploy manifest made executable: an
  allowlist copy `output/` → `publish/` (git-ignored) + `--check` mode; verified
  218 files, zero internals. Deploy `publish/`, never `output/`.
- Rebuilt dashboard/site/newsletter on the 105-corpus ("as of 2026-07-31");
  forms still disabled (no handle); 113 tests green.

## [0.24.0] — 2026-07-31

### Changed — Stop-ship doctrine: cadence follows the operator; utility demotion

Owner doctrine sharpened (`docs/DECISIONS.md` §12): no push while any honesty
betrayal exists; the vitrine must be worthy of the doctrine before growth topics.

- **Cadence-follows-operator, structurally.** Default builds promise NO cadence
  anywhere — landing/pro/fiches (EN+FR) say "after each corpus run"; the word
  "weekly" can only be produced by the weekly CI workflow itself
  (`MINERVA_CADENCE=weekly` set in its rebuild step, nowhere else). Verified in
  both modes: default build = 0 cadence claims in the chrome; CI-mode build =
  weekly wording present. A manual build cannot over-promise by construction.
- **Utility demotion in the score formula** (`analyzer.score_repo`):
  `UTILITY_PENALTY = 25` for repos matching `docs$|download|toolchain|tools$` —
  demotion, not exclusion; same pattern as the vitrine-curation rule. Takes
  effect at the fresh run (no intermediate rescore → avoids the known
  `rescore.py` FR-drift). Manual top-10 sanity check post-fresh-run added to the
  pre-push review. +3 penalty-isolated tests (**113** total).
- **Paid tiers requalified as "Planned scope — not built yet"**: removed
  "guaranteed", "REST API (read, 10k req/month)", "99.5% SLA", "Daily
  newsletter" as stated facts; −30% waitlist pledge kept as a pledge. FAQ
  aligned ("planned, not built yet").
- **Definition of "ready to publish"** (7 stop-ship checkboxes) recorded in
  `docs/DEPLOYMENT.md` §6.

## [0.23.0] — 2026-07-31

### Added / Fixed — Pre-launch arbitrations + visible-trust fixes (audit response)

Four owner arbitrations (logged in `docs/DECISIONS.md` §11), then the trust fixes:

- **Hosted freshness decided**: `.github/workflows/scheduled-run.yml` — weekly
  Monday cron (pipeline → history → rebuild → secret-scan → tests → auto-commit),
  with an explicit guard that no-ops green until repo secrets exist, so the file
  is inert pre-launch. Newsletter *send* stays a manual owner gesture.
- **Buttondown placeholder now degrades**: `MINERVA_NEWSLETTER` has no default;
  unset ⇒ all email forms render disabled ("sign-up opens at launch") + a build
  blocker warning — a live form posting to an unowned account would leak
  visitors' emails. Asymmetry with the URL placeholder closed.
- **Vitrine curation (scoring reformulated, formula frozen)**: Featured /
  Runners-up / landing proof only front decision-rich fiches; utility repos
  (docs/download/toolchain/tools — e.g. `esp-gitee-tools`, previously #4) stay
  in corpus/explorer but no longer carry the proof. Displayed ranks remain true
  corpus ranks. Score/confidence **legend** added (fiche pages + dashboard
  tooltips). Formula rework → V1.1 backlog.
- **`legal.html`** — privacy (static site, no cookies/analytics; email only via
  deliberate Buttondown subscribe), content provenance & LLM disclosure,
  maintainer corrections/removals policy, licensing, contact. Linked from every
  footer. False "EU-hosted" FAQ claim corrected (Buttondown is US-based).
- **106 FR fiche twin pages** — `f/<slug>.fr.html` with localized decision
  surface (headings, labels, legend, aside), `lang="fr"`, hreflang pairs (real
  domain only), EN↔FR toggle in the breadcrumb. The "EN + FR" trust-line is now
  verifiable on the site. Purge + sitemap cover both languages.
- **Stale-figure sweep (dashboard)**: "$0.005/fiche" → "$0.01 per bilingual
  pair"; "weekly incremental execution" → "incremental by design — every run is
  dated"; "~$2 (140 fiches)" → "~$1 (106 bilingual pairs)"; unverified
  "~3 100 lines" dropped; keyword-era scoring description → semantic embeddings
  + admission v2. **Watched-orgs conflation fixed** (27 watched from config vs
  15 currently yielding fiches) on landing + dashboard.
- **Pro page de-dated**: "Launching Q3 2026" (about to be false on its face) →
  "launch when it's ready"; roadmap Now/Next/Later/Exploring. −30% waitlist
  pledge kept (a choice, not a date).
- **Dashboard toolbar sticky-under-nav bug fixed** (`top: 48px`); OG card
  fiche-count parametrized (`__OG_N__`).
- Verified: 110/110 tests; dashboard `<script>` code byte-identical (only the
  injected `RUNNER_NAMES` data constant changed — the intended curation effect);
  0 stale claims left in built pages. Nothing pushed; no fresh run.
- **Proof-review catch**: the dashboard footer (separate template) had no
  `legal.html` link — added. Every built page now links Legal & privacy.

## [0.22.0] — 2026-07-31

### Changed — D5 corrective design pass: instrument, not template

Two independent audits (Grok, Lovable) converged: structure/UX solid, but the
rendered surface read as a generic "premium template", not a "calm analytical
instrument". Verified in code: default system-font stack, 5–8px "friendly SaaS"
radii, and a near-invisible decorative grid. Corrective decision — one coherent
pass, not a redesign — validated on a single reference surface
(`docs/design/fiche-d5.html`) then propagated landing → dashboard → pro.

- **New bounded `--slab` register** (`#1B1E20` bg / `#F5F6F4` fg) for exactly two
  structural surfaces per page: a shared **status-line** band under nav (brand +
  "Snapshot · as of {date}" + fiche count) and, where fiche data exists, **one**
  readout panel (score/confidence/domain) reordered **before** the human-readable
  title. Guardrail enforced: 1 readout max per surface, 0 on Pro (no fiche data),
  and the dashboard's Explorer deliberately stays on the light register — 106 rows
  re-rendering per keystroke would make a slab flip there feel like overload.
- **Flattened radius scale** (`--r-0`/`--r-sm`/`--r-pill` replacing the ad hoc
  2–8px values) across every container on landing/dashboard/fiche/pro — the
  single highest-leverage fix for the "generic SaaS card" look.
- **Typographic rule narrowed** (owner decision mid-pass): mono is scoped to
  status-line / wordmark / score / metrics / labels / section markers / IDs only.
  Editorial H1/H2 stay **sans**, firmer (weight 700, tracking −0.03em, tighter
  leading) — never mono by default. The fiche H1 staying mono is the identifier
  exception (an owner/repo id), not a precedent; analysis prose is untouched.
- **Contrast verified and one real issue fixed**: `--signal-on-slab` (`#5B948F`
  on `--slab`) computes to 4.93:1 (WCAG calc, AA pass). Found the readout's domain
  value was domain-hue text on slab at ≈3.78:1 (AA fail) — recolored to
  `--slab-ink`; domain identity is now carried only by the readout's left-edge
  tick.
- **Dashboard `<script>` block untouched** — diffed byte-for-byte against the
  pre-pass extract; identical. All interactivity (search/filter/sort/keyboard/
  presets) unaffected; the domain "dot" in the Explorer list became a calm CSS-
  only left tick (pure restyle of the existing element, no DOM/JS change).
- **Verified**: 110/110 tests, dashboard JS `node --check` clean, 0 leftover dark
  tokens, 0 fake-live wording, guardrails confirmed on the real build output.
  Nothing pushed, no fresh run.

## [0.21.0] — 2026-07-31

### Changed — Design Track wired: "calm analytical instrument" visual system

- **Full re-skin wired into `build_site.py` and `build_dashboard.py`**, replacing
  the dark-startup-SaaS look (near-black + alarm-red + glow) with the validated
  light-first "calm analytical instrument" language (D1–D4, see
  `docs/DESIGN_TRACK.md`): technical paper + ink (`#F5F6F4`/`#1B1E20`), one mineral
  teal-slate signal accent (`#2F5A5C`, dried down from an initial `#0F766E`),
  monospace for every quantitative/identifier/label value, confidence rendered as
  ink diamond marks (◆◆◆/◆◆◇/◆◇◇) instead of a colored dot, flat hairline
  components (no floating shadows), a near-subliminal background grid.
- **Landing / Pro / Fiche** (`build_site.py`): shared `BASE_CSS` + chrome (nav,
  footer, tag/conf/score/form atoms) factored once; numbered mono section labels
  (`01 · …`); fiche's Western-equivalent block stays the highlighted reading hero
  in the humanist sans (mono is reserved for identifiers/metrics/labels — owner
  vigilance rule from D3, binding at wiring); `<link rel="icon">` + `og:image` meta
  wired (og:image only emitted with a real `MINERVA_SITE_URL`, matching the
  existing placeholder-degradation rule).
- **Dashboard** (`build_dashboard.py`): Hero, Featured, Landscape charts,
  Runners-up, 2-pane Explorer and Pipeline sections re-skinned to the same system.
  **All interactivity is byte-for-byte unchanged** — search, domain chips, account/
  type/maturity selects, sort, presets, reset, `/` focus, Escape, ↑/↓ keyboard nav
  are untouched; only presentation moved. Added a `confMarks()` JS helper (mirrors
  the new Python `conf_dm()`) so confidence renders as ink marks in the row list and
  detail panel, consistent with every other surface.
- **Brand assets**: `favicon.svg` (register/aperture mark + mineral tick, reads on
  light or dark tabs) and `og.svg` (1200×630 social card: mark + wordmark, mono stat
  row, the Western-equivalent bridge as the signal moment) now shipped by
  `build_site.py` into `output/`.
- **Verified**: 110/110 tests green (no data-layer change — `build_items`,
  `compute_aggregates`, confidence tier, sitemap/robots/placeholder-degradation
  logic all untouched); dashboard inline JS re-validated with `node --check`; full
  sweep confirms 0 leftover dark-theme tokens, 0 fake-"live" wording, 0
  `minerva.example` in any shipped file. **Nothing pushed, no fresh run** —
  `scripts/build_history.py` stays on hold per the standing checkpoint.
- **Open**: `output/og.svg` still needs rasterizing to `og.png` at deploy time (no
  rasterizer wired into the build); see `docs/DEPLOYMENT.md`.

## [0.20.0] — 2026-07-30

### Added — Track 2 history foundation (implemented, not run) + docs parity

- **`scripts/build_history.py`** — the committed run-history artifact generator: a
  pure `compute_history()` (bootstrap `first_seen` baseline, MODIFIED via
  `pushed_at` diff, DELETED **tombstones**, Gitee/GitHub source detection) + I/O
  that writes `output/repo_ledger.json` (durable per-repo state) and appends
  `output/history.jsonl` (one line per run). `--dry-run` supported. **Not executed
  yet** — it must be bootstrapped by the fresh launch run so the baseline is not
  wasted. Schema in `docs/HISTORY_ARTIFACT.md`.
- **Tests**: +5 (**110** total) — `tests/test_build_history.py` pins both honesty
  guardrails and new/modified/removed/return detection on synthetic data (no real
  artifact generated).
- **`docs/DEPLOYMENT.md`** — explicit V1 deploy manifest: the exact public web set
  (`index/dashboard/pro/f/sitemap/robots`), what must never ship (`state.json`,
  caches, logs, newsletters, raw fiches), the history-artifact exception (served
  only once the signal layer lands), and the two pre-push preconditions.
- **`CHANGELOG.fr.md` parity restored** — back-filled 0.11.0 → 0.19.0 (was 9
  versions behind); EN/FR changelogs now at full version parity.

## [0.19.0] — 2026-07-30

### Fixed — Track 1 publication hygiene + narrative coherence (local, nothing pushed)

- **Graceful placeholder degradation** (`build_site`): while `MINERVA_SITE_URL` is
  the `minerva.example` placeholder, the build now ships **no fake absolute URLs** —
  it omits `<link rel=canonical>`, `og:url`, all sitemap `<loc>` entries (empty
  commented `sitemap.xml`) and the robots `Sitemap:` line. Real domain re-enables
  them. `MINERVA_CONTACT` similarly degrades the Enterprise CTA to the newsletter.
- **No fake "live" wording** (Track 2 guardrail): dashboard badge `Live · updated`
  → `Snapshot · as of {last_run}` (pulsing dot made static); hero "currently live
  on the radar" → "tracked in this snapshot"; landing CTA "Explore the **live**
  dashboard" → "Explore the dashboard".
- **Fiche coherence fixes**: the per-fiche "top N%" was hard-coded to 100% for
  every fiche → now a real score percentile; the source CTA was always "View on
  Gitee" → now source-aware ("View on GitHub" for the 67 GitHub-sourced fiches vs
  "View on Gitee" for the 39 Gitee ones).
- **Dashboard labels**: "Gitee organizations" → "Organizations" and stack/legend
  updated to "Gitee + GitHub" (sources are both); removed a stale "27 orgs" figure.
- **Stale editorial removed** from the shipped tree: `output/dispatch_00.md`
  (old-corpus opening edition, now factually wrong) moved to `archive/` (preserved,
  git-ignored, never served). `output/dispatch_*.md` + `archive/` added to
  `.gitignore`.
- Verified: 106 EN ↔ 106 FR fiches (zero asymmetry), 106 `f/` pages = 106
  `state.json` repos = 0 orphans, 105/105 tests green. `docs/UX_REDESIGN.md` and
  `ROADMAP.md` updated to record the resolved-hygiene status and the deploy-manifest
  caveat (only ship `index/dashboard/pro/f/sitemap/robots`, not `state.json` etc.).

## [0.18.0] — 2026-07-30

### Changed — UX redesign Phase 2: fiche-first dashboard explorer

- **Dashboard "Explore" reworked from a card grid into a 2-pane explorer**
  (`build_dashboard`): a compact, scannable **list** (left) + a **light, sticky
  detail panel** (right) showing the decision layer (Problem / How / Chinese
  specificity / **Western equivalent** highlighted / maturity / confidence +
  source & full-fiche links). Opens on the top fiche (fiche-first); `↑`/`↓` and
  click move through the corpus fast — the fast-exploration feel is preserved
  (owner requirement).
- **Use-case quick views** (presets): Edge-AI benchmarking, Robotics stacks,
  RTOS/BSP/firmware, High-confidence only — on top of the existing
  domain/type/account/maturity filters, search and sort (all preserved). New
  client-side confidence filter.
- Fixed stale "how it works" diagram text (Gitee+GitHub, semantic + anti-noise,
  EN+FR). Inline JS validated with `node --check`.

### Changed — UX redesign Phase 1: landing + publication hygiene

- **Landing rebuilt** (`build_site.build_landing`) around the validated framing
  (`docs/UX_REDESIGN.md`): value-prop hero ("Decision-ready intelligence on
  China's open-source hardware", B2B but engineer-accessible); a **real staged
  fiche** (sophgo/tpu-mlir) rendering the decision layer with the
  Western-equivalent field highlighted + confidence badge — the anti-directory
  proof; a **use-cases** section (tech scouting / competitive intelligence /
  sourcing-BOM / edge-AI benchmarking); accurate "how it works" (Gitee+GitHub,
  semantic scoring, EN+FR); honest corpus numbers (106 fiches, vendor share); a
  sources-&-method trust band; funnel CTAs (dashboard → weekly brief → Pro).
- **`docs/UX_REDESIGN.md`** — the validated framing + phase plan + owner decisions.

### Fixed — Publication hygiene

- `build_site` now **purges orphan fiche pages** (141 stale pages from the old
  corpus removed; sitemap 179 → 109 URLs, reflecting only the 106 live fiches).
- `build_site` **warns loudly** when `MINERVA_SITE_URL` is still the
  `minerva.example` placeholder (canonical/OG/sitemap would be fake) — set the
  real domain before any public deploy.
- Removed stale dated newsletters (kept the latest).

## [0.17.0] — 2026-07-30

### Added — GitHub org harvest (corpus 43 → 106)

- Authenticated full harvest of the 5 configured GitHub vendor orgs (bouffalolab,
  sophgo, unitreerobotics, kendryte, allwinner-zh) via `GITHUB_TOKEN`. Admission
  v2 kept **63 new wedge-pure repos** out of 221 enumerated: Unitree 31 (robotics),
  Sophgo 24 (edge-AI / RISC-V), Bouffalo 9 (MCU), Kendryte 3.
- **Corpus 43 → 106 fiches**, 15 owners; **big-tech share 30% → 12%** (77% before
  recalibration). Domains: Embedded 55, Edge AI 45, **Robotics 2 → 9**, IoT 2.
- Confirmed the incremental invariant end-to-end: an anonymous run generated 44
  fiches before the 55 req/h throttle, then the token relaunch bootstrapped those
  44 for free and generated only the remaining ~20 (~45 s total run).
- Dashboard, newsletter and static site rebuilt on the 106-fiche corpus; README
  (EN/FR) figures updated.

## [0.16.0] — 2026-07-30

### Added — Security hardening (pre-publication)

- **Hardened `.gitignore`**: now ignores every `.env.*` variant (not just
  `.env`) plus common secret shapes (`*.pem`, `*.key`, `*.p12`, `secrets.json`,
  `credentials.json`); `.env.example` explicitly allowed. Verified by simulation
  that `.env.local` / `.env.production` / `.env.bak` are no longer committable.
- **`.env.example`** — placeholder template for the three keys (GITEE_TOKEN,
  ANTHROPIC_API_KEY, optional GITHUB_TOKEN).
- **`scripts/secret_scan.py`** — local pre-push scan: fails if a real key
  pattern (Anthropic / GitHub PAT / Gitee access_token) appears in a committable
  file, or if any real `.env` is git-tracked. Verified: detects a planted key;
  the real repo is clean (45 files).
- **`SECURITY.md`** — secret-handling policy, a required pre-first-push checklist
  (rotate dev keys, run the scan, confirm `.env` unstaged, least-privilege
  GITHUB_TOKEN), and responsible-disclosure guidance.
- **CI guard consolidated** to run `scripts/secret_scan.py` (single source of
  truth) instead of an inline grep.

### Verified

- Full secret sweep: real GITEE_TOKEN / ANTHROPIC_API_KEY appear **only** in the
  local (gitignored) `.env`; no token in logs or any generated artifact.

## [0.15.0] — 2026-07-30

### Changed — Corpus recalibration: admission v2 (anti big-tech noise)

Product decision: the corpus must visibly match the wedge (embedded / IoT /
robotics / edge-AI on Chinese silicon), not generic big-tech OSS. Implemented as
two config-driven admission rules — the **score formula is untouched** and the
incremental invariants are preserved:

- **Contrastive anti-domain filter** (keyword-less repos only): 3 embedded
  "anti-domains" (ML research & large models, web & app dev, cloud & big-data
  infra) in `config/domains.json`; a repo with zero curated keywords is rejected
  when `best_anti_similarity > best_similarity + ANTI_MARGIN (0.08)`. Curated
  keywords grant immunity (a human anchor outranks a statistical similarity).
- **Generalist orgs require a curated keyword** (`generalist_orgs` in
  `config/sources.json`): calibration showed all confirmed noise entered via the
  semantic-only path with zero keywords, while true positives (MNN, PaddleOCR)
  carry one. Admission for these orgs = ≥1 keyword AND `sim ≥ 0.35`.
- **Keyword list surgery**: added high-precision wedge terms (risc-v, riscv,
  toolchain, u-boot, openharmony, harmonyos, ros, ros2, quadruped, unitree,
  motor, servo, motion control, tpu, maix, maixpy, maixcdk); removed
  demonstrated noise-openers (`sdk`, `control`, `motion`, `量化` — the last
  substring-matched inside 轻量化 "lightweight").
- **Keyword matching normalizes `_` and `/`** to spaces so repo names like
  `unitree_ros` anchor correctly (hyphens preserved for `risc-v`).
- **GitHub seeds now replace stale same-slug mirrors** (`pipeline._fetch_github_seeds`):
  Kendryte/Bouffalo keep dead Gitee mirrors that previously shadowed the live
  GitHub repos and got them silently hard-filtered.

**Corpus effect (fresh full run, 3,660 repos enumerated):** 176 → **43 fiches**,
12 → **15 owners**, big-tech share **77% → 30%**; 141 generic repos removed
(alibaba 76, ByteDance 50, paddlepaddle 13…), 8 wedge repos added (Sipeed MaixPy,
bearpi, AliOS-Things, MNNKit, Dummy-RISC-V-VPU…). Live calibration set: 17/17.

### Discovered — Gitee is drying up for the wedge (structural finding)

The full harvest hard-filtered **2,313/3,660 repos as stale >2 years**, including
**1,617 OpenHarmony repos** (openharmony, -sig, -tpc): the OpenAtom ecosystem has
migrated off Gitee (toward AtomGit/GitCode) and several hardware vendors publish
primarily on GitHub. Documented in `data-sources-and-compliance.md` (candidate
priorities raised) and ROADMAP (coverage path = GitHub token harvest +
AtomGit/GitCode connector). The "15/27 zero-fiche orgs" from the external audit
were stale mirrors, not fetch failures.

### Tests

- +9 (now **105**): admission v2 (contrastive rejection/immunity, generalist
  keyword rule, backward-compat without new params, `load_anti_domains`,
  underscore keyword matching) and GitHub-seed stale-mirror override.

## [0.14.1] — 2026-07-30

### Fixed — Truth alignment (findings from independent external audit)

An independent read-only audit (Grok, 2026-07-30) surfaced doc/site claims that
had drifted from reality. All verified findings fixed:

- **Stale test counts** (77/78 → **96**) in README badges, README.fr, key figures,
  project-structure comment, CONTRIBUTING, ROADMAP, ARCHITECTURE.
- **Stale LLM cost** (~$0.005/fiche → **~$0.01 per bilingual repo pair**) in
  README, README.fr, ARCHITECTURE, BUSINESS.
- **Landing badge** "Live · updated this week" (false: last pipeline run
  2026-04-27) → replaced by the honest "last pipeline run {date}".
- **Pro FAQ "Why not GitHub?"** claimed GitHub was future work while the connector
  has been integrated since 0.10.0 → rewritten ("Gitee only, or GitHub too?").
- **Landing wording** updated to Gitee **and** GitHub (hero lede + orgs stat label).
- **Phase-0 test artifact** `output/fiches/test_claude_kernel_liteos_a.md`
  removed (old-format FR file, invisible to tooling, outside state.json).
- **Stale `[MODIFIÉ]` badges** (April-era) stripped from the 4 stored fiches
  (EN + FR).
- **README honesty note**: current demo corpus spans 12 of the 27 watched orgs.
- **CI secret guard**: workflow now fails if `.env` is tracked or an API-key
  pattern appears in tracked files.
- **ROADMAP**: new audit-driven TODOs — corpus rebalancing (77% Alibaba+ByteDance
  skew, 15/27 orgs at zero fiches), hosted freshness, `rescore.py` EN-only drift
  risk, mixed `state.json` scores schema.

## [0.14.0] — 2026-07-30

### Added — Native bilingual pipeline (closes the last V1 roadmap gap)

- **`translator.generate_fiche_pair(repo, readme, score_info)`** — produces the
  EN + FR fiche pair from a SINGLE source of facts: one English LLM generation +
  one EN→FR prose translation (temperature 0), both markdowns composed by the new
  deterministic helper `_compose_fiche` (extracted from `generate_fiche`, whose
  single-language API is unchanged). Fail-safe: if the translation fails, the FR
  fiche keeps English prose under French labels rather than failing the repo.
- **Pipeline saves both sets natively** (`pipeline._process_llm`): every NEW /
  MODIFIED repo writes `output/fiches/<slug>_fiche.md` (EN) **and**
  `output/fiches_fr/<slug>_fiche.md` (FR); the `[MODIFIÉ]` badge is applied to
  both. `python src/pipeline.py` alone now maintains the two languages — no
  separate manual step.
- **Bootstrap requires the pair**: `_classify_only` short-circuits to BOOTSTRAP
  only if BOTH fiches exist (`_both_fiches_exist`); a missing language routes the
  repo through NEEDS_LLM (self-healing, no silent drift).
- **DELETED handled on both sides**: `scripts/clean_fiches.py` now removes
  orphans from `output/fiches/` and `output/fiches_fr/` together.
- **Tests**: +11 (96 total) — `generate_fiche_pair` (1 generation + 1 translation,
  empty signal, translation-failure fallback) and a new `tests/test_pipeline.py`
  (pair written on NEW, badge on both for MODIFIED, SKIPPED_EMPTY, dry-run,
  bootstrap-requires-both, self-healing classification).

### Changed

- `scripts/build_lang_fiches.py` is demoted to a one-shot migration/backfill tool
  (docstring updated) — no longer part of the normal flow.
- Per-repo LLM cost is now 1 generation + 1 small translation (~2 Haiku calls,
  still ≈ $0.01/repo); the incremental logic (UNCHANGED/SKIPPED_EMPTY short-
  circuits) is unchanged.

## [0.13.0] — 2026-07-29

### Added — Publishable V1 deliverables

- **`data-sources-and-compliance.md`** — per-source compliance register (access
  method, API-vs-scraping status, what we republish, risks, decision) for the
  integrated sources **and** candidate Chinese sources (GitCode, GitLink/Trustie,
  AtomGit, vendor portals), with an explicit integration rule. Cross-linked from
  `docs/SOURCES.md` and the README.
- **Confidence score** — transparent data-quality tier (High/Medium/Low) per
  fiche, computed from enrichment depth, metadata completeness, recency and an
  "unverified" flag (`confidence_tier` in `src/fiche_schema.py`, shared with the
  dashboard). Surfaced as a card badge; documented in `docs/SCORING.md`. Real
  spread on the current corpus: 108 High / 68 Medium. +7 tests (now 85 total).
- **`docs/SCORING.md`** — explains the relevance score and the confidence tier.

### Changed

- **`ROADMAP.md`** restructured into **MVP / V1 / V2** with explicit TODOs.
- **README** — status note (working MVP), confidence in "What you get", docs index
  updated (compliance register, scoring).

## [0.12.0] — 2026-07-29

### Added — Product hardening for publication (docs, framing, demo polish)

- **Product docs suite** under `docs/`: `POSITIONING.md` (value prop, ICP, use
  cases, differentiation), `BUSINESS.md` (revenue models, packaging/pricing,
  go-to-market), `SOURCES.md` (data sources, access method, rate limits, IP &
  compliance posture), `ARCHITECTURE.md` (modules, data flow, design decisions),
  plus top-level `ROADMAP.md`, `CONTRIBUTING.md`, and a `docs/DECISIONS.md`
  worklog.
- **Honest architecture diagram** `docs/assets/pipeline.svg` (brand-consistent,
  theme-safe, GitHub-renderable) used as the README hero.
- **README reframed product-first**: one-line value proposition, "Who it's for" +
  use cases, "What you get", docs index and badges — technical depth preserved.
  French README mirrored (badges, value prop, diagram, docs index).

### Changed

- **Dashboard demo polish**: hero rewritten to the value proposition (Gitee **and**
  GitHub, Western-equivalent mapping); added a footer sources-&-method trust line
  (official APIs, public metadata only, links back, "to be confirmed" convention).
- `.gitignore` comments translated to English (English-default consistency).

## [0.11.0] — 2026-07-29

### Added — English-first bilingual output (i18n)

- **English is now the default language, French is language 2** — for the GitHub publication.
- **Bilingual README and CHANGELOG**: `README.md` / `CHANGELOG.md` (English, default) + `README.fr.md` / `CHANGELOG.fr.md` (French), with a language switcher at the top of each.
- **`translator.py` internationalized**: `generate_fiche(..., lang="en"|"fr")`. English default. Localized field labels (`FIELD_LABELS`), maturity categories (`MATURITY_LABELS`), repo-language labels (`CODE_LANGUAGE_LABELS`), domain-name display (`DOMAIN_DISPLAY`), a full English `SYSTEM_PROMPT_EN` + English user prompt, and colon typography per language (EN `Type:`, FR `Type :`). New `translate_fiche_prose(prose, target_lang)` for faithful cross-language translation without re-fetch.
- **`fiche_schema.py` bilingual**: `Fiche.from_markdown` parses both EN and FR labels (`_LABEL_ALIASES`), detects the fiche language (`_detect_lang` → `Fiche.lang`), and `to_markdown` re-emits the matching labels/typography — round-trip preserved per language (used by `rescore.py`).
- **352 bilingual fiches**: 176 English in `output/fiches/` (default) + 176 French in `output/fiches_fr/` (language 2), generated by the new `scripts/build_lang_fiches.py` (translates the existing French set to English, remaps deterministic fields, no network re-fetch).
- **Output builders internationalized**: `build_dashboard.py`, `build_site.py`, `build_newsletter.py` UI translated to English; their fiche parsers accept both EN and FR labels; domain/status/language matching keys canonicalized to English (`Embedded`/`Robotics`/`Active`/`Bilingual CN-EN`) so charts, filters and tag colors work on the English fiches.
- **Code comments and docstrings** across `src/` and `scripts/` translated to English (runtime log messages and LLM prompts intentionally left as-is).

## [0.10.0] — 2026-07-29

### Added — GitHub connector (Chinese orgs absent from Gitee)

- **`src/github_fetcher.py`**: new GitHub REST v3 API connector, mirroring the public API of `fetcher.py` (`configure`, `list_all_repos_by_owner`, `fetch_repo`, `fetch_readme`). Normalizes GitHub repos to Minerva's exact schema and tags them `_minerva_source="github"`. Handles: self-imposed rate-limit (55 req/h anonymous, 4500 with `GITHUB_TOKEN`), respect for `X-RateLimit-Remaining`/`Reset`, retry on 403/429 (secondary rate limit), auto pagination, filtering of pure forks (`SKIP_FORKS`), and `GitHubPaginationError` to protect an owner from a false deletion detection (mirror of `FetchPaginationError`).
- **Pipeline wiring** (`pipeline.py`): `_fetch_github_accounts` / `_fetch_github_seeds` merge GitHub repos into the `repos` dict (Gitee takes priority on slug collision). GitHub orgs enter the `watched_owners` set (scoring bonus) and the protection for failed owners. `_process_llm` now routes the README fetch to the correct host based on `_minerva_source`.
- **Source-aware fiches**: `translator.generate_fiche` emits `**GitHub :** https://github.com/{full_name}` for GitHub repos (instead of `**Gitee :** …`). The 4 downstream parsers (`fiche_schema`, `build_dashboard`, `build_site`, and `build_newsletter` via the schema) accept both labels. `Fiche.source_label` (computed) guarantees a correct round-trip via `rescore.py`.
- **`config/sources.json`**: new keys `comptes_github` (bouffalolab, sophgo, unitreerobotics, kendryte, allwinner-zh — orgs verified live) and `seeds_github`.
- **Tests**: `tests/test_github_fetcher.py` (13 tests — normalization, pagination, forks, rate-limit, README, `GitHubPaginationError`). Total suite: **77 tests** (was 64).

### Fixed

- **`src/embedder.py`**: forces `USE_TF=0` / `USE_FLAX=0` before any import of `transformers`, to avoid the `TypeError: Descriptors cannot be created directly` crash on machines where TensorFlow + a recent protobuf are installed. Minerva only uses the PyTorch backend. (The Ubuntu CI was not affected because TF is not installed there.)
- **`src/analyzer.py`**: docstring of `filter_repos` corrected (`HIGH_SIM_THRESHOLD` = 0.45, was mistakenly noted as 0.55).

## [0.9.0] — 2026-04-26

### Added — Hybrid keyword + semantic scoring

- **Hybrid admission logic** in `analyzer.filter_repos`: a repo is kept if **(a)** `best_similarity ≥ 0.45` (semantic-strong) **OR** **(b)** at least 1 discriminating keyword matched (keyword-anchored). Plus the `score_total ≥ min_score` (15) threshold, unchanged. Resolves the tradeoff identified in 0.8.0: recovers the true positives with sparse descriptions (PaddleOCR via "ocr"; LuatOS via "esp32") without reopening the door to generic ML research noise. Calibration: 0.55 tested first (86 kept, too strict — the majority of true embedded positives are in the 0.40-0.55 sim range), then 0.45 retained (**371 kept** out of 3621, acceptable signal/noise).
- **`analyzer._match_keywords(repo, domains)`**: new private helper that iterates over the `mots_cles` of all domains and matches within `full_name + description` via `_keyword_in_text` (CJK substring + ASCII case-insensitive boundaries, already existing). The language is excluded to avoid false positives like "C" that matches everywhere.
- **`mots_cles_matches`** is now actually populated in the output of `score_repo` (was `[]` in 0.8.0). Usable by fiches/dashboard/newsletter to make the keyword-anchor explicit.
- **pytest tests**: 3 new scenarios in `tests/test_analyzer.py` (`test_filter_repos_drops_no_keyword_low_sim`, `test_filter_repos_keyword_anchor_admits_sparse_desc`, `test_filter_repos_rejects_ml_research_no_specific_keyword`). Schema test updated to verify `mots_cles_matches` is non-empty when keywords are effectively present.

### Changed — Tightening of Edge AI keywords

- **`config/domains.json` Edge AI mots_cles**: removed the generic terms that trigger ML research noise (`ai`, `ml`, `neural`, `deep-learning`, `transformer`, `llm`, `image`, `vision`, `detection`, `recognition`, `segmentation`, `quantization`, `inference`). Kept the deployment-specific terms (`ncnn`, `tflite`, `onnx`, `tensorrt`, `mnn`, `tnn`, `paddle-lite`, `openvino`, `mindspore lite`, `ocr`, `npu`, `kpu`, `dpu`, `推理`, `神经网络`, `量化`). Added `rknn`, `snpe`, `coreml`, `paddlelite` (frequent spelling variants).
- **analyzer.py constants**: removed `MIN_SIM_WATCHED` / `MIN_SIM_UNWATCHED` (logic now hybrid). Replaced by a single `HIGH_SIM_THRESHOLD = 0.55`.

### Cleanup repository
- Removed Python caches (`__pycache__/`, `.pytest_cache/`).
- Removed dev logs (kept the 3 most recent) and all `probe_*.log`.
- Removed the one-shot diagnostic scripts: `probe_gitee_search.py`, `probe_luatos.py`, `probe_new_seeds.py`, `probe_owner_casing.py`, `probe_seeds.py`, `test_claude_api.py`, `test_real_data.py`, `compare_scoring.py`. Their intent is documented in the CHANGELOG; their output is no longer relevant after the tightening.
- Removed `output/state.json.before_semantic` (obsolete snapshot, no longer comparable since the switch to hybrid) and `output/diff_20260425.md`.
- Removed `test_batch/` (phase 0 artifact).
- 923 orphan markdown fiches removed via `clean_fiches.py` (state.json is the source of truth after the 0.30/0.40 calibration of 0.8.0).

## [0.8.0] — 2026-04-25 (night, continued)

### Added — Semantic scoring via embeddings

- **`src/embedder.py`**: lazy wrapper around `sentence-transformers` with the `paraphrase-multilingual-MiniLM-L12-v2` model (~118 MB, 50 languages, 384-dim L2-normalized vectors). API: `get_embedder()` (singleton), `embed(text)`, `embed_batch(texts)`, `cosine(a, b)`. Persistent disk cache `output/embeddings_cache.json` indexed by SHA-256 hash of the source text — automatic invalidation if the model changes.
- **`config/domains.json` v2**: each domain now has a `definition` (a dense 80-120 word paragraph describing the semantic intent). The `mots_cles` remain available for offline fallback / other tools.
- **Refactor of `analyzer.score_repo`**: complete replacement of keyword matching by cosine similarity against the embeddings of domain definitions. Output schema preserved (`score_total`, `scores_par_domaine`, `mots_cles_matches=[]`, `domaine_principal`) + new `best_similarity` field (float [0, 1]).
- **Pre-batch embeddings in `filter_repos`**: 1 `model.encode()` call on all non-hard-filtered repos instead of N individual calls (~10× faster cold).
- **New similarity thresholds**:
  - `MIN_SIM_WATCHED = 0.18` (curated accounts)
  - `MIN_SIM_UNWATCHED = 0.25` (others)
  Replaces the old "≥1 keyword matched" guard. If a repo does not reach the threshold in any domain → drop.
- **pytest tests** (`tests/test_analyzer.py` rewritten): 13 tests including 8 new semantic ones (RTOS → Embedded, OCR/CN → Edge AI, off-topic repo → low sim, multi-domain, output schema). The model loads on the first test (~3 s), and benefits from the cache for subsequent ones.

### Changed
- Complete removal of the `POINTS_KEYWORD` / `BONUS_KEYWORD_FULL_NAME` computation from the score. Global bonuses (stars, forks, recency, CJK, non-mirror, watched_owner) kept and unchanged.
- `requirements.txt`: added `sentence-transformers>=2.5.0,<3` and `numpy>=1.24.0`.
- `_keyword_in_text` kept in analyzer.py for backward compatibility (public utility, not in the scoring).

### Empirical validation and calibration
- Analyzer self-test: Tencent/ncnn (CN description "高性能神经网络...") → Edge AI score 99 sim 0.63; openharmony/kernel_liteos_a → Embedded sim 0.52; ByteDance/xgplayer (HTML5 player) → IoT sim 0.28.
- Full pipeline run on 3621 repos with **3 successive calibrations**:
  - **0.18 / 0.25** (initial) → **2250 kept** (over-inclusive: ByteDance ML research, ComfyUI, diffusion models, etc. match Edge AI via the words "transformer/image/llm" without being real edge inference).
  - **0.30 / 0.40** (mid) → **1336 kept** (still too many: most ML research projects still pass the watched threshold, which is too lax for big-tech orgs with 400+ repos).
  - **0.42 / 0.50** (final) → target ~250-400 repos, acceptable signal/noise.
- **One-shot LLM cost**: 1575 fiches generated on the first pass (~$8 LLM Haiku 4.5). They remain on disk, reusable via bootstrap if future calibration brings them back. Deliberate cost: architecture tested at scale, empirical validation of thresholds.
- 44/44 pytest green.

### Tradeoff identified (to dig into)
Pure semantic scoring has a blind spot: the embedding model does not distinguish
sufficiently between "edge inference" and "ML research / cloud vision" — both have a
high similarity with an Edge AI definition that mentions transformers, vision,
quantization. Consequence: the thresholds have to be very high (0.50 unwatched)
to reject the noise, which can cause the loss of legitimate but poorly described
edge projects (e.g. alibaba/Mooncake — memory pool for LLM serving, lost at the 0.50 threshold).

**Possible evolution** (if precision becomes an issue): a hybrid keyword+
semantic approach. Keep a mandatory keyword (≥1 keyword matched) + ranking by semantics.
Combines the precision of the keyword (PaddleOCR via "ocr") with the semantic nuance
(graded score according to the strength of the match). It would go back to the 0.7.x system but with
a score refined by embedding instead of simple counting. Not implemented in this
version out of fidelity to the "replace keyword matching" instruction.

## [0.7.1] — 2026-04-25 (night)

### Added
- `translator._clean_readme_paragraphs(readme, max_chars=3500)`: pre-processing of the README before LLM injection. Removes shields.io badges, decorative HTML blocks (img/table/center), horizontal rules, entire License/Copyright sections, HTML TOC, and truncates code blocks > 300 chars (keeps 6 lines + a marker). Idempotent.
- 9 pytest tests for `_clean_readme_paragraphs` (badges, HTML, license, TOC, code blocks, blank lines, max_chars truncation, idempotence, None/empty handling).
- `scripts/probe_gitee_search.py`: 9 variants tested on `/search/repositories` (q-param, header-token, /search/repos, sort, language, fork, POST, keyword without hyphen, Chinese keyword, known repo name). Result: all HTTP 200 + 0 results. /search/users works with the same token (sanity check) → Gitee server bug confirmed, specific to /search/repositories.
- `scripts/probe_luatos.py`: 15 slugs tested. Result: `openLuat/LuatOS` exists via direct access (1836★, Lua engine for Hezhou's Air8000/Air8101/Air780E cellular modules) but the `openLuat` org does not enumerate (404 on /orgs and /users). It is a "shadow" org — individual repo access only.
- `openLuat/LuatOS` added to `seeds_gitee` to work around the lack of org enumeration.

### Changed
- `_call_claude_for_fiche` now injects `_clean_readme_paragraphs(readme)` instead of raw `readme[:3500]`.
- Mention "(nettoyé : badges/license/TOC/blocs code longs supprimés)" in the prompt so that Claude knows what it sees has been filtered.
- `fetcher.search_repos` comment updated with the detail of the 9 tested variants (proof that it is indeed a server bug, not a missed format).

### Quality (LuatOS, fiche freshly generated with the new prompt + clean_readme)
- Chipsets named precisely: Air8000, Air8101, Air780E
- Concrete counters: "Lua 5.3, 74 bibliothèques noyau, 55 extensions C, ~1000 APIs"
- Named tools: "GitHub Actions pour CI", "LuaTools pour flashage"
- Precise Chinese specificity: "Hezhou (合宙), fabricant majeur de modules cellulaires LTE-M/NB-IoT"
- Honesty: "Aucune conformité à standard chinois spécifique détectée ; pas d'intégration WeChat/Alipay/Baidu Cloud mentionnée"

## [0.7.0] — 2026-04-25 (evening)

### Added
- **Parallelization of LLM calls** in `pipeline._generate_fiches` via `ThreadPoolExecutor`. Configurable via `MINERVA_LLM_WORKERS` (default 8). Observed benchmark: 8 fiches in 11 s (vs ~24 s sequential); bootstrap of 140 fiches goes from ~7 min to ~1 min.
- Thread-safe Gitee rate-limiter: `_acquire_rate_permit()` groups check + sleep + reserve under `threading.Lock`. Avoids quota overruns in parallel.
- `Anthropic(max_retries=4)`: native SDK retry on 429/5xx with exponential backoff — covers bursts against the Haiku 4.5 RPM limit.
- Validation of the LLM `type` field against `ALLOWED_TYPES`; automatic fallback to `infer_type()` if the value is out of the list.
- Multi-page static site: `output/index.html` (landing + email capture), `output/pro.html` (3-tier pricing + waitlist), `output/f/<slug>.html × 140` (1 page per fiche, OpenGraph + canonical), `output/sitemap.xml`, `output/robots.txt`. Monetization funnel ready (Buttondown/Substack/MailerLite via env var).

### Changed
- **Claude prompt rewritten in French** with a senior-engineer tone, strict anti-marketing rules (words "puissant", "complet", "moderne"… forbidden), precise definitions of the 8 types, per-field length constraints, and an "à confirmer" instruction rather than inventing. An org context system is injected (`ORG_SPECIFICITE`).
- `CLAUDE_MAX_TOKENS` 500 → 800, `CLAUDE_TEMPERATURE` 0.2 → 0.1 (more deterministic). README slice 2000 → 3500 chars.
- `DELAY_BETWEEN_REQUESTS_S` for authenticated Gitee 0.5 s → 0.1 s (the hourly cap is enough, frees up parallelism).
- Test `test_configure_authenticated_sets_higher_rate` adapted to the new value.

### Quality observations (before/after sample)
- `Tencent/ncnn`: before = generic "framework optimisé"; after = "écrit en C++, support ARM 32/64-bit, format propriétaire ncnn (conversion via pnnx), Vulkan pour GPU mobile, NEON, OpenMP". Honest Chinese specificity: "pas de lien vendor chinois, cible SoC ARM généralistes".
- `paddlepaddle/PaddleOCR`: before = "suite complète multilingue"; after = "Python 3.8–3.12, distribution PyPI, runtime PaddleInference, sous-modèle PaddleOCR-VL nommé, équivalents contextualisés (LLaVA/Qwen-VL pour la partie vision-langage)".

## [0.6.0] — 2026-04-25

### Added
- `scripts/clean_fiches.py`: removal of orphan markdown fiches (present on disk but absent from `state.json`).
- `scripts/probe_owner_casing.py`: verification of the canonical casing of Gitee owners.
- "≥1 keyword matched" safeguard in `analyzer.filter_repos`: a repo without any domain keyword is rejected regardless of its score (eliminates false positives purely carried by the global bonuses).
- Case-insensitive comparison of owners (`watched_owners` lowercased) in `analyzer.score_repo` and `analyzer.filter_repos`.
- Persistence of the `scores` key in `state.json` across pipeline runs (preservation of the work of `rescore.py`).
- Expansion of `config/domains.json`: Edge AI gains 11 keywords (ocr, vision, ai, ml, deep-learning, transformer, llm, image, detection, recognition, segmentation), Embedded 6 (cortex, arm, mips, dsp, fpga, soc), IoT 1 (coap).
- pytest test suite (`tests/test_analyzer.py`, `test_fetcher.py`, `test_translator.py`) and GitHub Actions CI workflow (`.github/workflows/ci.yml`).
- Apache 2.0 LICENSE.

### Changed
- `_keyword_in_text` now uses `re.ASCII` for ASCII keywords: an English word like "OCR" matches in the middle of a Chinese text (CJK characters are no longer seen as `\w`, so word boundaries work).
- README: title + 30-second Demo section + figures expressed in relative terms.
- `config/sources.json`: 6 owners normalized to their canonical Gitee casing (Sipeed, ByteDance, paddlepaddle, JD-opensource, Tencent, TencentOS), added starfive and starfive-tech, removed `openLuat` (404 on all variants: org gone from Gitee).

### Removed
- 181 orphan fiches (`output/fiches/*.md`): 171 `third_party_*`, 1 `mirrors_*`, 9 old archives — corpus cleaned up.
- `openLuat` removed from the list of watched accounts.

### Fixed
- Unicode word-boundary bug: ASCII keywords could not match in the middle of a CJK text (`\b` Unicode-aware). PaddleOCR and other Chinese descriptions with English acronyms were silently filtered out.
- Gitee casing: 5+ accounts (ByteDance, paddlepaddle, JD-opensource, Tencent, etc.) did not receive the +8 watched bonus nor the low threshold (15 vs 20) because of a strict-case string comparison.

## [0.5.0] — 2026-04-25

### Added
- **Edge AI** domain in `config/domains.json` (mobile inference frameworks, NPU, AI hardware acceleration).
- 8 new watched big-tech orgs (alibaba, bytedance, baidu, paddlepaddle, jd-opensource, tencent, dongshanpi, licheepi).
- `scripts/rescore.py`: recomputation of the scores of existing fiches with an up-to-date `domains.json`, **without any LLM call** (free).
- HTML + TXT newsletter (`scripts/build_newsletter.py`): rich version for the browser + plain-text version sendable by email.
- Probe scripts to validate candidate Gitee seeds.

### Changed
- `state.json` enriched with the `scores` key (per repo: score, domain, edge_ai_score).

## [0.4.0] — 2026-04

### Added
- Single-file interactive dashboard (`scripts/build_dashboard.py` → `output/dashboard.html`): dynamic filters by domain/type/score, full-text search, sorting, openable without a server (file://).
- Incremental diff: `output/diff_YYYYMMDD.md` listing NEW/MODIFIED/DELETED per run.
- `state.json`: persistent memory between runs (`last_run`, `repos: {full_name: pushed_at}`).
- Bootstrap LLM-skip: if a fiche already exists on disk for a repo classified as NEW (first run with a pre-existing corpus), no LLM call, just recording of the state.
- Exponential retry on the intermediate pages of Gitee pagination + carry-forward of the state for owners with an incomplete fetch (anti-false-deletion).

### Fixed
- Gitee pagination glitch that caused false deletion detections (271 false-deletes eliminated).

## [0.3.0] — 2026-04

### Added
- LLM enrichment via Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) for the analytical fields of the fiche (Problem solved, How it works, Chinese specificity, Type, Western equivalent).
- `seeds_gitee` in `config/sources.json`: manual mechanism to replace keyword search.
- Hard filters upstream of scoring: `third_party_*` and `mirrors/*` outside watched accounts.

### Removed
- CN-FR dictionary-based translation system (insufficient for quality technical fiches).

### Fixed
- Gitee keyword search (`/search/repositories`): endpoint broken server-side (systematically returns []). Cleanly disabled, replaced by `seeds_gitee`.
- `.env` loading: the python-dotenv convention (override of existing variables) is applied to prevent an old key persisted at the OS level from masking the value in the file.

## [0.2.0] — 2026-04

### Added
- Full orchestration pipeline (`src/pipeline.py`): fetcher → analyzer → translator.
- Gitee authentication via `GITEE_TOKEN` (rate-limit 4500 req/h vs 60 anonymous).
- Timestamped logging in `output/logs/`.

## [0.1.0] — 2026-04

### Added
- Initial architecture: `src/fetcher.py`, `src/analyzer.py`, `src/translator.py`.
- 3 initial domains (Embedded, IoT, Robotics) configured in `config/domains.json`.
- Standardized markdown fiche format (Type, Domain, Score, Problem solved, How it works, Chinese specificity, Western equivalent, Maturity, Language, Gitee).
