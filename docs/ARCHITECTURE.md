# Architecture

> How Minerva is built, for a technical reviewer. The design goal is a small,
> testable, incremental pipeline with clean seams between collection, scoring,
> enrichment and presentation.

## Data flow

```
Gitee API v5 ┐
             ├─► Collect ─► Score ─► Enrich ─► Outputs
GitHub REST ┘   (fetch)   (semantic) (Claude)   ├─ fiches EN/FR (output/fiches[,_fr]/)
                                                 ├─ dashboard.html
                                                 └─ newsletter_*.{html,txt}
                     ▲                                    │
                     └──────── state.json (diff) ◄────────┘
```

See [`docs/assets/pipeline.svg`](assets/pipeline.svg) for the diagram used in the README.

## Modules

| Module | Responsibility |
|---|---|
| [`src/fetcher.py`](../src/fetcher.py) | Gitee API v5 client: pagination, retry, thread-safe rate-limit, README fetch. |
| [`src/github_fetcher.py`](../src/github_fetcher.py) | GitHub REST v3 client, same public surface, normalizes repos to the shared schema and tags `_minerva_source="github"`. |
| [`src/analyzer.py`](../src/analyzer.py) | Semantic scoring: cosine similarity of repo text vs domain definitions, hybrid keyword-anchor admission, hard filters, global bonuses. |
| [`src/embedder.py`](../src/embedder.py) | Lazy `sentence-transformers` wrapper + on-disk embedding cache. |
| [`src/translator.py`](../src/translator.py) | Deterministic extractors + Claude Haiku enrichment; **i18n** fiche generation (EN default / FR). |
| [`src/fiche_schema.py`](../src/fiche_schema.py) | Pydantic source-of-truth for parsing/serializing fiches (bilingual, round-trip safe). |
| [`src/pipeline.py`](../src/pipeline.py) | Orchestration: fetch → filter → enrich, incremental diff, parallel LLM calls, state persistence. |

Presentation is decoupled in `scripts/`:
[`build_dashboard.py`](../scripts/build_dashboard.py),
[`build_newsletter.py`](../scripts/build_newsletter.py),
[`build_site.py`](../scripts/build_site.py),
[`rescore.py`](../scripts/rescore.py) (offline, LLM-free),
[`build_lang_fiches.py`](../scripts/build_lang_fiches.py) (one-shot migration/backfill
tool — the pipeline itself now maintains both language sets natively).

## Key design decisions

- **Shared repo schema across sources.** GitHub repos are normalized to the exact
  dict shape Gitee produces, so scoring and enrichment are source-agnostic. Adding
  a third source means implementing one `configure / list_all_repos_by_owner /
  fetch_repo / fetch_readme` surface — nothing downstream changes.
- **Fiche as the interface.** Every output (dashboard, newsletter, site) is built
  from the markdown fiches. The fiche format is a stable, parsable contract
  (`fiche_schema.Fiche`), which keeps presentation and generation independent.
- **Incremental by default.** `state.json` stores `pushed_at` per repo; each run
  computes NEW / MODIFIED / DELETED and only calls the LLM for what changed —
  turning a scrape into a monitoring product and keeping cost near zero per run.
- **Deterministic vs LLM split.** Objective fields (maturity, language, score,
  domain, source URL) are computed locally; only the analytical prose is LLM-
  generated. This bounds cost, latency and hallucination surface.
- **i18n as data, not forks.** Language is a parameter; labels/prompts/values are
  table-driven (`FIELD_LABELS`, `MATURITY_LABELS`, `DOMAIN_DISPLAY`), and the
  schema parses both languages. English is default, French is language 2.
- **Native bilingual runs, single source of facts.** `generate_fiche_pair` does
  ONE English LLM generation (the facts) + ONE EN→FR prose translation, then
  composes both markdowns deterministically (`_compose_fiche`) — the two sets
  cannot drift. The pipeline saves both per repo; BOOTSTRAP requires both fiches
  on disk (self-healing if one is missing); orphan cleanup covers both sets.

## Extension points

- **New watched org** → add to `config/sources.json` (`comptes_gitee` /
  `comptes_github`) or a specific repo to `seeds_*`.
- **New domain** → add a definition + keywords to `config/domains.json`; re-score
  offline for $0 with `scripts/rescore.py`.
- **New source** → implement the fetcher surface above; the rest is transparent.

## Reliability & testing

- **96 unit tests** (`pytest`) across fetcher, github_fetcher, analyzer, pipeline,
  translator and fiche_schema, plus a bilingual generate/parse round-trip.
- **CI** on GitHub Actions: config check, `compileall`, full test run.
- **Robustness by construction:** any per-repo error is logged and never breaks a
  run; owners with partial fetches are protected from false "deletion" detection;
  the `.env` loader tolerates quotes/whitespace; embeddings and TF backends are
  guarded for portability.

## Cost & performance

- Embeddings run locally (no API cost); the model downloads once (~118 MB) and is
  cached on disk between runs.
- LLM: ~$0.01 per repo (EN generation + FR translation, Haiku 4.5); a full bootstrap is ~$2-4, and
  incremental runs cost only for changed repos.
