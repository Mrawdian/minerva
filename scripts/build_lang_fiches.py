"""One-shot MIGRATION/BACKFILL tool — produces the bilingual fiche pair from an
existing source set.

⚠️  Since the native-bilingual pipeline change, `python src/pipeline.py` generates
and maintains BOTH the EN and FR sets on every run (translator.generate_fiche_pair).
This script is NOT part of the normal flow anymore. Keep it only for:
  - the historical one-time migration (FR-only corpus → EN default + FR set);
  - exceptional backfills after a manual corpus surgery.

Historical context: Minerva long generated French-only fiches. For the publication
switch (English default, French as language 2), this script:

  1. reads the existing French fiches in `output/fiches/`;
  2. copies them verbatim to `output/fiches_fr/` (the FR set, language 2);
  3. translates the 4 prose fields to English via `translator.translate_fiche_prose`
     (identical facts between EN and FR, no network re-fetch);
  4. remaps the deterministic fields (maturity, domain, language) to English;
  5. writes the EN set (default language) to `output/fiches/`.

Usage:
    python scripts/build_lang_fiches.py [--workers 8] [--limit N]
"""

import argparse
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

import translator  # noqa: E402
from fiche_schema import Fiche, FicheParseError  # noqa: E402

FICHES_DIR = ROOT / "output" / "fiches"          # set par défaut (deviendra EN)
FICHES_FR_DIR = ROOT / "output" / "fiches_fr"    # set langue 2 (FR)

# Remaps déterministes FR → EN (champs non-prose).
_MATURITY_FR_EN = {
    "Archivé": "Archived", "Stable": "Stable", "Actif": "Active",
    "Expérimental": "Experimental", "mis à jour": "updated",
}
_LANGUAGE_FR_EN = {
    "Bilingue CN-EN": "Bilingual CN-EN", "Chinois": "Chinese", "Anglais": "English",
}


def _remap_maturity(fr: str) -> str:
    out = fr
    for a, b in _MATURITY_FR_EN.items():
        out = out.replace(a, b)
    return out


def _to_english(fiche_fr: Fiche) -> Fiche:
    """Construit la fiche EN à partir d'une fiche FR : prose traduite + champs remappés."""
    prose_en = translator.translate_fiche_prose({
        "probleme_resolu": fiche_fr.probleme_resolu,
        "comment_ca_marche": fiche_fr.comment_ca_marche,
        "specificite_chinoise": fiche_fr.specificite_chinoise,
        "equivalent_occidental": fiche_fr.equivalent_occidental,
    }, target_lang="en")

    return fiche_fr.model_copy(update={
        "lang": "en",
        "probleme_resolu": prose_en["probleme_resolu"],
        "comment_ca_marche": prose_en["comment_ca_marche"],
        "specificite_chinoise": prose_en["specificite_chinoise"],
        "equivalent_occidental": prose_en["equivalent_occidental"],
        "domaine": translator._translate_domain(fiche_fr.domaine, "en"),
        "maturite": _remap_maturity(fiche_fr.maturite),
        "langue": _LANGUAGE_FR_EN.get(fiche_fr.langue, fiche_fr.langue),
    })


def _process_one(md_path: Path) -> tuple[str, str]:
    """Retourne (nom, statut) : traite une fiche FR → écrit FR + EN."""
    name = md_path.name
    try:
        text = md_path.read_text(encoding="utf-8")
        fiche_fr = Fiche.from_markdown(text)
    except (FicheParseError, ValueError) as exc:
        return name, f"SKIP (parse: {exc})"

    if fiche_fr.lang != "fr":
        # Déjà en anglais (relance) : on ne re-traduit pas, on garde tel quel.
        return name, "ALREADY_EN"

    # 1. Copie FR vers fiches_fr/
    (FICHES_FR_DIR / name).write_text(fiche_fr.to_markdown(), encoding="utf-8")

    # 2. Traduit et écrit EN dans fiches/
    fiche_en = _to_english(fiche_fr)
    md_path.write_text(fiche_en.to_markdown(), encoding="utf-8")
    return name, "OK"


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère la paire bilingue de fiches")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit", type=int, default=0, help="0 = toutes")
    args = parser.parse_args()

    FICHES_FR_DIR.mkdir(parents=True, exist_ok=True)
    fiches = sorted(FICHES_DIR.glob("*_fiche.md"))
    if args.limit:
        fiches = fiches[:args.limit]
    print(f"{len(fiches)} fiches à traiter (workers={args.workers})")

    counts = {"OK": 0, "ALREADY_EN": 0, "SKIP": 0}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(_process_one, p): p for p in fiches}
        for fut in as_completed(futures):
            name, status = fut.result()
            key = "SKIP" if status.startswith("SKIP") else status
            counts[key] = counts.get(key, 0) + 1
            if status.startswith("SKIP"):
                print(f"  ⚠️  {name}: {status}")

    print(f"\nEN générées : {counts['OK']}  |  déjà EN : {counts['ALREADY_EN']}  |  "
          f"ignorées : {counts['SKIP']}")
    print(f"FR (langue 2) : {FICHES_FR_DIR}")
    print(f"EN (défaut)   : {FICHES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
