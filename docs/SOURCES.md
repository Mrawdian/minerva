# Sources, access method & compliance

> What data Minerva touches, how it accesses it, and the compliance posture.
> Written so a partner, buyer or legal reviewer can assess the data provenance in
> minutes. Everything here is enforced in code — see the references.
>
> 👉 For the **per-source operational register** (access method, API-vs-scraping
> status, risks and decision for each integrated *and candidate* source), see
> [`data-sources-and-compliance.md`](../data-sources-and-compliance.md). This
> document is the narrative posture behind that register.

## Data sources

| Source | Endpoint | Auth | What is read |
|---|---|---|---|
| **Gitee** | Official REST API v5 (`gitee.com/api/v5`) | `GITEE_TOKEN` (personal token) | Public repository metadata + public README |
| **GitHub** | Official REST API v3 (`api.github.com`) | `GITHUB_TOKEN` (optional PAT) | Public repository metadata + public README |
| **Anthropic** | Claude API (Haiku 4.5) | `ANTHROPIC_API_KEY` | Receives a repo description + cleaned README excerpt to generate the summary fields |

Both code sources are **official, documented REST APIs** — not HTML scraping.
Access is in [`src/fetcher.py`](../src/fetcher.py) (Gitee) and
[`src/github_fetcher.py`](../src/github_fetcher.py) (GitHub).

## What is and isn't collected

**Collected** — public, factual repository metadata only:
- `full_name`, `description`, primary `language`, `stargazers_count`,
  `forks_count`, `pushed_at`, `default_branch`, `archived` flag, and the public
  README text.

**Never collected:**
- Private repositories, private user data, emails, or any authenticated-only content.
- Credentials, secrets, or paywalled material.
- Personal data beyond what is intrinsically public in an org/repo listing (the
  org handle and public counts). No profiling of individuals.

## Rate limiting — we stay *under* the published limits

Minerva self-imposes caps **below** each provider's official limit and spaces
requests, precisely so it behaves as a well-mannered API client, not a scraper:

- **Gitee:** official limit 5000 req/h → Minerva caps at **4500 req/h** with a
  minimum spacing between requests ([`fetcher.configure`](../src/fetcher.py)).
- **GitHub:** official limit 5000 req/h authenticated / 60 anonymous → Minerva
  caps at **4500 / 55** and honors `X-RateLimit-Remaining` / `Reset`
  ([`github_fetcher.configure`](../src/github_fetcher.py)).
- A thread-safe sliding-window limiter enforces the hourly cap even under
  parallelism.

The only retry-on-block is a **single, documented** retry after a Gitee `403`
(Baidu WAF), with a fixed wait — resilience against a transient block, **not**
evasion. There is no header spoofing, no proxy rotation, no CAPTCHA handling.

## Filtering — quality and respect built in

The pipeline deliberately drops noise and non-original content:
- `third_party_*` ports and unwatched `mirrors/*` (not original work),
- pure forks on GitHub (`SKIP_FORKS`),
- archived / abandoned repos (no push > 2 years, `archived` flag, or Gitee
  `关闭` status).

## Intellectual property & attribution

- **No code redistribution.** Minerva stores repository *metadata* and its own
  *original derived summaries* (the fiches). It does not copy, host or
  redistribute the projects' source code.
- **Original work.** The fiche prose (Problem solved, How it works, Chinese
  specificity, Western equivalent) is generated, not copied from the README.
- **Attribution by design.** Every fiche links back to the primary source
  (`Gitee:` / `GitHub:` line), so users always reach and credit the origin.
- **Upstream licenses are respected.** Each referenced project keeps its own
  license; Minerva's own code is Apache-2.0.

## LLM data handling

Only a repository's public description and a **truncated, cleaned** README excerpt
(badges/license/long code blocks stripped, ~3500 chars max) are sent to the
Claude API to produce the summary fields. No customer or private data is involved.
The prompt instructs the model to write *"to be confirmed"* rather than invent
facts, and every fiche links to the source for verification — reducing the risk of
unverifiable claims.

## Compliance posture (summary)

- Official APIs only, within published rate limits, authenticated.
- Public, factual metadata + public READMEs only.
- No evasion, no private/personal data harvesting, no code redistribution.
- Attribution and links back to every source.
- **Takedown-friendly:** any project can be excluded from a run by removing it
  from `config/sources.json`; fiches are regenerable and deletable per repo.

## Honest open questions

- Provider Terms of Service can change; a production/commercial deployment should
  re-review Gitee and GitHub ToS for the specific use (redistribution of derived
  summaries at scale, API commercial-use clauses).
- Some vendors publish only outside Gitee/GitHub (vendor portals); those are
  intentionally out of scope until a compliant access path is confirmed.
- Export-control / geopolitical sensitivity: Minerva surfaces **public** technical
  information only and takes no position on end-use.
