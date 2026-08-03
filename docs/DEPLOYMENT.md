# Deployment manifest — what ships, what never ships (V1)

> Minerva builds into `output/`, but **`output/` is not the deploy root**. It also
> holds internal artifacts that must never be served. This manifest defines the
> exact public set for the V1 public release. Nothing here is pushed yet.

## 1. What MUST be published (the V1 public web set)

Exactly these paths from `output/`, and nothing else:

| Path | Why |
|---|---|
| `index.html` | Landing (funnel entry) |
| `dashboard.html` | The proof — fiche-first explorer |
| `pro.html` | Plans + waitlist |
| `legal.html` | Privacy, provenance, corrections/removals, contact |
| `f/*.html` | One shareable decision page per fiche — **EN (`.html`) + FR (`.fr.html`)** |
| `favicon.svg` | Brand tab icon (self-contained SVG) |
| `og.png` | Social card — rasterized from the shipped `og.svg` at deploy |
| `sitemap.xml` | SEO — **only meaningful with a real `MINERVA_SITE_URL`** |
| `robots.txt` | Crawl policy |

That is the whole public surface. The `f/` pages already present each fiche's
decision layer, so the raw markdown corpus does not need to be served.

## 2. What must NEVER be published

Must be excluded from the deploy root (some are already git-ignored, but a naive
"serve `output/`" would still leak them):

| Path | Reason |
|---|---|
| `state.json` | Internal pipeline ledger — not a public artifact |
| `embeddings_cache.json` | ~9 MB internal cache (git-ignored) |
| `diff_*.md` | Per-run internal diff (git-ignored) |
| `logs/` | Run logs (git-ignored) |
| `newsletter_*.html` / `*.txt` | Distributed via the email provider, not the web root |
| `dispatch_*.md` | Editorial drafts (git-ignored, and stale ones archived) |
| `fiches/` , `fiches_fr/` | Raw markdown source — kept in the git repo, not served (robots already disallows them defensively) |
| `.env`, any secret | Never — git-ignored; rotation is a pre-push step |

## 3. The history artifact — a deliberate exception, later

`repo_ledger.json` and `history.jsonl` (Track 2) are **committed to the git repo**
(they are the durable memory) but are **not served in V1** — there is no signal
layer yet. When the Phase 3 signal strip ships and reads them client-side, they
**join the public web set** (they carry only public-derived metadata — repo names,
dates, scores, confidence — nothing sensitive). Until then: excluded.

## 4. How to enforce it (recommended)

**Built: `scripts/collect_public.py`** — the manifest, enforced as an allowlist
copy into `publish/` (git-ignored, derived, rebuilt at will):

```
python scripts/collect_public.py          # output/ → publish/ (allowlist only)
python scripts/collect_public.py --check  # fail if any stray file is present
```

Verified: 218 files (8 root + 105 EN + 105 FR fiche pages), zero internals
(`state.json`, ledger, history, newsletters, raw fiches all excluded by
construction). Deploy `publish/` — never `output/`.

## 5. Hard preconditions before any public push

Owner-side and blocking:

1. **Rotate keys** — Gitee + Anthropic dev keys (see `SECURITY.md`), then run
   `scripts/secret_scan.py`. After the push, add them as **GitHub repo secrets**
   (`GITEE_TOKEN`, `ANTHROPIC_API_KEY`, `GITHUB_API_TOKEN`) to activate the
   weekly workflow (`.github/workflows/scheduled-run.yml` — inert until then).
2. **Set a real `MINERVA_SITE_URL`** and rebuild — re-enables canonical /
   `og:url` / hreflang / sitemap `<loc>` / robots `Sitemap:` (all suppressed in
   placeholder mode). Optionally set `MINERVA_CONTACT`.
3. **Create the owner-controlled Buttondown account** and rebuild with
   `MINERVA_NEWSLETTER=<handle>` — until then every email form renders disabled
   ("sign-up opens at launch"); a live form posting to an unowned account would
   leak visitors' emails.

Only after these, and after the fresh launch run + review, does `publish/` go live.

## 6. Definition of "ready to publish" (owner doctrine, 2026-07-31)

**Stop-ship rule: no push while any honesty betrayal exists.** Publish only when
every box is true — not "perfect", but *coherent with its own law*:

- [ ] **Cadence decision written and 100% of copy aligned.** Implemented
      structurally: default builds promise NO cadence ("after each corpus run");
      the word "weekly" can only be produced by the weekly CI workflow itself
      (`MINERVA_CADENCE=weekly`, set nowhere else). A manual build cannot
      over-promise by construction.
- [ ] **No email ever reaches an account we don't control.** `MINERVA_NEWSLETTER`
      unset ⇒ forms render disabled; verified in the live DOM.
- [ ] **No numeric claim contradicted by the repo.** ($0.005, 140 fiches,
      "weekly incremental execution", "EU-hosted", "15 watched", Q3-2026,
      "guaranteed", "10k req/month", "99.5% SLA" — all purged or requalified
      as "Planned scope".)
- [ ] **No absurd public ranking.** Vitrine curated (decision-grade only) +
      utility demotion in the score formula (`UTILITY_PENALTY`, applied by the
      fresh run). **Manual check of the new top-10 after the fresh run — a
      hardware person must not laugh** — is part of the pre-push review.
- [ ] **FR/EN says exactly what is consumable.** 106 FR twin pages served,
      EN↔FR toggle, hreflang.
- [ ] **Minimal privacy page since we capture emails.** `legal.html`, linked
      from every page, FAQ aligned, no invented hosting claims.
- [ ] **"as of" coherent with `state.json`.** Status-line and footer dates come
      from `last_run`; fresh run immediately before push.
