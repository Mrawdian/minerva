"""
Offline validation of the analyzer → translator chain on Phase 0 data.

No network calls: reads data/raw/ and data/readmes/, produces fiches in output/fiches/.
"""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

import analyzer  # noqa: E402
import translator  # noqa: E402


RAW_DIR = ROOT / "data" / "raw"
READMES_DIR = ROOT / "data" / "readmes"
FICHES_DIR = ROOT / "output" / "fiches"
SOURCES_PATH = ROOT / "config" / "sources.json"


def find_readme(slug: str) -> tuple[str | None, str | None]:
    """Cherche un README dans data/readmes/ pour le slug donné.

    Ordre :
      1. {slug}_README.md, {slug}_readme.md, {slug}.md (patterns explicites)
      2. Tout fichier dont le stem commence par slug

    Returns (contenu, nom_fichier) ou (None, None).
    """
    explicit_candidates = [f"{slug}_README.md", f"{slug}_readme.md", f"{slug}.md"]
    for name in explicit_candidates:
        p = READMES_DIR / name
        if p.is_file():
            return p.read_text(encoding="utf-8"), p.name

    for p in sorted(READMES_DIR.glob(f"{slug}*")):
        if p.is_file():
            return p.read_text(encoding="utf-8"), p.name

    return None, None


def main() -> int:
    domains = analyzer.load_domains()
    sources = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    watched_owners = sources.get("comptes_gitee", [])
    min_score_watched = int(sources.get("min_score", 15))
    min_score_unwatched = min_score_watched + 5
    watched_set = set(watched_owners)

    json_files = sorted(RAW_DIR.glob("*.json"))
    total = len(json_files)

    pertinents = 0
    fiches_generees = 0
    ignores = 0

    print(f"Traitement de {total} repos depuis {RAW_DIR}")
    print(f"Comptes surveillés (seuil {min_score_watched}) : {watched_owners}")
    print(f"Comptes non surveillés (seuil {min_score_unwatched})\n")

    for jf in json_files:
        slug = jf.stem
        repo = json.loads(jf.read_text(encoding="utf-8"))
        full_name = repo.get("full_name", slug)

        score_info = analyzer.score_repo(repo, domains, watched_owners=watched_owners)
        score = score_info["score_total"]
        owner = full_name.split("/", 1)[0]
        threshold = min_score_watched if owner in watched_set else min_score_unwatched

        if score < threshold:
            print(f"⏭️  {full_name} — Score: {score} (seuil {threshold}) — ignoré")
            ignores += 1
            continue

        if translator.is_archived(repo):
            print(f"📦 {full_name} — Score: {score} — Archivé (>2 ans), ignoré")
            ignores += 1
            continue

        pertinents += 1
        readme_content, readme_name = find_readme(slug)
        readme_note = f"README: {readme_name}" if readme_name else "README: (absent)"

        try:
            fiche = translator.generate_fiche(repo, readme_content, score_info)
            if fiche is None:
                print(f"⏭️  {full_name} — Score: {score} — Skipped (signal vide post-LLM)")
                ignores += 1
                continue
            translator.save_fiche(fiche, full_name, str(FICHES_DIR))
            fiches_generees += 1
            print(f"✅ {full_name} — Score: {score} — Fiche sauvegardée — {readme_note}")
        except Exception as exc:
            print(f"❌ {full_name} — Score: {score} — Erreur génération: {exc}")

    print()
    print("=" * 60)
    print("BILAN")
    print("=" * 60)
    print(f"Total repos traités   : {total}")
    print(f"Repos pertinents      : {pertinents}")
    print(f"Fiches générées       : {fiches_generees}")
    print(f"Repos ignorés         : {ignores}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
