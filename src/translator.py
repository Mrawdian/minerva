"""
Generation of technical fiches in French from Gitee metadata + README.

Architecture:
- deterministic extractors (Directory Structure parser, hardware chipsets)
- analytical enrichment via Claude API (Haiku) for Problem solved, How it works,
  Chinese specificity, Type, Western equivalent
- objective metadata (maturity, language, score) computed locally

The ANTHROPIC_API_KEY key is read from .env (project root) or os.environ.
Without a key, fallback on default values (truncated description, ORG_SPECIFICITE).
"""

import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from anthropic import Anthropic


log = logging.getLogger("minerva.translator")

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"

CLAUDE_MODEL = "claude-haiku-4-5-20251001"
CLAUDE_MAX_TOKENS = 800
CLAUDE_TEMPERATURE = 0.1
CLAUDE_MAX_RETRIES = 4  # SDK-level retry sur 429/5xx avec backoff exponentiel

ALLOWED_TYPES = {
    "RTOS", "Framework", "Library", "Driver",
    "Board Support Package", "Documentation", "Tool", "Application",
}

# ─── Internationalization (i18n) ─────────────────────────────────────────
# Minerva produces fiches in English (default language) and in French
# (language 2). Each language has its field labels, its maturity
# categories, and its LLM prompt. The language is passed as a parameter (`lang`)
# to generate_fiche / _call_claude_for_fiche. Default: "en".

DEFAULT_LANG = "en"

# Labels of the markdown fiche fields, per language. The order is fixed on the
# generate_fiche side; this mapping only translates the labels.
FIELD_LABELS = {
    "en": {
        "type": "Type",
        "domain": "Domain",
        "score": "Relevance score",
        "problem": "Problem solved",
        "how": "How it works",
        "specificity": "Chinese specificity",
        "equivalent": "Western equivalent",
        "maturity": "Maturity",
        "language": "Language",
    },
    "fr": {
        "type": "Type",
        "domain": "Domaine",
        "score": "Score de pertinence",
        "problem": "Problème résolu",
        "how": "Comment ça marche",
        "specificity": "Spécificité chinoise",
        "equivalent": "Équivalent occidental",
        "maturity": "Maturité",
        "language": "Langue",
    },
}

# Maturity categories (field value), per language.
MATURITY_LABELS = {
    "en": {"archived": "Archived", "stable": "Stable", "active": "Active",
           "experimental": "Experimental", "updated": "updated"},
    "fr": {"archived": "Archivé", "stable": "Stable", "active": "Actif",
           "experimental": "Expérimental", "updated": "mis à jour"},
}

# Value of the "Language" field (language of the repo), per fiche language.
CODE_LANGUAGE_LABELS = {
    "en": {"CN": "Chinese", "EN": "English", "BI": "Bilingual CN-EN"},
    "fr": {"CN": "Chinois", "EN": "Anglais", "BI": "Bilingue CN-EN"},
}

# Translation of domain names (defined in French in domains.json) to
# English for display in the EN fiches. Unknown domain → as-is.
DOMAIN_DISPLAY = {
    "en": {"Embarqué": "Embedded", "IoT": "IoT", "Robotique": "Robotics",
           "Edge AI": "Edge AI"},
    "fr": {"Embarqué": "Embarqué", "IoT": "IoT", "Robotique": "Robotique",
           "Edge AI": "Edge AI"},
}


def _norm_lang(lang: str | None) -> str:
    """Normalizes the language code to 'en' or 'fr' (default 'en')."""
    return "fr" if (lang or "").lower().startswith("fr") else "en"


def _translate_domain(domaine: str, lang: str) -> str:
    """Translates a domain name (or a combination 'A / B') for display."""
    mapping = DOMAIN_DISPLAY[lang]
    parts = [p.strip() for p in domaine.split("/")]
    return " / ".join(mapping.get(p, p) for p in parts)


SYSTEM_PROMPT_EN = """You are a senior engineer, expert in:
- embedded systems (RTOS, BSP, MCU/SoC drivers),
- IoT (network stacks, protocols, cellular modules),
- robotics (ROS, control, perception),
- edge AI (mobile inference frameworks, NPU, quantization).

You read technical Mandarin fluently. You write short fiches in English to help other engineers quickly assess the relevance of a Chinese open-source project found on Gitee or GitHub.

Strict rules:
- FORBIDDEN: marketing superlatives ("powerful", "revolutionary", "easy to use", "leading", "complete", "modern", "robust", "innovative").
- FORBIDDEN: hollow generalities ("unified platform", "end-to-end solution", "rich ecosystem").
- MANDATORY: verifiable technical facts (component names, languages, dependencies, hardware targets, protocols, standards).
- If a piece of information is not in the provided context, write "to be confirmed" rather than inventing it.
- If the README is in Chinese, translate it mentally before summarizing; do not paraphrase the description generically.
- Output: valid JSON ONLY, no code block, no preamble."""


SYSTEM_PROMPT = """Tu es un ingénieur senior français expert en :
- systèmes embarqués (RTOS, BSP, drivers MCU/SoC),
- IoT (stacks réseau, protocoles, modules cellulaires),
- robotique (ROS, contrôle, perception),
- edge AI (frameworks d'inférence mobile, NPU, quantification).

Tu lis couramment le mandarin technique. Tu rédiges des fiches courtes en français pour aider d'autres ingénieurs francophones à évaluer rapidement la pertinence d'un projet open source chinois trouvé sur Gitee.

Règles strictes :
- INTERDIT : superlatifs marketing ("puissant", "révolutionnaire", "facile à utiliser", "leader", "complet", "moderne", "robuste", "innovant").
- INTERDIT : généralités creuses ("plateforme unifiée", "solution end-to-end", "écosystème riche").
- OBLIGATOIRE : faits techniques vérifiables (noms de composants, langages, dépendances, cibles matérielles, protocoles, normes).
- Si une info n'est pas dans le contexte fourni, écrire "à confirmer" plutôt qu'inventer.
- Si le README est en chinois, le traduire mentalement avant de résumer ; ne pas paraphraser génériquement la description.
- Sortie : JSON valide UNIQUEMENT, pas de bloc de code, pas de préambule."""


ORG_SPECIFICITE: dict[str, str] = {
    "openharmony": "OpenHarmony — OS open source de l'Open Atom Foundation (origine Huawei), poussé comme alternative nationale pour l'IoT et les appareils grand public chinois.",
    "openharmony-sig": "OpenHarmony SIG (Special Interest Group) — sous-organisation de la communauté OpenHarmony, regroupe les contributions de groupes thématiques (graphique, sécurité, multimédia, etc.).",
    "openharmony-tpc": "OpenHarmony TPC (Third-Party Components) — dépôt officiel des bibliothèques tierces validées et portées vers OpenHarmony par la communauté.",
    "openluat": "Hezhou (合宙) — fabricant chinois de modules cellulaires (gammes Air8000/Air8101/Air780E), très présent dans l'IoT industriel chinois.",
    "espressifsystems": "Espressif Systems (乐鑫, Shanghai) — fabricant des SoCs ESP8266/ESP32 ; miroir Gitee officiel synchronisé depuis GitHub.",
    "espressif": "Espressif Systems (乐鑫, Shanghai) — fabricant des SoCs ESP8266/ESP32 ; miroir Gitee officiel synchronisé depuis GitHub.",
    "embedfire": "EmbedFire (野火, Shenzhen) — marque pédagogique chinoise de référence, kits et manuels diffusés massivement dans les universités techniques.",
    "rt-thread": "RT-Thread Ltd. (Shanghai) — éditeur du premier RTOS d'origine chinoise à s'être imposé industriellement.",
    "rockchip": "Rockchip (瑞芯微电子, Fuzhou) — fondeur chinois de SoCs applicatifs milieu-haut de gamme.",
    "hisilicon": "HiSilicon (海思半导体) — filiale fabless de Huawei, conçoit les SoCs Hi35xx (caméra IP, smart vision, set-top box) et Kirin (mobile).",
}

RTOS_KEYWORDS = ("rtos", "thread", "rt-thread", "freertos", "zephyr", "liteos")
DRIVER_KEYWORDS = ("driver", "hal", "bsp")
DOC_KEYWORDS = ("docs", "tutorial", "教程")
BOARD_KEYWORDS = ("board", "soc")

HARDWARE_PATTERNS = [
    r"\bHi\d{4}\w*\b",
    r"\bRK\d{4}\w*\b",
    r"\bSTM32\w+\b",
    r"\bESP32\w*\b",
    r"\bGD32\w+\b",
    r"\bMM32\w+\b",
    r"\bAir\d{3,4}\w*\b",
]


_dotenv_loaded = False


def _ensure_dotenv_loaded() -> None:
    """Loads .env (project root) into os.environ only once.

    The .env overrides the existing variables in os.environ (python-dotenv convention):
    we avoid an old key persisted at the OS level masking the file's up-to-date value.
    """
    global _dotenv_loaded
    if _dotenv_loaded:
        return
    _dotenv_loaded = True
    if not ENV_FILE.is_file():
        return
    for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


def _contains_cjk(text: str) -> bool:
    return any("一" <= c <= "鿿" for c in text)


def _cjk_ratio(text: str) -> float:
    if not text:
        return 0.0
    cjk = sum(1 for c in text if "一" <= c <= "鿿")
    return cjk / len(text)


def detect_language(text: str) -> str:
    """Returns 'CN' if >10% CJK characters, 'EN' otherwise."""
    return "CN" if _cjk_ratio(text) > 0.10 else "EN"


def _classify_fiche_language_code(description: str, readme: str | None) -> str:
    """Returns a language-neutral code of the repo: 'CN' / 'EN' / 'BI' (bilingual)."""
    desc_cn = _contains_cjk(description)
    readme_cn = bool(readme) and _contains_cjk(readme)
    desc_ascii = bool(re.search(r"[A-Za-z]{4,}", description))
    readme_ascii = bool(readme) and bool(re.search(r"[A-Za-z]{4,}", readme))

    any_cn = desc_cn or readme_cn
    any_en = desc_ascii or readme_ascii

    if any_cn and any_en:
        return "BI"
    if any_cn:
        return "CN"
    return "EN"


def _classify_fiche_language(description: str, readme: str | None,
                             lang: str = DEFAULT_LANG) -> str:
    """Localized label of the repo language (Chinese/English/Bilingual CN-EN)."""
    code = _classify_fiche_language_code(description, readme)
    return CODE_LANGUAGE_LABELS[_norm_lang(lang)][code]


def _clean_text(text: str) -> str:
    """Removes markdown escaping artifacts (`\\(`, `\\)`, `\\[`, `\\]`)."""
    if not text:
        return text
    return (
        text.replace("\\(", "(")
        .replace("\\)", ")")
        .replace("\\[", "[")
        .replace("\\]", "]")
    )


# Noise patterns to strip from the README before sending to the LLM.
# The goal: maximize the density of technical signal within the allocated 3500-char
# window. CI banners, shields.io badges, license blocks, HTML TOC, etc.

_BADGE_LINE_RE = re.compile(
    r"""(?xm)
    ^                       # début de ligne
    [ \t]*                  # indent éventuel
    (?:
        \[!\[[^\]]*\]\([^)]+\)\]\([^)]+\)   # [![alt](img)](href)
      | !\[[^\]]*\]\([^)]+\)                 # ![alt](img)
      | \[!\[[^\]]*\]\[[^\]]+\]\]\[[^\]]+\] # référence indirecte
    )
    (?:\s+(?:\[!\[[^\]]*\]\([^)]+\)\]\([^)]+\)|!\[[^\]]*\]\([^)]+\)))*  # plusieurs badges sur la même ligne
    [ \t]*$
    """
)

_HTML_BLOCK_RE = re.compile(
    r"(?is)<(p|div|table|center|h[1-6]|ul|ol|li|a|blockquote|pre|tbody|tr|td|th)\b[^>]*>.*?</\1>",
)
_HTML_VOID_RE = re.compile(
    r"(?is)<(?:img|br|hr|input|meta|link|source)\b[^>]*/?>",
)

_HORIZONTAL_RULE_RE = re.compile(r"(?m)^[ \t]*(?:\*\s*\*\s*\*+|-{3,}|_{3,})[ \t]*$")

_LICENSE_BLOCK_RE = re.compile(
    r"(?is)(?:^|\n)(?:#{1,3}[ \t]*)?"
    r"(?:license|licence|copyright|许可证|版权)\b[^\n]*\n"
    r"(?:.{0,2000}?)(?=\n#{1,3}\s|\Z)",
)

_TOC_HEADING_RE = re.compile(
    r"(?is)(?:^|\n)#{1,3}[ \t]*"
    r"(?:table[ \t]+of[ \t]+contents?|toc|sommaire|目录)\s*\n"
    r"(?:[\-\*\+\s\d\.\)\(]+\[[^\]]+\]\([^)]+\)[ \t]*\n)+",
)

_LONG_CODE_FENCE_RE = re.compile(r"(?s)```[^\n]*\n(.{300,}?)\n```")

_BLANK_LINES_RE = re.compile(r"\n{3,}")


def _clean_readme_paragraphs(readme: str | None, max_chars: int = 3500) -> str | None:
    """Cleans the README to maximize technical density before LLM injection.

    Steps (idempotent):
      1. Remove lines that are 100% shields.io badges / CI status images.
      2. Remove raw HTML blocks (often decoration: center tables, logos).
      3. Remove markdown horizontal rules (---, ***).
      4. Remove entire License / Copyright sections (of no interest to the LLM).
      5. Remove TOCs ("Table of Contents" sections + their list of links).
      6. Truncate code blocks over 300 chars (keep an excerpt).
      7. Collapse multiple blank lines.
      8. Truncate to max_chars, cutting cleanly at the end of a paragraph.

    The result is designed to fit into the Claude prompt. No network call.
    """
    if not readme:
        return readme

    cleaned = readme

    cleaned = _BADGE_LINE_RE.sub("", cleaned)
    cleaned = _HTML_BLOCK_RE.sub("", cleaned)
    cleaned = _HTML_VOID_RE.sub("", cleaned)
    cleaned = _HORIZONTAL_RULE_RE.sub("", cleaned)
    cleaned = _LICENSE_BLOCK_RE.sub("\n", cleaned)
    cleaned = _TOC_HEADING_RE.sub("\n", cleaned)

    def _truncate_code_block(m: re.Match) -> str:
        body = m.group(1)
        first_lines = "\n".join(body.split("\n")[:6])
        return f"```\n{first_lines}\n... [bloc tronqué]\n```"

    cleaned = _LONG_CODE_FENCE_RE.sub(_truncate_code_block, cleaned)
    cleaned = _BLANK_LINES_RE.sub("\n\n", cleaned)
    cleaned = cleaned.strip()

    if len(cleaned) > max_chars:
        cut = cleaned[:max_chars]
        # Clean cut: goes back to the last "\n\n" (paragraph)
        last_para = cut.rfind("\n\n")
        if last_para > max_chars * 0.6:
            cut = cut[:last_para]
        cleaned = cut.rstrip() + "\n\n[…tronqué]"

    return cleaned


def infer_type(repo: dict) -> str:
    """Infers the type from full_name, description and language. Used as a fallback."""
    full_name = (repo.get("full_name") or "").lower()
    description = (repo.get("description") or "").lower()
    language = (repo.get("language") or "").lower()

    if any(k in full_name for k in RTOS_KEYWORDS):
        return "RTOS"
    if "框架" in description or "framework" in description or "sdk" in description or language == "lua":
        return "Framework"
    if any(k in full_name for k in DRIVER_KEYWORDS):
        return "Driver"
    if any(k in full_name for k in DOC_KEYWORDS):
        return "Documentation"
    if any(k in full_name for k in BOARD_KEYWORDS):
        return "Board Support Package"
    return "Library"


def _parse_iso_datetime(s: str | None) -> datetime | None:
    if not s:
        return None
    s = s.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def _age_days(dt: datetime | None) -> int | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).days


def _format_date_short(dt: datetime | None) -> str:
    if dt is None:
        return ""
    return dt.strftime("%Y-%m")


def infer_maturity(repo: dict, lang: str = DEFAULT_LANG) -> str:
    """Classifies into Archived/Stable/Active/Experimental (+ inline metadata), localized.

    The extras (★ N, N forks) are language-neutral; only the category and the word
    "updated"/"mis à jour" are translated. The month stays in YYYY-MM format.
    """
    lang = _norm_lang(lang)
    labels = MATURITY_LABELS[lang]
    pushed = _parse_iso_datetime(repo.get("pushed_at"))
    age = _age_days(pushed)
    stars = repo.get("stargazers_count") or 0
    forks = repo.get("forks_count") or 0

    if age is not None and age > 730:
        category = labels["archived"]
    elif stars > 500 and age is not None and age < 365:
        category = labels["stable"]
    elif age is not None and age < 180:
        category = labels["active"]
    else:
        category = labels["experimental"]

    extras: list[str] = []
    if stars:
        extras.append(f"★ {stars}")
    if forks:
        extras.append(f"{forks} forks")
    date_str = _format_date_short(pushed)
    if date_str:
        extras.append(f"{labels['updated']} {date_str}")

    if extras:
        return f"{category} ({', '.join(extras)})"
    return category


def is_archived(repo: dict, max_years: int = 2) -> bool:
    """True if the repository is considered archived.

    Three signals used, logical OR:
      1. last push > max_years (default 2 years) — temporal staleness
      2. repo['archived'] is True — standard flag, rarely used in practice on Gitee
      3. repo['status'] == '关闭' — the real Gitee signal (status "Closed"). Empirical
         measurement 2026-04-27: ~28% of a sample of 50 retained repos used it,
         while 'archived' was None everywhere.
    """
    if repo.get("archived") is True:
        return True
    if repo.get("status") == "关闭":
        return True
    pushed = _parse_iso_datetime(repo.get("pushed_at"))
    age = _age_days(pushed)
    if age is None:
        return False
    return age > max_years * 365


def _get_org_specificite(full_name: str) -> str | None:
    """Returns the specificity of the namespace if known, otherwise None."""
    if not full_name:
        return None
    if full_name.startswith("mirrors/"):
        return None
    namespace = full_name.split("/", 1)[0].lower()
    return ORG_SPECIFICITE.get(namespace)


def _parse_directory_structure(readme: str) -> dict[str, str]:
    """Extracts the mapping {top-level dir: description} from a 'Directory Structure' section."""
    if not readme:
        return {}
    sect_match = re.search(
        r"(?is)#{1,3}\s*(?:Directory\s+Structure|目录结构|Directory)[^\n]*\n(.*?)(?=\n#{1,3}\s|\Z)",
        readme,
    )
    if not sect_match:
        return {}
    section = sect_match.group(1)

    entries: dict[str, str] = {}
    for m in re.finditer(
        r"^[├└]──\s+([A-Za-z0-9_.\-]+)\s+#\s*(.+?)\s*$",
        section,
        flags=re.MULTILINE,
    ):
        name = m.group(1)
        desc = m.group(2).strip()
        entries.setdefault(name, desc)
    return entries


def _extract_hardware(readme: str) -> list[str]:
    """Extracts references to chipsets (Hi*, RK*, STM32*, ESP32*, GD32*, MM32*, Air*)."""
    if not readme:
        return []
    seen: dict[str, str] = {}
    for pat in HARDWARE_PATTERNS:
        for m in re.findall(pat, readme):
            key = m.lower()
            seen.setdefault(key, m)
    return sorted(seen.values())


def _looks_like_empty_fiche(llm_result: dict) -> bool:
    """True if the LLM output signals that the repo has no usable content.

    Three criteria, 2/3 rule. Works on the dict returned by
    _call_claude_for_fiche, BEFORE generate_fiche turns it into markdown.

    Criteria:
      C1 — probleme_resolu contains one of the confession phrases:
           "n'a pas de contenu", "archivé", "aucun problème spécifique",
           "informations disponibles ne permettent pas", "le dépôt est archivé"
      C2 — comment_ca_marche starts with "À confirmer" AND is < 100 chars
           (signals that no concrete info followed the hedge)
      C3 — equivalent_occidental.strip() == "À confirmer" AND specificite_chinoise
           contains "à confirmer" (the LLM hedges on both comparative fields)

    2 criteria out of 3 → fiche considered empty. A single criterion → we keep it (the LLM
    may hedge on one field while delivering something concrete on the other two).
    """
    pr = (llm_result.get("probleme_resolu") or "").lower()
    cm = (llm_result.get("comment_ca_marche") or "").strip()
    eq = (llm_result.get("equivalent_occidental") or "").strip()
    sp = (llm_result.get("specificite_chinoise") or "").lower()

    c1_phrases = (
        "n'a pas de contenu",
        "archivé",
        "aucun problème spécifique",
        "informations disponibles ne permettent pas",
        "le dépôt est archivé",
    )
    c1 = any(p in pr for p in c1_phrases)
    c2 = cm.startswith("À confirmer") and len(cm) < 100
    c3 = eq.lower() == "à confirmer" and "à confirmer" in sp

    return sum((c1, c2, c3)) >= 2


def _call_claude_for_fiche(
    description: str,
    readme: str | None,
    repo_name: str,
    language: str,
    dir_structure: dict[str, str],
    hardware: list[str],
    score_info: dict | None = None,
    lang: str = DEFAULT_LANG,
) -> dict:
    """Calls Claude Haiku to generate the analytical fields of the fiche.

    Returns a dict with the keys probleme_resolu, comment_ca_marche,
    specificite_chinoise, type, equivalent_occidental.

    Note: the LLM does NOT produce the "domaine" field. That one is computed
    locally by the analyzer (cosine similarity against the domain definitions)
    and filled by generate_fiche from score_info. score_info is nonetheless injected
    into the prompt as CONTEXT so that the LLM aligns its tone/type with the domain
    already identified — without having to rewrite or contradict it.

    If the API key is absent or if the call fails → fallback on default values.
    """
    _ensure_dotenv_loaded()
    lang = _norm_lang(lang)
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    dir_info = ""
    if dir_structure:
        dir_info = "\n".join([f"  - {k}: {v}" for k, v in dir_structure.items()])

    hw_info = ", ".join(hardware) if hardware else ""

    if lang == "en":
        fallback = {
            "probleme_resolu": (description[:200] if description else "Information not available"),
            "comment_ca_marche": (readme[:300] if readme else "See the project README"),
            "specificite_chinoise": (
                _get_org_specificite(repo_name) or "Chinese open-source project"
            ),
            "type": infer_type(
                {"full_name": repo_name, "description": description, "language": ""}
            ),
            "equivalent_occidental": "Not identified",
        }
    else:
        fallback = {
            "probleme_resolu": (description[:200] if description else "Information non disponible"),
            "comment_ca_marche": (readme[:300] if readme else "Voir le README du projet"),
            "specificite_chinoise": (
                _get_org_specificite(repo_name) or "Projet open source chinois"
            ),
            "type": infer_type(
                {"full_name": repo_name, "description": description, "language": ""}
            ),
            "equivalent_occidental": "Non identifié",
        }

    if not api_key:
        log.warning(f"ANTHROPIC_API_KEY absent — fallback pour {repo_name}")
        return fallback

    org_context = _get_org_specificite(repo_name) or ""
    owner = repo_name.split("/", 1)[0] if "/" in repo_name else repo_name
    cleaned_readme = _clean_readme_paragraphs(readme, max_chars=3500)

    if lang == "en":
        domaine_context = ""
        if score_info:
            dom = score_info.get("domaine_principal") or "(undetermined)"
            score = score_info.get("score_total", 0)
            domaine_context = (
                f"PRE-COMPUTED DOMAIN (by cosine similarity against the Minerva definitions): "
                f"{dom} — score {score}/100. Take it into account to align the tone and the "
                f"choice of `type`. Do not rewrite this label in your output: it is filled locally.\n\n"
            )

        prompt = f"""{domaine_context}Repository: {repo_name}
Main language: {language or "(not detected)"}

DESCRIPTION (Gitee/GitHub field, max 500 chars):
{description[:500] if description else "(no description)"}

README EXCERPT (cleaned: badges/license/TOC/long code blocks removed, max 3500 chars):
{cleaned_readme if cleaned_readme else "(no README accessible)"}

DIR STRUCTURE (extracted from the README):
{dir_info if dir_info else "(no structure section detected)"}

DETECTED CHIPSETS (Hi*, RK*, STM32*, ESP32*, GD32*, MM32*, Air*):
{hw_info if hw_info else "(no chipset cited)"}

ORG CONTEXT:
{org_context if org_context else "(not documented on the Minerva side)"}

---

Generate a JSON object with EXACTLY these 5 keys (no others):

{{
  "probleme_resolu": "1 to 2 technical sentences in English: WHICH specific problem this project solves. Not 'provide a solution' — be concrete. Good example: 'Replace Nordic's proprietary Bluetooth stack with an open-source nRF52-compatible implementation'. Bad example: 'Provide a modern BLE framework'.",

  "comment_ca_marche": "3 to 4 sentences in English on the concrete architecture: main components, language(s), notable dependencies, supported hardware targets if relevant. Cite names (libraries, modules, formats, protocols) rather than generic concepts.",

  "specificite_chinoise": "1 to 2 sentences in English on what ties this project to the Chinese ecosystem: parent organization and its real role in the Chinese industry, associated chipset vendor (HiSilicon, Rockchip, Allwinner, Espressif, Kendryte…), compliance with a Chinese standard, WeChat/Alipay/Baidu Cloud integration, etc. If there is no specific tie beyond the Chinese author, write literally: 'Hosted on Gitee/GitHub by {owner}; no particular Chinese specificity beyond the author.'",

  "type": "Choose EXACTLY one value among: RTOS, Framework, Library, Driver, Board Support Package, Documentation, Tool, Application. Definitions: RTOS=real-time kernel; Framework=reusable infrastructure with inversion of control; Library=API to call; Driver=low-level hardware interface; Board Support Package=port of an OS to a specific board; Documentation=docs/book/tutorials without own code; Tool=CLI/desktop utility; Application=final app.",

  "equivalent_occidental": "1 to 3 comparable Western projects separated by commas, with minimal context if not obvious. Good example: 'Zephyr (Linux Foundation), FreeRTOS (Amazon)'. If there is no direct equivalent, write: 'No known direct equivalent — specific combination of [verifiable distinctive element]'."
}}

Reply ONLY with the JSON. No markdown code block, no surrounding text."""
        system_prompt = SYSTEM_PROMPT_EN
    else:
        domaine_context = ""
        if score_info:
            dom = score_info.get("domaine_principal") or "(non déterminé)"
            score = score_info.get("score_total", 0)
            domaine_context = (
                f"DOMAINE PRÉ-CALCULÉ (par cosine similarity contre les définitions Minerva) : "
                f"{dom} — score {score}/100. Tiens-en compte pour aligner le ton et le choix "
                f"du `type`. Ne réécris pas ce label dans ta sortie : il est rempli localement.\n\n"
            )

        prompt = f"""{domaine_context}Repository : {repo_name}
Langage principal : {language or "(non détecté)"}

DESCRIPTION (champ Gitee, max 500 chars) :
{description[:500] if description else "(aucune description Gitee)"}

EXTRAIT README (nettoyé : badges/license/TOC/blocs code longs supprimés, max 3500 chars) :
{cleaned_readme if cleaned_readme else "(aucun README accessible)"}

STRUCTURE DIR (extraite du README) :
{dir_info if dir_info else "(aucune section structure détectée)"}

CHIPSETS DÉTECTÉS (Hi*, RK*, STM32*, ESP32*, GD32*, MM32*, Air*) :
{hw_info if hw_info else "(aucun chipset cité)"}

CONTEXTE ORG :
{org_context if org_context else "(non documenté côté Minerva)"}

---

Génère un JSON avec EXACTEMENT ces 5 clés (pas d'autres) :

{{
  "probleme_resolu": "1 à 2 phrases techniques en français : QUEL problème spécifique ce projet résout. Pas 'fournir une solution' — sois concret. Bon exemple : 'Remplacer la pile Bluetooth propriétaire de Nordic par une implémentation open source compatible nRF52'. Mauvais exemple : 'Fournir un framework BLE moderne'.",

  "comment_ca_marche": "3 à 4 phrases en français sur l'architecture concrète : composants principaux, langage(s), dépendances notables, cibles matérielles supportées si pertinent. Cite des noms (libraries, modules, formats, protocoles) plutôt que des concepts génériques.",

  "specificite_chinoise": "1 à 2 phrases sur ce qui relie ce projet à l'écosystème chinois : organisation parente avec son rôle réel dans l'industrie chinoise, chipset vendor associé (HiSilicon, Rockchip, Allwinner, Espressif, Kendryte…), conformité à un standard chinois, intégration WeChat/Alipay/Baidu Cloud, etc. Si aucun lien spécifique au-delà de l'auteur chinois, écris littéralement : 'Hébergé sur Gitee par {owner} ; pas de spécificité chinoise particulière au-delà de l'auteur.'",

  "type": "Choisir EXACTEMENT une valeur parmi : RTOS, Framework, Library, Driver, Board Support Package, Documentation, Tool, Application. Définitions : RTOS=noyau temps réel ; Framework=infrastructure réutilisable avec inversion de contrôle ; Library=API à appeler ; Driver=interface matérielle bas niveau ; Board Support Package=portage d'un OS sur une carte précise ; Documentation=docs/livre/tutoriels sans code propre ; Tool=utilitaire CLI/desktop ; Application=app finale.",

  "equivalent_occidental": "1 à 3 projets occidentaux comparables séparés par des virgules, avec contexte minimal si non évident. Bon exemple : 'Zephyr (Linux Foundation), FreeRTOS (Amazon)'. Si aucun équivalent direct, écris : 'Aucun équivalent direct connu — combinaison spécifique de [élément distinctif vérifiable]'."
}}

Réponds UNIQUEMENT avec le JSON. Pas de bloc de code markdown, pas de texte autour."""
        system_prompt = SYSTEM_PROMPT

    try:
        client = Anthropic(api_key=api_key, max_retries=CLAUDE_MAX_RETRIES)
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            temperature=CLAUDE_TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )

        text = response.content[0].text.strip()
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0]
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0]
        text = text.strip()

        result = json.loads(text)

        # Validation of the type against the whitelist
        type_value = (result.get("type") or "").strip()
        if type_value not in ALLOWED_TYPES:
            log.warning(f"Type LLM hors liste blanche pour {repo_name} : {type_value!r} → fallback")
            type_value = fallback["type"]

        return {
            "probleme_resolu": result.get("probleme_resolu") or fallback["probleme_resolu"],
            "comment_ca_marche": result.get("comment_ca_marche") or fallback["comment_ca_marche"],
            "specificite_chinoise": result.get("specificite_chinoise") or fallback["specificite_chinoise"],
            "type": type_value,
            "equivalent_occidental": result.get("equivalent_occidental") or fallback["equivalent_occidental"],
        }
    except json.JSONDecodeError as exc:
        log.warning(f"Claude API a renvoyé un JSON invalide pour {repo_name} : {exc}")
        return fallback
    except Exception as exc:
        log.warning(f"Échec Claude API pour {repo_name} : {exc}")
        return fallback


def generate_fiche(repo: dict, readme: str | None, score_info: dict,
                   lang: str = DEFAULT_LANG) -> str | None:
    """Generates the complete markdown of a technical fiche (Minerva format), localized.

    Analytical fields (Problem, How, Specificity, Type, Equivalent) → Claude API
    (in the `lang` language). Deterministic fields (Maturity, Language, Score,
    Domain, source) → computed locally and localized.

    Args:
        lang: "en" (default) or "fr". Determines the LLM output language, the
            field labels, and the colon typography (EN: `Type:`,
            FR: `Type :`).

    Returns:
        str of the markdown if the fiche is valid, None if the LLM signals empty content
        (cf. _looks_like_empty_fiche). The caller (pipeline) must treat None as
        "do not publish this repo, mark skipped in state.json".
    """
    lang = _norm_lang(lang)
    full_name = repo.get("full_name") or "(unknown)"
    description = repo.get("description") or ""

    dir_structure = _parse_directory_structure(readme) if readme else {}
    hardware = _extract_hardware(readme) if readme else []

    llm = _call_claude_for_fiche(
        description=description,
        readme=readme,
        repo_name=full_name,
        language=_classify_fiche_language(description, readme, lang="en"),
        dir_structure=dir_structure,
        hardware=hardware,
        score_info=score_info,
        lang=lang,
    )

    if _looks_like_empty_fiche(llm):
        log.info(f"Fiche écartée (signal vide post-LLM) : {full_name}")
        return None

    return _compose_fiche(repo, readme, score_info, llm, lang)


def _compose_fiche(repo: dict, readme: str | None, score_info: dict,
                   llm: dict, lang: str) -> str:
    """Assembles the fiche markdown from an LLM prose dict — deterministic, no I/O.

    All localized parts (field labels, colon typography, domain display, maturity,
    repo-language label) are computed here from `lang`, so the same LLM result can
    be composed in any supported language.
    """
    lang = _norm_lang(lang)
    labels = FIELD_LABELS[lang]
    # Colon typography: non-breaking-space-like space before ':' in FR.
    sep = " :" if lang == "fr" else ":"

    def _field(key: str, value: str) -> str:
        return f"**{labels[key]}{sep}** {value}"

    full_name = repo.get("full_name") or "(unknown)"
    description = repo.get("description") or ""
    fiche_lang = _classify_fiche_language(description, readme, lang=lang)

    scores = score_info.get("scores_par_domaine") or {}
    if scores and max(scores.values(), default=0) > 0:
        top = max(scores.values())
        domaine_display = " / ".join(d for d, s in scores.items() if s == top)
    else:
        domaine_display = score_info.get("domaine_principal", "")
    domaine_display = _translate_domain(domaine_display, lang)

    maturite = infer_maturity(repo, lang=lang)
    score_total = score_info.get("score_total", 0)

    # Source-aware line: Gitee by default, GitHub for the connector's repos.
    if repo.get("_minerva_source") == "github":
        source_line = f"**GitHub{sep}** https://github.com/{full_name}"
    else:
        source_line = f"**Gitee{sep}** https://gitee.com/{full_name}"

    probleme = _clean_text(llm["probleme_resolu"])
    comment = _clean_text(llm["comment_ca_marche"])
    specificite = _clean_text(llm["specificite_chinoise"])
    equivalent = _clean_text(llm["equivalent_occidental"])
    type_ = llm["type"]

    lines = [
        "---",
        f"## {full_name}",
        _field("type", type_),
        _field("domain", domaine_display),
        _field("score", f"{score_total}/100"),
        _field("problem", probleme),
        _field("how", comment),
        _field("specificity", specificite),
        _field("equivalent", equivalent),
        _field("maturity", maturite),
        _field("language", fiche_lang),
        source_line,
        "---",
    ]
    return "\n".join(lines) + "\n"


def generate_fiche_pair(repo: dict, readme: str | None,
                        score_info: dict) -> tuple[str | None, str | None]:
    """Generates the EN + FR fiche pair from a SINGLE source of facts.

    Strategy (native bilingual, no drift):
      1. One LLM generation in English (default language) → the facts.
      2. One prose translation EN→FR (translate_fiche_prose, temperature 0) —
         same facts, French wording.
      3. Both markdowns composed deterministically via _compose_fiche.

    Cost: 1 generation + 1 translation (~2 small Haiku calls per repo).
    Type is a controlled vocabulary (RTOS, Framework…) shared by both languages.

    Returns:
        (fiche_en, fiche_fr). (None, None) if the LLM signals empty content —
        the caller must treat it as "skipped", like generate_fiche.
        If the translation fails, fiche_fr falls back to the English prose with
        French labels (logged) rather than failing the repo.
    """
    full_name = repo.get("full_name") or "(unknown)"
    description = repo.get("description") or ""

    dir_structure = _parse_directory_structure(readme) if readme else {}
    hardware = _extract_hardware(readme) if readme else []

    llm_en = _call_claude_for_fiche(
        description=description,
        readme=readme,
        repo_name=full_name,
        language=_classify_fiche_language(description, readme, lang="en"),
        dir_structure=dir_structure,
        hardware=hardware,
        score_info=score_info,
        lang="en",
    )

    if _looks_like_empty_fiche(llm_en):
        log.info(f"Fiche écartée (signal vide post-LLM) : {full_name}")
        return None, None

    fiche_en = _compose_fiche(repo, readme, score_info, llm_en, "en")

    # FR prose = faithful translation of the same facts (falls back to EN prose
    # on failure inside translate_fiche_prose — never fails the repo).
    prose_fr = translate_fiche_prose(llm_en, target_lang="fr")
    llm_fr = dict(llm_en)
    llm_fr.update(prose_fr)
    fiche_fr = _compose_fiche(repo, readme, score_info, llm_fr, "fr")

    return fiche_en, fiche_fr


_TRANSLATE_SYSTEM = {
    "en": "You are a technical translator. Translate the given French text into precise, "
          "natural technical English. Preserve all proper nouns, product names, component "
          "names, acronyms, numbers and code identifiers exactly. Do not add or remove "
          "information. Output valid JSON only.",
    "fr": "Tu es un traducteur technique. Traduis le texte anglais fourni en français "
          "technique précis et naturel. Préserve exactement les noms propres, noms de "
          "produits, composants, acronymes, nombres et identifiants de code. N'ajoute ni "
          "ne retire aucune information. Réponds en JSON valide uniquement.",
}


def translate_fiche_prose(prose: dict, target_lang: str = DEFAULT_LANG) -> dict:
    """Translates the 4 prose fields of a fiche (probleme/comment/specificite/equivalent).

    Used to produce the bilingual pair (a fiche generated in one language,
    faithfully translated to the other) without re-fetch or re-analysis. The facts are
    thus identical between EN and FR.

    Args:
        prose: dict with the keys probleme_resolu, comment_ca_marche,
            specificite_chinoise, equivalent_occidental.
        target_lang: "en" (default) or "fr" — TARGET language of the translation.

    Returns:
        dict with the same keys, translated. On API/JSON failure → returns `prose`
        unchanged (fail-safe: better the source language than an empty fiche).
    """
    _ensure_dotenv_loaded()
    target_lang = _norm_lang(target_lang)
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    keys = ("probleme_resolu", "comment_ca_marche", "specificite_chinoise",
            "equivalent_occidental")
    if not api_key:
        log.warning("ANTHROPIC_API_KEY absent — traduction ignorée (prose inchangée)")
        return dict(prose)

    payload = {k: prose.get(k, "") for k in keys}
    prompt = (
        f"Translate the values of this JSON into {'English' if target_lang == 'en' else 'French'}. "
        f"Return a JSON object with the SAME keys and translated values, nothing else:\n\n"
        f"{json.dumps(payload, ensure_ascii=False)}"
    )
    try:
        client = Anthropic(api_key=api_key, max_retries=CLAUDE_MAX_RETRIES)
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            temperature=0.0,
            system=_TRANSLATE_SYSTEM[target_lang],
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0]
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0]
        result = json.loads(text.strip())
        return {k: (result.get(k) or prose.get(k, "")) for k in keys}
    except Exception as exc:
        log.warning(f"Échec traduction prose ({exc}) — prose inchangée")
        return dict(prose)


def save_fiche(fiche: str, repo_full_name: str, output_dir: str = "output/fiches") -> str:
    """Writes the fiche to {output_dir}/{slug}_fiche.md and returns the path."""
    slug = re.sub(r"[^A-Za-z0-9_\-]", "_", repo_full_name.replace("/", "_"))
    out_path = Path(output_dir) / f"{slug}_fiche.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(fiche, encoding="utf-8")
    return str(out_path)
