# Data sources & compliance register

> Per-source operational register: **how** we access each source, whether it's an
> **API or scraping**, what we **republish**, the **risks**, and the **decision**.
> This is the authoritative source-by-source table. For the narrative posture and
> IP logic, see [docs/SOURCES.md](docs/SOURCES.md).

## Product principle (what we republish)

Minerva is a **discovery, curation and translation engine — not a mirror and not
an aggressive scraper.** For every project we republish only the **minimum
necessary**:

- title (`owner/repo`),
- a short original EN/FR summary (generated, not copied),
- useful public metadata (stars, forks, last push, language, domain),
- tags,
- a relevance/confidence score,
- **a direct link back to the original source.**

We never mirror repositories, never republish source code, and never bulk-copy
README text. Every fiche sends the user to the origin.

## Integrated sources (used by the V1 pipeline)

| Source | Access method | API / scraping | Auth | What we read | What we republish | Rate-limit posture | Risks | Decision |
|---|---|---|---|---|---|---|---|---|
| **Gitee** (priority) | Official REST **API v5** (`gitee.com/api/v5`) | ✅ API only | `GITEE_TOKEN` | Public repo metadata + public README | Title, summary, metadata, tags, score, link | Self-capped **4500/h** (official 5000) + spacing; single documented retry on 403 WAF, no evasion | Gitee `/search` broken server-side (workaround: curated org list + seeds); ToS may restrict commercial use at scale | **Integrated.** Priority source. |
| **GitHub** | Official REST **API v3** (`api.github.com`) | ✅ API only | `GITHUB_TOKEN` (optional) | Public repo metadata + public README | Same minimal set | Self-capped **4500/h** auth (55/h anon), honors `X-RateLimit-*` | Anonymous 60/h too low for full runs; captures Chinese orgs absent from Gitee | **Integrated.** Captures GitHub-only Chinese vendors (Bouffalo, Sophgo, Unitree, Kendryte, Allwinner). |
| **Anthropic Claude** | Official API (Haiku 4.5) | ✅ API | `ANTHROPIC_API_KEY` | Receives description + truncated README excerpt | — (produces the summary) | SDK retry/backoff | LLM may be imperfect → "to be confirmed" convention + source link for verification | **Integrated.** Enrichment only; no user/private data sent. |

All three are **official documented APIs — no HTML scraping is used anywhere in
the pipeline.** Enforced in [`src/fetcher.py`](src/fetcher.py),
[`src/github_fetcher.py`](src/github_fetcher.py), [`src/translator.py`](src/translator.py).

## Evaluated / candidate sources (not yet integrated)

Realistic, defensible ingestion plan for widening coverage. Each requires an
explicit compliance decision **before** integration.

| Source | What it is | Access status | Risk / blocker | Decision |
|---|---|---|---|---|
| **GitCode** (`gitcode.com`, CSDN) | Large Chinese code host | Partial/undocumented API; login-gated areas | ToS + API stability unknown; risk of needing scraping | **Candidate (priority raised 2026-07-30)** — evaluate official API + ToS first. Do not scrape. |
| **GitLink / Trustie** (`gitlink.org.cn`) | Open-source collaboration platform (education/gov backed) | Has a documented API | Coverage overlap with Gitee; API maturity to confirm | **Candidate — API-first integration, low risk.** |
| **AtomGit** (`atomgit.com`, OpenAtom Foundation) | Newer foundation-backed host | API emerging | Early-stage; coverage TBD | **Candidate (priority raised 2026-07-30)** — monitor; integrate when API stable. |

> **Empirical finding (2026-07-30 full harvest):** of 3,660 repos enumerated
> across the 22 watched Gitee orgs, **2,313 had no push in >2 years** — including
> **1,617 OpenHarmony repos** (openharmony + -sig + -tpc). The OpenAtom/OpenHarmony
> ecosystem has effectively migrated off Gitee (toward AtomGit/GitCode), and
> several hardware vendors publish primarily on GitHub. Consequence: Gitee alone
> no longer carries the fresh wedge supply; the GitHub org harvest (needs
> `GITHUB_TOKEN`) and an AtomGit/GitCode connector are the coverage path. This is
> why the two candidates above moved up in priority.
| **Vendor / CSDN portals** | Blog/portal pages, some vendor SDK pages | HTML only, no stable public API | Would require scraping; against product principle | **Excluded** unless an official feed/API appears. |
| **Self-hosted Gitea instances (vendors)** | Per-vendor code servers | Gitea REST API (if public) | Case-by-case ToS; fragmentation | **Case-by-case**, API-only, only if publicly offered. |

**Integration rule:** a new source is added only if (1) it offers an official API
or an explicitly authorized feed, (2) its ToS permits reading public metadata,
(3) we can respect its rate limits, and (4) we still only republish the minimal
set above with a link back. Any source failing these stays out.

## Compliance summary

- Official APIs only, authenticated, **under** published rate limits, no evasion.
- Public, factual metadata + public READMEs only — no private, personal or
  paywalled data.
- No code redistribution; original summaries + links back to every source.
- **Takedown-friendly:** remove an entry from `config/sources.json`; fiches are
  regenerable and deletable per repo.
- Provider ToS can change — a commercial deployment must re-review Gitee/GitHub
  (and any new source) ToS for the specific use.

_Last reviewed: 2026-07-29._
