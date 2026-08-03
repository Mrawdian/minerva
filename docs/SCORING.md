# Scoring: relevance & confidence

Minerva surfaces two distinct, transparent signals per project. Neither is a
black box — both are computed from observable data.

## 1. Relevance score (0–100)

*"How relevant is this project to the four watched domains?"*

Computed in [`src/analyzer.py`](../src/analyzer.py):

- **Semantic similarity** — multilingual embeddings of the repo text
  (`full_name . description . language`) vs each domain's dense definition
  (cosine similarity). This is the core signal and works across Chinese/English.
- **Maturity & reach bonuses** — stars, forks, recent activity, CJK presence,
  non-mirror, and a bonus for officially-watched accounts.
- **Hybrid admission** — a repo is kept if it is semantically strong *or*
  keyword-anchored, above a calibrated threshold; mirrors, forks, third-party
  ports and archived repos are hard-filtered out.

The score is shown as the pill on each dashboard card and in the fiche
(`Relevance score: N/100`).

### Admission v2 — anti-noise tightening (2026-07-30)

An independent audit showed the corpus drifting toward generic big-tech output
(ML research, web/low-code, cloud infra) admitted through the *semantic-only*
path. Two config-driven rules now gate admission — the score formula itself is
unchanged:

1. **Contrastive anti-domain filter** (keyword-less repos only). Three off-wedge
   "anti-domains" (ML research & large models, web & app development, cloud &
   big-data infrastructure — `anti_domains` in `config/domains.json`) are
   embedded like the wedge domains. A repo with **zero curated keywords** is
   rejected when its best anti-domain similarity exceeds its best wedge
   similarity by more than `ANTI_MARGIN` (0.08 — calibrated live so that true
   positives like alibaba/MNN, whose description reads "deep learning
   framework", are not falsely cut). Repos carrying a curated keyword are
   immune: a deliberate human anchor outranks a statistical similarity
   (case in point: sophgo/tpu-mlir — "Machine learning compiler" leans
   ML-research semantically, but `tpu` is a curated wedge keyword).
2. **Generalist orgs need a curated keyword** (`generalist_orgs` in
   `config/sources.json`: alibaba, ByteDance, baidu, Tencent, JD-opensource,
   paddlepaddle). Calibration on a live good/bad set showed the noise
   (ERNIE-300B, flink-connectors, lowcode, weex, PaddleNLP) matches **zero**
   curated keywords while the true positives (MNN, PaddleOCR) all carry one.
   For these orgs, admission requires ≥1 curated keyword **and**
   `sim ≥ GENERALIST_MIN_SIM` (0.35). Wedge/vendor orgs keep the v1 OR-rule.

Supporting changes from the same calibration pass:

- **Keyword matching handles separator-heavy repo names**: `_` and `/` are
  normalized to spaces before word-boundary matching, so `unitree_ros` matches
  `ros`/`unitree` (hyphens are preserved — curated keywords like `risc-v`
  contain them).
- **Wedge keyword expansion**: `risc-v`, `riscv`, `toolchain`, `u-boot`
  (Embedded); `openharmony`, `harmonyos` (IoT); `ros`, `ros2`, `quadruped`,
  `unitree`, `motor`, `servo`, `motion control` (Robotics); `tpu` (Edge AI);
  `maix`, `maixpy`, `maixcdk` (Sipeed product line).
- **Low-precision keywords removed** after they demonstrably re-admitted noise:
  `sdk` (matched cloud/app SDKs), `control` (matched "flow control"), `motion`
  (matched AI video animation), `量化` (substring-matched inside 轻量化 /
  "lightweight").
- **GitHub seeds outrank stale mirrors**: a hand-curated GitHub seed replaces a
  same-slug Gitee copy when its `pushed_at` is fresher (several vendors keep a
  dead Gitee mirror while developing on GitHub).

Both admission rules are transparent (rejections are logged with the reason and
the similarity values) and reproducible (`tests/test_analyzer.py` +
`tests/test_pipeline.py`; live calibration set of 17 known good/bad repos,
17/17).

## 2. Confidence tier (High / Medium / Low)

*"How much can I trust this fiche's content?"* — a **data-quality** signal,
separate from relevance.

Computed by `confidence_tier(...)` in
[`src/fiche_schema.py`](../src/fiche_schema.py) from observable signals:

- **Fallback detection** — if the fiche contains the generic phrases emitted when
  the README/LLM was unavailable, it is thin → **Low**.
- **Unverified flag** — an explicit "to be confirmed" / "à confirmer" from the
  model means the claim isn't fully grounded → capped at **Medium**.
- **Enrichment depth** — the length of the "How it works" field distinguishes a
  real README-backed summary from a stub.
- **Metadata completeness** — presence of maturity signals (stars / last-push date).
- **Recency** — a last push within ~18 months; stale data is less certain to
  reflect the project's current reality → capped at **Medium**.

Rules (deliberately simple and explainable):

| Tier | Condition |
|---|---|
| **Low** | fallback phrases present, or "How it works" < 80 chars |
| **High** | "How it works" ≥ 160 chars **and** metadata present **and** recent **and** not flagged unverified |
| **Medium** | everything in between |

Shown as a `◆ High/Medium/Low` badge on each dashboard card. It is a **derived,
presentation-layer signal** — computed from the fiche's own content, not stored in
the markdown and requiring no extra LLM call.

## Why two signals

A project can be highly relevant but have a thin fiche (no accessible README), or
have a rich fiche but be only tangentially relevant. Separating **relevance** from
**confidence** lets a user triage honestly — and keeps Minerva's output auditable,
which matters for a professional/decision-support use case.

> Roadmap: a **confidence v2** (source reliability × freshness × enrichment depth
> × corroboration) is listed in [ROADMAP.md](../ROADMAP.md).

## Honest limits of the relevance score (read this before quoting a number)

The score is a **coarse triage signal — a sort key, not a measurement of the
ecosystem**. Two limits are structural and worth stating plainly:

1. **Provenance is partly circular today.** The current corpus scores come from
   the offline rescore pass, which embeds the **fiche's own LLM-generated prose**
   (not the source description/README). The score therefore partly measures how
   the LLM wrote about a repo, not the repo itself. A **source-first rescore**
   (re-embedding the original description + README) is the planned fix; until
   then, treat one-point differences as noise and ±10 as weakly informative.
2. **Admission breathes at the threshold.** A repo near `min_score` can enter or
   leave the corpus between runs with no real-world change (embedding/recency
   variance — e.g. `bearpi-hm_nano`, 2026-07-31). Corpus membership changes are
   therefore not all "the world moved". Any future change-signal layer must
   label threshold exits distinctly from real removals (see ROADMAP V1.1
   guardrails).
