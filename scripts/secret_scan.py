"""Local secret scan — run before any public push.

Fails (exit 1) if a real secret pattern appears in a file that git would commit,
or if a real .env is not ignored. Mirrors the CI guard in .github/workflows/ci.yml
so problems are caught locally first.

Usage:
    python scripts/secret_scan.py
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# High-signal secret shapes. Kept narrow to avoid false positives on docs that
# legitimately mention "sk-ant-..." as a placeholder (those use the literal
# words, not a 20+ char key body).
PATTERNS = {
    "Anthropic API key": re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    "GitHub classic PAT": re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    "GitHub fine-grained PAT": re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    "Gitee access_token in URL": re.compile(r"access_token=[A-Za-z0-9]{20,}"),
}

# Directories never scanned (regenerable / vendored / local-only).
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "output", "data"}
# .env* are gitignored and hold the real keys — not committed, so not scanned
# for content; their *tracking* status is checked separately below.
SKIP_FILES = {".env"}


def _tracked_or_committable(path: Path) -> bool:
    """True if the file would end up in a commit (not gitignored)."""
    rel = path.relative_to(ROOT)
    if any(part in SKIP_DIRS for part in rel.parts):
        return False
    if path.name in SKIP_FILES or path.name.startswith(".env"):
        return False
    return True


def main() -> int:
    findings: list[str] = []

    # 1. No real .env variant should be git-trackable.
    if (ROOT / ".git").exists():
        try:
            out = subprocess.run(
                ["git", "-C", str(ROOT), "ls-files", "--", ".env", ".env.*"],
                capture_output=True, text=True, check=False,
            ).stdout.strip()
            tracked = [f for f in out.splitlines() if f and f != ".env.example"]
            if tracked:
                findings.append(f"env file(s) TRACKED by git: {tracked}")
        except Exception:
            pass  # no git yet — nothing tracked

    # 2. Scan committable files for secret bodies.
    scanned = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or not _tracked_or_committable(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        scanned += 1
        for label, pat in PATTERNS.items():
            if pat.search(text):
                findings.append(f"{label} in {path.relative_to(ROOT)}")

    if findings:
        print("SECRET SCAN FAILED:")
        for f in findings:
            print(f"  - {f}")
        return 1

    print(f"Secret scan OK — {scanned} committable files clean, no env leak.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
