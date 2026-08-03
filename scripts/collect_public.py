"""Collects the EXACT public web set into publish/ — the deploy manifest, enforced.

docs/DEPLOYMENT.md §1-2 defines what ships and what must never ship. Serving
`output/` directly would leak internals (state.json, ledger, newsletters, raw
fiches). This script makes the manifest executable: an ALLOWLIST copy — nothing
not listed here can ever reach the deploy root by accident.

Usage:
    python scripts/collect_public.py          # build publish/ from output/
    python scripts/collect_public.py --check  # verify publish/ contains no stray file

Deploy `publish/` (GitHub Pages artifact, rsync target, any static host).
publish/ is a derived artifact — git-ignored, rebuilt at will.
"""

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
PUB = ROOT / "publish"

# The whole public surface — exactly docs/DEPLOYMENT.md §1. Anything else in
# output/ (state.json, repo_ledger.json, history.jsonl, newsletters, diffs,
# caches, logs, raw fiches) must NOT be copied. The history artifacts join this
# list only when the signal layer ships and reads them (DEPLOYMENT §3).
ALLOW_FILES = [
    "index.html",
    "dashboard.html",
    "pro.html",
    "legal.html",
    "sitemap.xml",
    "robots.txt",
    "favicon.svg",
    "og.svg",       # rasterize to og.png at deploy; og:image only emitted with a real domain
]
ALLOW_DIRS = {
    "f": "*.html",   # per-fiche pages, EN (.html) + FR (.fr.html)
}


def build() -> int:
    if PUB.exists():
        shutil.rmtree(PUB)
    PUB.mkdir()
    n = 0
    missing = []
    for name in ALLOW_FILES:
        src = OUT / name
        if not src.is_file():
            missing.append(name)
            continue
        shutil.copy2(src, PUB / name)
        n += 1
    for d, pattern in ALLOW_DIRS.items():
        (PUB / d).mkdir()
        for p in sorted((OUT / d).glob(pattern)):
            shutil.copy2(p, PUB / d / p.name)
            n += 1
    print(f"OK : publish/ — {n} file(s) copied (allowlist)")
    if missing:
        print(f"⚠️  missing from output/ (not built?): {', '.join(missing)}")
        return 1
    # Post-copy safety: nothing outside the allowlist may exist in publish/.
    return check(quiet=True)


def check(quiet: bool = False) -> int:
    allowed = {PUB / f for f in ALLOW_FILES}
    strays = []
    for p in PUB.rglob("*"):
        if p.is_dir():
            if p.name not in ALLOW_DIRS:
                strays.append(p)
            continue
        if p.parent == PUB and p not in allowed:
            strays.append(p)
        elif p.parent != PUB and p.parent.name not in ALLOW_DIRS:
            strays.append(p)
    if strays:
        print("❌ stray file(s) in publish/ — the allowlist was bypassed:")
        for s in strays[:20]:
            print(f"   {s.relative_to(ROOT)}")
        return 1
    if not quiet:
        print("OK : publish/ contains only the allowlisted public set")
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify publish/ only")
    args = ap.parse_args()
    return check() if args.check else build()


if __name__ == "__main__":
    raise SystemExit(main())
