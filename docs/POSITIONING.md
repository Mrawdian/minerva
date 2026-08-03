# Positioning

> Who Minerva is for, the problem it removes, and why it is different.
> This document is the reference for the product framing used in the README,
> the landing page and the newsletter.

## One-line value proposition

**Minerva turns the Chinese open-source hardware ecosystem — most of it in
Chinese, fragmented across Gitee and GitHub — into decision-ready English/French
technical intelligence you can monitor over time.**

## The problem

The Chinese ecosystem ships an enormous amount of embedded, IoT, robotics and
edge-AI code: RTOSes (RT-Thread, TencentOS-tiny, AliOS-Things), NPU/edge-AI SDKs
(ncnn, MNN, Kendryte, Sophgo tpu-mlir), RISC-V toolchains, robotics stacks
(Unitree), vendor BSPs (Rockchip, Allwinner, Bouffalo). For a Western engineering
or intelligence team this ecosystem is effectively **dark matter**:

1. **Language** — most descriptions and READMEs are in Mandarin.
2. **Fragmentation** — it is spread across Gitee *and* GitHub, over dozens of
   organizations, with no unified index. Gitee's own repository search is broken
   server-side.
3. **No discovery layer** — GitHub-trending-style tools ignore Gitee entirely,
   and none map Chinese projects to their Western equivalents.
4. **Signal/noise** — the interesting frameworks are buried under forks, mirrors,
   demos and abandoned repos.

The cost of this blind spot is concrete: missing a maturing RISC-V toolchain, an
edge-AI runtime that out-performs the one you ship, or a competitor quietly
open-sourcing its robotics stack — until it is already an industry fact.

## What Minerva does

Minerva is a **continuous technology-watch engine**, not a one-shot scrape:

- **Collects** public repository metadata + READMEs from Gitee and GitHub across a
  curated set of Chinese hardware/embedded organizations.
- **Scores** each repo semantically against four domains (Embedded, IoT, Robotics,
  Edge AI), filtering mirrors, forks and abandoned projects.
- **Enriches** the relevant ones into structured, bilingual **fiches** — Problem
  solved, How it works, Chinese specificity, **Western equivalent**, Maturity —
  the fields a decision-maker actually needs.
- **Presents** the corpus as an interactive dashboard + an email-ready newsletter,
  and tracks changes over time via an incremental diff.

The output is **decision-ready intelligence**, not a repo list.

## Who it is for (ICP)

| Segment | Job to be done |
|---|---|
| **Embedded / IoT hardware companies** | Evaluate Chinese RTOS/BSP/SDK maturity before designing them into a product; benchmark vs FreeRTOS/Zephyr. |
| **Semiconductor / SoC vendors (DevRel, strategy)** | Track competitor SDKs and the RISC-V / edge-AI toolchain landscape. |
| **R&D / innovation / tech-scouting teams** | Systematic scouting of Chinese alternatives in robotics, edge-AI, connectivity. |
| **Competitive & market intelligence analysts** | Monitor a target company's open-source footprint and its evolution over time. |
| **Consultancies / analysts / investors** | Due diligence on the OSS depth of Chinese hardware/AI players. |
| **Standards & compliance teams** | Follow OpenHarmony, RISC-V and Chinese-standard ecosystem momentum. |

## Core use cases

1. **Technology scouting** — find the Chinese equivalent/alternative to a Western
   framework (the fiche's *Western equivalent* field is the bridge).
2. **Competitive intelligence** — watch a competitor's public repos and get a
   dated diff of what moved, run over run.
3. **Sourcing / BOM decisions** — assess a chipset vendor's SDK maturity before
   committing a design.
4. **Standards tracking** — quantify OpenHarmony / RISC-V ecosystem activity.
5. **Due diligence** — measure a company's real open-source output.
6. **Edge-AI benchmarking** — line up inference runtimes (ncnn, MNN, TFLite,
   tpu-mlir) with maturity signals.

## Why Minerva is different

- **Vertical, not generic.** Focused on embedded / IoT / robotics / edge-AI —
  calibrated scoring, not repo-trending noise.
- **Gitee *and* GitHub.** Captures Chinese-only-on-Gitee projects that
  English-language tooling never sees, plus the GitHub-only vendors.
- **Structured, bilingual intelligence.** LLM-generated decision fields with an
  explicit **Western-equivalent mapping** — a bridge no raw repo list provides.
- **Monitoring, not snapshot.** Incremental `state.json` diff makes it a product
  you subscribe to, not a report you read once.
- **A corpus that compounds.** Every run enriches a durable, structured,
  bilingual dataset — an asset that grows more valuable over time.

## What Minerva is *not*

- Not a general-purpose GitHub trending tool.
- Not a chatbot or a generic LLM wrapper.
- Not a code redistributor — it links back to sources and publishes original
  summaries and metadata only (see [SOURCES.md](SOURCES.md)).
- Not a scraper of private, personal or paywalled data.
