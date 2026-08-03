# Security

Minerva touches only official, public APIs (see
[data-sources-and-compliance.md](data-sources-and-compliance.md)) and stores no
end-user data. The main security surface is therefore **secret handling** — the
API keys the pipeline needs at runtime.

## How secrets are handled

- All keys live in a local **`.env`** at the repo root: `GITEE_TOKEN`,
  `ANTHROPIC_API_KEY`, and optionally `GITHUB_TOKEN`.
- `.env` (and every `.env.*` variant) is **gitignored** — only `.env.example`
  (placeholders) is tracked. See [`.gitignore`](.gitignore).
- Keys are never written to any generated artifact (fiches, dashboard,
  newsletter, site, logs). This is enforced two ways:
  - **`scripts/secret_scan.py`** — run it locally before any push.
  - **CI guard** — the GitHub Actions workflow runs the same scan and fails the
    build if a key pattern appears in a committable file or a real `.env` is
    tracked.

## ⚠️ Before your first public push (required)

This repository is not yet a git repo, so there is no history to leak — but do
this in order:

1. **Rotate the keys that were used during development.** The local `.env` holds
   live `GITEE_TOKEN` and `ANTHROPIC_API_KEY` that have been used on this machine.
   Before going public, **revoke and regenerate them** in their dashboards
   (Gitee → Settings → Private tokens; Anthropic Console → API keys). This is a
   manual action only you can take — the project cannot rotate keys for you.
2. **Run the secret scan:** `python scripts/secret_scan.py` (must print OK).
3. **Confirm `.env` is ignored:** after `git init && git add -A`, run
   `git status` and verify **no `.env*` file is staged** (only `.env.example`).
4. **Use a least-privilege `GITHUB_TOKEN`** for the harvest: a read-only classic
   PAT with no scopes, or a fine-grained token limited to public-repo read.
5. **Never paste keys into issues, PRs, logs, or screenshots.**

## Reporting a vulnerability

Please report security issues privately (e.g. a GitHub security advisory or a
direct message to the maintainer) rather than opening a public issue. Include
steps to reproduce and the affected version. We aim to acknowledge within a few
days.

## Scope notes

- No code from watched repositories is redistributed — Minerva stores metadata
  and original summaries, and links back to the source.
- Provider Terms of Service can change; a commercial deployment should re-review
  Gitee/GitHub (and any new source) ToS for the specific use.
