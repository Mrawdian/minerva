"""Removes orphan markdown fiches: present on disk but absent from state.json.

state.json is the source of truth (canonical tracked repos). Any .md in
output/fiches/ or output/fiches_fr/ that matches no repo in state.json is
considered an orphan (old run, hard filter added later, repo archived/deleted
on Gitee, etc.). Both language sets are cleaned together so a DELETED repo
disappears from EN and FR alike.

No network calls. No LLM calls. Irreversible action — no dry-run mode
requested, but easy to add via --dry-run if needed.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = ROOT / "output" / "state.json"
FICHES_DIRS = [
    ("EN", ROOT / "output" / "fiches"),
    ("FR", ROOT / "output" / "fiches_fr"),
]


def slugify(full_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-]", "_", full_name.replace("/", "_"))


def _clean_dir(label: str, fiches_dir: Path, expected_files: set[str]) -> tuple[int, int]:
    """Removes orphans in one language directory. Returns (on_disk, deleted)."""
    if not fiches_dir.is_dir():
        print(f"[{label}] répertoire absent ({fiches_dir}) — ignoré")
        return 0, 0

    on_disk = sorted(fiches_dir.glob("*_fiche.md"))
    orphans = [p for p in on_disk if p.name not in expected_files]

    print(f"[{label}] fiches sur disque : {len(on_disk)} — orphelines : {len(orphans)}")

    deleted = 0
    for p in orphans:
        try:
            p.unlink()
            print(f"[{label}] Supprimé : {p.name}")
            deleted += 1
        except OSError as exc:
            print(f"[{label}] ERREUR suppression {p.name} : {exc}", file=sys.stderr)
    return len(on_disk), deleted


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    if not STATE_FILE.is_file():
        print(f"ERREUR : state.json introuvable à {STATE_FILE}", file=sys.stderr)
        return 1

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    tracked = set(state.get("repos", {}).keys())
    expected_files = {f"{slugify(fn)}_fiche.md" for fn in tracked}
    print(f"Repos suivis (state) : {len(tracked)}\n")

    total_on_disk = 0
    total_deleted = 0
    for label, fiches_dir in FICHES_DIRS:
        on_disk, deleted = _clean_dir(label, fiches_dir, expected_files)
        total_on_disk += on_disk
        total_deleted += deleted

    print()
    print("--- Bilan (EN + FR) ---")
    print(f"Avant nettoyage       : {total_on_disk} fiches")
    print(f"Orphelines supprimées : {total_deleted}")
    print(f"Restantes             : {total_on_disk - total_deleted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
