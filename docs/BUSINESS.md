# Business & monetization

> How Minerva can become a revenue-generating or sellable asset, without changing
> what it is. This is a working thesis, not a committed plan — it exists to make
> the commercial logic legible to a partner, buyer or investor.

## The asset

Minerva is three things stacked:

1. **An engine** — a tested, incremental pipeline that turns two public APIs into
   structured, bilingual technical intelligence.
2. **A corpus** — a growing, curated, structured dataset of Chinese
   embedded/IoT/robotics/edge-AI projects with decision fields and
   Western-equivalent mapping. This is the part that **compounds**: every run
   makes it deeper and the historical diff more valuable.
3. **A distribution surface** — dashboard + newsletter, i.e. a built-in funnel.

The defensibility is not the code (the APIs are public); it is the **curated org
list + domain-calibrated scoring + the accumulated, time-stamped bilingual
corpus**. Those are hard to replicate and improve with every run.

## Revenue models (ranked by fit)

1. **Managed intelligence subscription (primary).** Hosted dashboard + recurring
   brief for a vertical (e.g. "Edge-AI on Chinese silicon"). Recurring,
   low-touch, content-led. Matches the existing Free / Pro / Enterprise tiers.
2. **Data feed / API.** The fiches as structured JSON for teams that want to pipe
   the intelligence into their own tools (CI dashboards, market-intel platforms).
3. **Custom watch (services-light).** A client supplies target orgs/competitors;
   Minerva runs a bespoke watch and delivers the diff. High willingness-to-pay in
   competitive-intelligence and sourcing.
4. **Periodic reports.** A quarterly *"State of Chinese Embedded / Edge-AI OSS"*
   PDF — a premium artifact and a lead magnet at the same time.
5. **Open-core.** The engine stays open (credibility, contributions); hosting,
   history, API, SSO and support are paid.

## Packaging (aligned with `output/pro.html`)

> Packaging below is **planned scope** (Pro/Enterprise are waitlist-stage, not
> built) — keep it in sync with `output/pro.html`, which is the public source of
> truth. No invented quotas or SLAs: specifics get committed when they exist.

| Tier | Price | For | Includes (planned) |
|---|---|---|---|
| **Free / OSS** | €0 (self-host) | Tinkerers, evaluators | Full engine, self-run pipeline, dashboard, EN+FR. |
| **Pro** | €19 / month | Individual analysts, small teams | Hosted always-fresh dashboard, per-run brief with full diff, read API, historical diff archive. |
| **Enterprise** | Custom | Companies, intel teams | Custom org/competitor watch, integrations, SSO, data export, priority support, quarterly report. |

Pricing rationale: Pro is deliberately "the price of a lunch" to remove friction
and build the newsletter list that feeds Enterprise. Enterprise is where the
value (custom watch + support) is monetized.

## Go-to-market

- **Content-led.** The newsletter *is* the top of funnel; the quarterly report is
  the lead magnet. Publish the corpus openly enough to be discoverable, gate
  freshness/history/custom-watch.
- **Developer credibility first.** Ship a clean, honest open-source repo; earn
  trust with embedded/edge-AI communities (r/embedded, Hacker News, RISC-V and
  OpenHarmony circles) before selling.
- **Targeted outreach** to the ICP in [POSITIONING.md](POSITIONING.md): embedded
  hardware companies, SoC-vendor strategy teams, tech-scouting and CI analysts.
- **Wedge vertical:** start with **Edge-AI on Chinese silicon** (Sophgo, Kendryte,
  ncnn/MNN) — the corpus is already densest there (see the dashboard's domain
  split), the audience is well-defined, and the Western-equivalent mapping is
  most differentiated.

## Market logic (qualitative TAM)

The buyers are not "everyone" — they are teams for whom *missing* a Chinese
hardware/AI development has a real cost: hardware vendors, SoC companies,
industrial/automotive R&D, competitive-intelligence and sourcing functions, and
the consultancies/investors who serve them. That is a **narrow, high-value,
underserved** audience — the right shape for a focused subscription product, not a
volume play.

## Why now

- China's embedded/RISC-V/edge-AI open-source output is accelerating and
  increasingly strategic to Western BOM, competitive and standards decisions.
- LLMs make structured, bilingual enrichment cheap enough (~$0.01 per bilingual repo pair) to run
  as a continuous product for the first time.
- No incumbent covers Gitee *and* GitHub with domain-calibrated, decision-ready,
  bilingual output.

## Risks & honest caveats

- **Key-person / single-source risk** — mitigated by the engine being tested,
  documented and reproducible.
- **Source ToS / access** — addressed and bounded in [SOURCES.md](SOURCES.md);
  the product only touches public APIs within their published limits.
- **LLM accuracy** — mitigated by the prompt's "to be confirmed" rule and the fact
  that every fiche links back to the primary source for verification.
- **Narrow audience** — a feature (focus, willingness to pay) more than a bug, but
  it caps the volume ceiling; the play is value per account, not scale.

See [ROADMAP.md](../ROADMAP.md) for what must ship to make each tier real.
