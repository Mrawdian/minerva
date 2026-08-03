"""Pydantic schema for the Minerva markdown fiches.

Single source of truth for parsing/generating the fiches. Replaces the regexes
scattered across rescore.py and build_newsletter.py.

Not yet used by build_dashboard.py and build_site.py — those files have
their own inline logic that will be migrated in a dedicated sprint (cf. TODO at
the top of each).
"""

import re
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, computed_field


def _is_recent_month(month: str, max_age_months: int = 18) -> bool:
    """True if a 'YYYY-MM' string is within `max_age_months` of now (freshness)."""
    if not month or len(month) < 7:
        return False
    try:
        y, m = int(month[:4]), int(month[5:7])
    except ValueError:
        return False
    now = datetime.now(timezone.utc)
    age_months = (now.year - y) * 12 + (now.month - m)
    return age_months <= max_age_months


_TITLE_RE = re.compile(r"^##\s+(.+?)(\s+\[MODIFIÉ\])?\s*$")
_FIELD_RE = re.compile(r"^\*\*([^:*]+?)\s*:\*\*\s*(.*)$")
_SCORE_RE = re.compile(r"\s*(\d+)")
_STARS_RE = re.compile(r"★\s*(\d+)")
_FORKS_RE = re.compile(r"(\d+)\s*forks")
# Accepts EN fiches ("updated 2026-07") and FR fiches ("mis à jour 2026-07").
_PUSHED_AT_MONTH_RE = re.compile(r"(?:updated|mis à jour) (\d{4}-\d{2})")

# Accepted field labels, EN (default) and FR. The fiche is bilingual:
# English is the default language, French is language 2.
_LABEL_ALIASES = {
    "type": ("Type",),
    "domaine": ("Domain", "Domaine"),
    "score": ("Relevance score", "Score de pertinence"),
    "probleme": ("Problem solved", "Problème résolu"),
    "comment": ("How it works", "Comment ça marche"),
    "specificite": ("Chinese specificity", "Spécificité chinoise"),
    "equivalent": ("Western equivalent", "Équivalent occidental"),
    "maturite": ("Maturity", "Maturité"),
    "langue": ("Language", "Langue"),
    "source": ("Gitee", "GitHub"),
}


def _pick(fields: dict, key: str, default: str = "") -> str:
    """Returns the first value found among the EN/FR aliases of a field."""
    for label in _LABEL_ALIASES[key]:
        if label in fields:
            return fields[label]
    return default


def _detect_lang(fields: dict) -> str:
    """Infers the fiche language from the labels present ('fr' if FR labels)."""
    fr_markers = ("Problème résolu", "Score de pertinence", "Spécificité chinoise",
                  "Comment ça marche", "Maturité", "Langue")
    return "fr" if any(m in fields for m in fr_markers) else "en"


# Output labels for to_markdown, per language (mirror of translator.FIELD_LABELS).
_OUT_LABELS = {
    "en": ("Type", "Domain", "Relevance score", "Problem solved", "How it works",
           "Chinese specificity", "Western equivalent", "Maturity", "Language"),
    "fr": ("Type", "Domaine", "Score de pertinence", "Problème résolu", "Comment ça marche",
           "Spécificité chinoise", "Équivalent occidental", "Maturité", "Langue"),
}


# Generic fallback phrases emitted when the LLM/README was unavailable (EN + FR).
# Their presence means the fiche is thin → lower confidence.
_FALLBACK_MARKERS = (
    "Information not available", "See the project README", "Not identified",
    "Chinese open-source project",
    "Information non disponible", "Voir le README du projet", "Non identifié",
    "Projet open source chinois",
)


def confidence_tier(prose_all: str, main_prose_len: int,
                    has_metadata: bool, is_recent: bool = True) -> str:
    """Transparent data-quality confidence tier for a fiche: High / Medium / Low.

    Not the *relevance* score (which measures topical fit); this measures how much
    to trust the fiche's own content, derived only from observable signals:
      - fallback phrases present → the enrichment was thin,
      - an explicit "to be confirmed" flag from the model → unverified claim,
      - depth of the "How it works" field (real README-backed vs generic),
      - presence of maturity metadata (stars / last-push date),
      - recency of the last push (stale data is less certain to reflect reality).

    Deliberately simple and explainable — no LLM, no stored field, computed from
    the fiche itself. See docs/SCORING.md.
    """
    is_fallback = any(m in prose_all for m in _FALLBACK_MARKERS)
    if is_fallback or main_prose_len < 80:
        return "Low"
    unverified = "to be confirmed" in prose_all.lower() or "à confirmer" in prose_all.lower()
    if main_prose_len >= 160 and has_metadata and is_recent and not unverified:
        return "High"
    return "Medium"


class FicheParseError(ValueError):
    """Raised when the markdown does not have the minimal structure of a fiche."""


class Fiche(BaseModel):
    """1:1 reflection of the markdown produced by translator.generate_fiche.

    Round-trip guaranteed: Fiche.from_markdown(f.to_markdown()) == f (the computed
    fields [owner, stars, forks, pushed_at_month] are derived from maturite and
    full_name, thus consistent by construction).
    """

    full_name: str = Field(min_length=1)
    type: str
    domaine: str
    score_de_pertinence: int = Field(ge=0, le=100)

    probleme_resolu: str
    comment_ca_marche: str
    specificite_chinoise: str
    equivalent_occidental: str

    maturite: str
    langue: str
    gitee_url: str
    lang: str = "en"  # fiche language ("en" default, "fr" language 2)
    modified_flag: bool = False  # [MODIFIÉ] in the H2 title

    # ─── Computed fields (derived from the fields above) ────────────────

    @computed_field
    @property
    def owner(self) -> str:
        return self.full_name.split("/", 1)[0] if "/" in self.full_name else ""

    @computed_field
    @property
    def source_label(self) -> str:
        """'GitHub' if the URL points to github.com, 'Gitee' otherwise.

        Guarantees that to_markdown re-emits the right label for fiches coming
        from the GitHub connector (round-trip via rescore.py, etc.).
        """
        return "GitHub" if "github.com" in self.gitee_url else "Gitee"

    @computed_field
    @property
    def stars(self) -> int:
        m = _STARS_RE.search(self.maturite)
        return int(m.group(1)) if m else 0

    @computed_field
    @property
    def forks(self) -> int:
        m = _FORKS_RE.search(self.maturite)
        return int(m.group(1)) if m else 0

    @computed_field
    @property
    def pushed_at_month(self) -> str:
        m = _PUSHED_AT_MONTH_RE.search(self.maturite)
        return m.group(1) if m else ""

    @computed_field
    @property
    def confidence(self) -> str:
        """Data-quality confidence tier (High/Medium/Low) — see confidence_tier."""
        prose_all = " ".join((self.probleme_resolu, self.comment_ca_marche,
                              self.specificite_chinoise, self.equivalent_occidental))
        has_meta = self.stars > 0 or bool(self.pushed_at_month)
        is_recent = _is_recent_month(self.pushed_at_month)
        return confidence_tier(prose_all, len(self.comment_ca_marche or ""),
                               has_meta, is_recent)

    # ─── Serialization / deserialization ────────────────────────────────

    @classmethod
    def from_markdown(cls, text: str) -> "Fiche":
        """Parses a markdown fiche into a Fiche instance.

        Raises:
            FicheParseError: missing H2 title or markdown too degraded to
                find the numeric score.
            pydantic.ValidationError: required field empty or out of bounds (score).
        """
        if not text or not text.strip():
            raise FicheParseError("markdown vide")

        title: Optional[str] = None
        modified_flag = False
        fields: dict[str, str] = {}

        for line in text.splitlines():
            s = line.strip()
            if title is None:
                m = _TITLE_RE.match(s)
                if m:
                    title = m.group(1).strip()
                    modified_flag = bool(m.group(2))
                    continue
            m = _FIELD_RE.match(s)
            if m:
                fields[m.group(1).strip()] = m.group(2).strip()

        if title is None:
            raise FicheParseError("titre H2 (## owner/repo) absent du markdown")

        score_raw = _pick(fields, "score")
        score_m = _SCORE_RE.match(score_raw)
        if not score_m:
            raise FicheParseError(
                f"Score illisible : {score_raw!r} (attendu: 'N/100')"
            )

        return cls(
            full_name=title,
            type=_pick(fields, "type"),
            domaine=_pick(fields, "domaine"),
            score_de_pertinence=int(score_m.group(1)),
            probleme_resolu=_pick(fields, "probleme"),
            comment_ca_marche=_pick(fields, "comment"),
            specificite_chinoise=_pick(fields, "specificite"),
            equivalent_occidental=_pick(fields, "equivalent"),
            maturite=_pick(fields, "maturite"),
            langue=_pick(fields, "langue"),
            gitee_url=_pick(fields, "source"),
            lang=_detect_lang(fields),
            modified_flag=modified_flag,
        )

    def to_markdown(self) -> str:
        """Serializes to markdown in the translator.generate_fiche format.

        The format identically mimics the one produced by the pipeline to guarantee
        the round-trip with the existing fiches (framing with '---', same
        labels, same field orders).
        """
        lang = "fr" if self.lang == "fr" else "en"
        sep = " :" if lang == "fr" else ":"
        lab = _OUT_LABELS[lang]

        title = f"## {self.full_name}"
        if self.modified_flag:
            title += " [MODIFIÉ]"
        lines = [
            "---",
            title,
            f"**{lab[0]}{sep}** {self.type}",
            f"**{lab[1]}{sep}** {self.domaine}",
            f"**{lab[2]}{sep}** {self.score_de_pertinence}/100",
            f"**{lab[3]}{sep}** {self.probleme_resolu}",
            f"**{lab[4]}{sep}** {self.comment_ca_marche}",
            f"**{lab[5]}{sep}** {self.specificite_chinoise}",
            f"**{lab[6]}{sep}** {self.equivalent_occidental}",
            f"**{lab[7]}{sep}** {self.maturite}",
            f"**{lab[8]}{sep}** {self.langue}",
            f"**{self.source_label}{sep}** {self.gitee_url}",
            "---",
        ]
        return "\n".join(lines) + "\n"
