"""Rescore existing fiches (EN + FR twins) with the up-to-date scoring config.

No network calls. No LLM calls.

Strategy:
- Reads state.json (canonical list of tracked repos)
- For each repo, parses the markdown fiche via Fiche.from_markdown (see fiche_schema)
  to rebuild a synthetic repo dict (description = concatenation of the analytical
  LLM fields, full_name = title, etc.)
- Re-applies analyzer.score_repo with the updated domains
- If the score or the domain changes, rewrites the fiche via Fiche.to_markdown
  (preserving its language — EN or FR)
- Persists the scores in state.json under the 'scores' key (does not break the diff)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

import analyzer  # noqa: E402
from fiche_schema import Fiche, FicheParseError  # noqa: E402
from translator import _translate_domain  # noqa: E402 — display localization

STATE_FILE = ROOT / "output" / "state.json"
FICHES_DIR = ROOT / "output" / "fiches"
FICHES_FR_DIR = ROOT / "output" / "fiches_fr"
SOURCES_FILE = ROOT / "config" / "sources.json"


def slugify(full_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-]", "_", full_name.replace("/", "_"))


def compute_domaine_display(score_info: dict) -> str:
    """Reproduit la logique de translator.generate_fiche pour le champ Domaine."""
    scores = score_info.get("scores_par_domaine") or {}
    if scores and max(scores.values(), default=0) > 0:
        top = max(scores.values())
        return " / ".join(d for d, s in scores.items() if s == top)
    return score_info.get("domaine_principal", "(non déterminé)")


def main() -> int:
    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    state_repos = state.get("repos", {})
    sources = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    watched_owners = sources.get("comptes_gitee", [])
    domains = analyzer.load_domains()
    print(f"Domaines chargés : {[d['nom'] for d in domains]}")
    print(f"State.json : {len(state_repos)} repos suivis\n")

    updated_score = 0
    updated_domain = 0
    updated_fr = 0
    edge_ai_matched = 0
    parse_errors = 0
    new_state_scores: dict[str, dict] = {}
    deltas: list[tuple[str, int, int, str, str]] = []

    for full_name, pushed_at in state_repos.items():
        fiche_path = FICHES_DIR / f"{slugify(full_name)}_fiche.md"
        if not fiche_path.is_file():
            continue

        try:
            fiche = Fiche.from_markdown(fiche_path.read_text(encoding="utf-8"))
        except (FicheParseError, ValueError) as exc:
            print(f"⚠️  parse error sur {full_name} : {exc}", file=sys.stderr)
            parse_errors += 1
            continue

        old_score = fiche.score_de_pertinence
        old_domaine = fiche.domaine

        prose = " ".join([
            fiche.probleme_resolu,
            fiche.comment_ca_marche,
            fiche.specificite_chinoise,
            fiche.equivalent_occidental,
        ])

        synthetic = {
            "full_name": fiche.full_name,
            "description": prose,
            "language": "",
            "stargazers_count": fiche.stars,
            "forks_count": fiche.forks,
            "pushed_at": pushed_at,
        }

        score_info = analyzer.score_repo(synthetic, domains, watched_owners=watched_owners)
        new_score = score_info["score_total"]
        # compute_domaine_display returns RAW config domain names ("Embarqué"…).
        # Fiches display LOCALIZED names ("Embedded" in EN) — always translate
        # per fiche language before writing, or EN fiches get FR domain names.
        raw_domaine = compute_domaine_display(score_info)
        new_domaine = _translate_domain(raw_domaine, fiche.lang)
        edge_ai_score = score_info["scores_par_domaine"].get("Edge AI", 0)
        if edge_ai_score > 0:
            edge_ai_matched += 1

        new_state_scores[fiche.full_name] = {
            "score": new_score,
            "domaine": raw_domaine,
            "edge_ai_score": edge_ai_score,
        }

        score_changed = new_score != old_score
        domain_changed = new_domaine != old_domaine
        if score_changed or domain_changed:
            updated = fiche.model_copy(update={
                "score_de_pertinence": new_score,
                "domaine": new_domaine,
            })
            fiche_path.write_text(updated.to_markdown(), encoding="utf-8")
            if score_changed:
                updated_score += 1
            if domain_changed:
                updated_domain += 1
            deltas.append((fiche.full_name, old_score, new_score, old_domaine, new_domaine))

        # FR twin: apply the SAME score/domain (facts come from the EN scoring —
        # re-scoring the FR prose would drift via different embeddings). This
        # closes the known "rescore EN-only" drift risk.
        fr_path = FICHES_FR_DIR / f"{slugify(full_name)}_fiche.md"
        if fr_path.is_file():
            try:
                fr = Fiche.from_markdown(fr_path.read_text(encoding="utf-8"))
            except (FicheParseError, ValueError) as exc:
                print(f"⚠️  parse error (FR) sur {full_name} : {exc}", file=sys.stderr)
                parse_errors += 1
            else:
                fr_domaine = _translate_domain(raw_domaine, "fr")
                if fr.score_de_pertinence != new_score or fr.domaine != fr_domaine:
                    fr_updated = fr.model_copy(update={
                        "score_de_pertinence": new_score,
                        "domaine": fr_domaine,
                    })
                    fr_path.write_text(fr_updated.to_markdown(), encoding="utf-8")
                    updated_fr += 1

    state["scores"] = new_state_scores
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Repos avec match Edge AI > 0   : {edge_ai_matched}")
    print(f"Fiches avec score modifié     : {updated_score}")
    print(f"Fiches avec domaine modifié   : {updated_domain}")
    print(f"Fiches FR synchronisées        : {updated_fr}")
    print(f"Fiches non parsables           : {parse_errors}")
    print(f"state.json enrichi de la clé 'scores' ({len(new_state_scores)} entrées)")

    if deltas:
        deltas.sort(key=lambda x: -(x[2] - x[1]))
        print(f"\n=== Top 15 deltas de score ===")
        for full, old, new, od, nd in deltas[:15]:
            d = "→ Edge AI" if "Edge AI" in nd and "Edge AI" not in od else ""
            print(f"  {old:>3} → {new:>3}  (+{new - old})  {full:<55} {d}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
