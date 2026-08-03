# Design Track — graphic direction of Minerva as a product showcase

> A distinct workstream from the UX/IA redesign (`docs/UX_REDESIGN.md`, which fixed
> *structure*: fiche-first, funnel, use cases). This Track is about the **visual
> identity and craft** — what Minerva *looks and feels like* as a vitrine. No visual
> execution starts until a direction is picked (below). Constraints preserved:
> static-first, no fake "live", engineer-credible not corporate-empty, don't break
> the validated Phase 1/2 structure — we re-skin, we don't re-architect.

## North star (visual)

In five seconds, the look alone should say: **a serious intelligence instrument on
China's open-source hardware — decision-ready, built by engineers, not a marketing
site and not a generic directory.** Craft carries credibility here more than copy.

## What this Track is / is not

- **Is:** color system, typography, layout grid, component styling, a rigorous
  data-viz language (domains + confidence), motion rules, and brand assets (logo
  mark, favicon, OG image). One coherent grammar across landing / dashboard / fiche
  / pro.
- **Is not:** new pages, new IA, new copy strategy, new product surfaces, or any
  signal/live behaviour (frozen until the history artifact + fresh run exist).

## Honest read of the current visuals

What exists today (from `build_site.py` / `build_dashboard.py`):

- Dark-only (`--bg-0 #08080d`), single red accent (`--acc #ff3344`), domain colors
  (Embedded blue / IoT teal / Robotics purple / Edge-AI pink), gold highlight;
  Inter/system sans + mono for code; radial-gradient background glow; `▲ MINERVA`
  wordmark; rounded cards.
- **Works:** coherent tokens, decent hierarchy, the fiche-first proof reads clearly,
  it's not amateur.
- **Weak / risk:** it reads as **generic dark-startup SaaS** (near-black + saturated
  red + glow is the default template look); the red is loaded (alarm / "China
  cliché") and undifferentiated; data-viz is decorative, not a real system; no
  ownable identity, no brand assets (favicon/OG/logo are minimal); light mode absent.
  Nothing here is *distinct to Minerva*.

The gap is not competence — it's **distinctiveness and intent**. That is what this
Track buys.

## Design principles (constraint-aware)

1. **Credibility over flash** — every choice must read as instrument, never gloss.
2. **Decision-first hierarchy** — the Western-equivalent, confidence and maturity are
   the visual heroes; the system foregrounds the decision layer.
3. **Honest motion** — functional only (focus, transitions); no pulsing "live", no
   motion implying real-time; dated snapshots stay labeled.
4. **Escape the default** — a deliberate, ownable palette + type + grid that does
   not look like the near-black/red startup template.
5. **Data as identity** — domains and confidence tiers get one rigorous, consistent
   color/mark language; the data-viz *is* part of the brand.
6. **Substance, not stereotype** — the "China" angle is carried by content, never by
   clichéd iconography (no dragons/lanterns); decide the red accent deliberately.
7. **One system, bilingual** — identical grammar EN/FR and across all surfaces.

## Direction — DECIDED (owner, 2026-07-31): **A, refined → "calm analytical instrument"**

Not "terminal cosplay". A **calm technical-intelligence instrument**: dense,
disciplined, fast to read. Emotion: **quiet authority, precision, rapid legibility.**
References: a *disciplined* financial terminal, a high-end devtool product, a *light*
intelligence console. Visual base = analytical instrument, **not** a nostalgic
terminal.

**Explicitly avoid:** hacker look, Bloomberg cosplay, neon-on-black, demonstrative
"techno" grids, "futuristic-AI" UI. Restraint is the point — the instrument is calm,
never theatrical.

The three candidate directions considered:

- **A — Instrument / Terminal.** Engineer-native: monospace-forward, dense, grid-ruled,
  muted palette + one signal accent, oscilloscope/devtool precision (Linear/Vercel
  restraint × Bloomberg terminal). *Max engineer credibility, most distinct; risk:
  can feel cold to non-eng buyers.*
- **B — Editorial intelligence / Dossier.** Analyst-publication: strong typography
  (serif × sans), generous space, calm authority, reads like a premium intelligence
  briefing (Economist / Stripe-press / research desk). *Best sells "decision-ready
  intelligence, not a directory"; risk: can drift "magazine" if overdone.*
- **C — Refined console.** Keep the dark console, but elevate it with real craft:
  precise data-viz, restrained accent, sharper hierarchy. *Lowest risk, closest to
  today; risk: hardest to fully escape the generic-dark look.*

(A hybrid — e.g. B's editorial authority for landing/fiche + A's instrument precision
for the dashboard — is viable and can be the outcome; we pick a primary first.)

## Design-system dimensions to define once a direction is chosen (D1)

Palette (light/dark decision) · type scale & pairing · spacing/grid · radii &
elevation · **domain + confidence data-viz colors** · iconography · motion rules ·
imagery/texture · brand assets (wordmark, favicon, OG). Delivered as a spec + one
reference page before touching real surfaces.

## Surface scope & order

Design language (D1) → **Landing** (highest-leverage vitrine) → Dashboard + Fiche →
Pro + brand assets (logo, favicon, OG image) → final polish. Cross-cutting: the
confidence/domain data-viz language.

## Phases & cadence (show before proceeding, like the UX Track)

- **D0 — Direction pick + mood** ✅ *A, refined → "calm analytical instrument".*
- **D1 — Design language / tokens + reference page** ✅ *validated 2026-07-31.*
  Light-first, technical paper + ink, one cool signal accent, mono for
  quantitative/labels, confidence as ink marks, no glow/fake-live/floating-shadow.
  Refinements: **accent dried to a mineral teal-slate `#2F5A5C`** (was `#0F766E`,
  too friendly-SaaS); **background grid near-subliminal** (`0.028` alpha). Reference:
  `docs/design/reference.html`.
- **D2 — Landing re-skin** ✅ *validated 2026-07-31 as a standalone mockup*
  (`docs/design/landing.html`). Keeps proof → trust → conversion; no marketing-site
  drift, no generic-dark. **Not wired** (owner method decision below).
- **D3 — Dashboard + Fiche re-skin** ✅ *validated 2026-07-31 as standalone mockups*
  (`docs/design/fiche.html`, `docs/design/dashboard.html`). System coherence across
  landing/fiche/dashboard held; 2-pane keeps fast-exploration + light detail; fiche
  is a real decision page with the Western equivalent as the reading hero.
  **Owner vigilance rule (binding):** on the fiche, **mono must not gain ground** —
  it carries *identifiers, metrics, labels, score only*; the analysis prose stays in
  the humanist sans, comfortable and readable, **never a spec-sheet**. Applies to
  every surface at wiring.
- **D4 — Pro + brand assets + polish** ✅ *validated 2026-07-31* as standalone
  mockups (`docs/design/pro.html`, `docs/design/brand.html`, `favicon.svg`,
  `og.svg`). One system across landing/dashboard/fiche/pro/brand confirmed.
- **Wiring — done 2026-07-31.** The validated system (D1–D4) is wired into
  `build_site.py` (landing/pro/fiche, shared BASE_CSS + chrome, favicon + og
  meta) and `build_dashboard.py` (hero/featured/landscape/runners-up/explorer/
  pipeline, confidence rendered as ink marks via a new `confMarks()` JS helper).
  Dashboard interactivity (search/filter/sort/keyboard/presets) is **byte-for-byte
  unchanged** — only presentation moved. Verified: 110/110 tests, dashboard inline
  JS `node --check` clean, 0 leftover dark-theme tokens, 0 fake-live wording, 0
  `minerva.example` in shipped output, placeholder degradation intact. **Not
  pushed, no fresh run.** OG PNG rasterization is still open — `build_site.py`
  ships `og.svg` and only emits `og:image` (pointing at `/og.png`) once a real
  domain is set; `og.png` itself must be rasterized at deploy time (see
  `docs/DEPLOYMENT.md`).

### Method decision (owner, 2026-07-31)

Keep every re-skin as a **standalone mockup** under `docs/design/` and do a **single
coherent wiring** of the shared token system at the end — do **not** partially wire
`build_site.py` with a "transitional light" state for pro/fiche. Rationale: the
landing, pro and fiche share BASE_CSS + chrome; a partial wire would leave visually
broken surfaces mid-stream. Nothing is wired, pushed, or run until landing + fiche +
dashboard mockups are all validated.

## Constraints held throughout

Static-first; no fake live / no signal behaviour; re-skin not re-architect (Phase 1/2
IA preserved); engineer-friendly not corporate; bilingual; 110 tests stay green;
nothing pushed; no fresh run; `build_history.py` stays on hold. All held through
wiring — verified in the Wiring entry above.

## Open owner decisions — all resolved

1. **Primary direction** — ✅ A refined ("calm analytical instrument").
2. **Theme** — ✅ light-first (technical paper + ink); calm-dark deferred as a later
   paired theme, not the vitrine's center of gravity.
3. **Accent** — ✅ mineral teal-slate `#2F5A5C` (dried down from an initial
   `#0F766E`).
4. **Method** — ✅ standalone mockups per phase, one coherent wiring at the end (see
   Method decision above) — done 2026-07-31.

## D5 — corrective pass (owner-requested, 2026-07-31)

Two independent audits (Grok, Lovable) converged: structure/UX solid, but the
rendered surface read as generic "premium template", not a "calm analytical
instrument". Root cause verified in code: the default system-font stack, 5–8px
"friendly SaaS" radii, and a near-invisible decorative grid — none of it
distinctive to Minerva. Corrective decision: **one bounded instrument register
(`--slab`) + a flattened radius scale + a reordered readout panel + a narrowed
typographic rule**, applied as a single coherent pass — not a redesign.

- **Validated on one reference surface first** (`docs/design/fiche-d5.html`) before
  propagating — same discipline as D1's reference page.
- **Typographic rule narrowed by the owner mid-pass**: mono is scoped to
  status-line / wordmark / score / metrics / labels / section markers / IDs only.
  Editorial H1/H2 (landing/dashboard/pro) stay **sans**, firmer (weight 660→700,
  tracking tightened to −0.03em, leading 1.08→1.05) — never mono by default. The
  fiche H1 staying mono is the identifier exception (it *is* an owner/repo id),
  not a precedent.
- **`--signal-on-slab` contrast checked and fixed**: `#5B948F` on `--slab`
  `#1B1E20` computes to 4.93:1 (WCAG relative-luminance calc — AA pass for normal
  text). In the process, found and fixed a real contrast issue on the readout's
  domain value (was domain-hue text on slab, ≈3.78:1, failing AA) — recolored to
  `--slab-ink`; the domain-color identity is now carried only by the readout's
  left-edge tick bar.
- **Propagated in the validated order — landing → dashboard → pro** — wired
  directly into `build_site.py` / `build_dashboard.py` (fiche already carried the
  reference treatment). Guardrails held: **exactly one `--slab` readout per
  surface, zero on pro** (no fiche data there); the dashboard's Explorer
  (`.ex-list`/`.ex-detail`) was deliberately kept on the light register — with 106
  rows re-rendering per keystroke/arrow-press, a slab flip there would violate
  "keep the slab calm"; its domain dot became a calm CSS-only left tick instead
  (pure restyle of the existing `.rdot` element — no DOM/JS change, since the
  inline style only ever set `background-color`).
- **Dashboard `<script>` block verified byte-for-byte unchanged** — diffed against
  the pre-D5 extracted JS; identical. All interactivity (search/filter/sort/
  keyboard/presets) untouched.
- **Verified**: 110/110 tests, `node --check` clean, 0 leftover dark tokens, 0
  fake-live wording, exactly 1 readout on landing/dashboard/fiche and 0 on pro
  across the real build output.

## Next up

D1–D5 are designed, validated and wired. What's left before this can go public:

- **OG image**: rasterize `output/og.svg` → `output/og.png` at deploy time (no
  rasterizer is wired into the build yet — headless Chrome / `rsvg-convert` /
  `cairosvg`, documented in `docs/DEPLOYMENT.md`).
- Owner review of the real rendered output (`output/index.html`,
  `output/dashboard.html`, `output/pro.html`, `output/f/*.html`) before proceeding
  to the pre-launch checkpoint (Track 1 clean + FR parity + history-artifact ready +
  deployment manifest, all already true) → fresh run → push.
