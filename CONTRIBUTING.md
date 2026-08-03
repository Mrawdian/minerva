# Contributing to Minerva

Thanks for your interest. Minerva is a focused technology-watch engine for the
Chinese open-source embedded / IoT / robotics / edge-AI ecosystem. Contributions
that sharpen that focus — coverage, scoring quality, presentation, docs — are very
welcome. Please keep changes aligned with the project's scope (see
[docs/POSITIONING.md](docs/POSITIONING.md)).

## Setup

```bash
git clone <repo-url> minerva && cd minerva
pip install -r requirements.txt
python -m pytest -q          # 96 tests should pass
```

For runs that hit the network you need a `.env` at the root (see the README):
`GITEE_TOKEN`, `ANTHROPIC_API_KEY`, and optionally `GITHUB_TOKEN`. You do **not**
need any token to run the tests or open the pre-generated dashboard.

## Common contributions

- **Add a watched organization** → `config/sources.json` (`comptes_gitee` /
  `comptes_github`), or a specific repo in `seeds_gitee` / `seeds_github`. Verify
  the org/repo exists before adding.
- **Tune a domain** → edit its `definition` / keywords in `config/domains.json`,
  then re-score offline for $0: `python scripts/rescore.py`.
- **Add a data source** → implement the fetcher surface (`configure`,
  `list_all_repos_by_owner`, `fetch_repo`, `fetch_readme`) as in
  `src/github_fetcher.py`; downstream code is source-agnostic.

## Ground rules

- **Keep the DNA.** No general-purpose repo trending, no chatbot, no unvetted
  sources. See the invariants in [docs/POSITIONING.md](docs/POSITIONING.md) and
  the compliance posture in [docs/SOURCES.md](docs/SOURCES.md).
- **Tests pass and stay green.** Add tests for new behavior; network and LLM calls
  must be mocked in tests (see `tests/test_github_fetcher.py` for the pattern).
- **Match the surrounding style.** English code comments and docstrings; runtime
  log messages may stay as they are.
- **Respect sources.** No scraping, no rate-limit evasion, no private data.

## Pull requests

1. Branch from the default branch.
2. Keep the change focused; describe *what* and *why*.
3. Ensure `python -m pytest -q` and `python -m compileall src scripts tests` pass.
4. Run `python scripts/secret_scan.py` before pushing — it must print OK (also
   enforced in CI). See [SECURITY.md](SECURITY.md).
4. Update docs/CHANGELOG when behavior or interfaces change.

## Reporting issues

Include: what you ran, what you expected, what happened, and (for pipeline issues)
the relevant lines from `output/logs/`. For a data-quality issue on a specific
fiche, link the fiche and the source repo.
