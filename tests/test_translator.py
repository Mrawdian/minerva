"""Tests de src/translator.py — fonctions déterministes (pas de LLM)."""

from unittest.mock import patch

import translator


def test_detect_language_cn():
    text = "嵌入式系统是一种特殊的计算机系统"
    assert translator.detect_language(text) == "CN"


def test_detect_language_en():
    text = "Embedded system is a specialized computer system"
    assert translator.detect_language(text) == "EN"


def test_classify_fiche_language_bilingual():
    desc = "嵌入式系统 embedded system"
    # Anglais par défaut, français en langue 2.
    assert translator._classify_fiche_language(desc, None) == "Bilingual CN-EN"
    assert translator._classify_fiche_language(desc, None, lang="fr") == "Bilingue CN-EN"


def test_classify_fiche_language_pure_cn():
    assert translator._classify_fiche_language("纯中文描述系统", None) == "Chinese"
    assert translator._classify_fiche_language("纯中文描述系统", None, lang="fr") == "Chinois"


def test_classify_fiche_language_pure_en():
    assert translator._classify_fiche_language("Pure English description here", None) == "English"


def test_classify_fiche_language_code_neutral():
    """Le code langue-neutre est indépendant de la langue de la fiche."""
    assert translator._classify_fiche_language_code("纯中文描述系统", None) == "CN"
    assert translator._classify_fiche_language_code("Pure English here", None) == "EN"
    assert translator._classify_fiche_language_code("嵌入式 embedded", None) == "BI"


def test_infer_maturity_archived():
    repo = {"pushed_at": "2020-01-01T00:00:00+00:00", "stargazers_count": 0, "forks_count": 0}
    assert translator.infer_maturity(repo).startswith("Archived")       # défaut EN
    assert translator.infer_maturity(repo, lang="fr").startswith("Archivé")


def test_infer_maturity_stable_high_stars():
    """>500 stars + push < 365 jours = Stable."""
    repo = {"pushed_at": "2026-01-01T00:00:00+00:00", "stargazers_count": 5000, "forks_count": 100}
    result = translator.infer_maturity(repo)
    assert "Stable" in result or "Active" in result
    assert "★ 5000" in result


def test_is_archived_true_after_2_years():
    repo = {"pushed_at": "2020-01-01T00:00:00+00:00"}
    assert translator.is_archived(repo) is True


def test_is_archived_false_recent():
    repo = {"pushed_at": "2026-01-01T00:00:00+00:00"}
    assert translator.is_archived(repo) is False


def test_is_archived_via_archived_flag():
    """Flag archived=True sur un repo récent doit faire basculer is_archived → True."""
    repo = {"pushed_at": "2026-04-01T00:00:00+00:00", "archived": True}
    assert translator.is_archived(repo) is True


def test_is_archived_via_gitee_status_closed():
    """Statut Gitee 关闭 (Fermé) sur un repo récent doit faire basculer is_archived → True.

    C'est le vrai signal d'archivage utilisé par Gitee. Mesuré empiriquement
    2026-04-27 : ~28% d'un échantillon de 50 repos en status=关闭, 0% en archived=True.
    """
    repo = {"pushed_at": "2026-04-01T00:00:00+00:00", "status": "关闭"}
    assert translator.is_archived(repo) is True


def test_is_archived_status_started_not_archived():
    """Statut 开始 (Started/Actif) sur un repo récent doit rester non-archivé."""
    repo = {"pushed_at": "2026-04-01T00:00:00+00:00", "status": "开始"}
    assert translator.is_archived(repo) is False


# ─── _looks_like_empty_fiche ────────────────────────────────────────────────

def test_looks_like_empty_fiche_strong_repo_returns_false():
    """Une fiche LLM riche et concrète n'est pas vide."""
    llm = {
        "probleme_resolu": "Fournir un framework d'inférence neuronale optimisé CPU pour mobile, sans dépendance externe.",
        "comment_ca_marche": "Écrit en C++, support ARM 32/64-bit et x86, charge des modèles ncnn convertis depuis Caffe/TF/ONNX, exécute par traversée de graphe avec optimisations NEON et Vulkan.",
        "specificite_chinoise": "Développé par Tencent, déployé en production dans QQ et WeChat.",
        "type": "Library",
        "equivalent_occidental": "TensorFlow Lite (Google), ONNX Runtime (Microsoft)",
    }
    assert translator._looks_like_empty_fiche(llm) is False


def test_looks_like_empty_fiche_moderate_with_one_hedge_returns_false():
    """Un seul critère (eq=À confirmer mais probleme et comment concrets) → pas vide."""
    llm = {
        "probleme_resolu": "Spécification d'un protocole de communication BLE custom pour capteurs Hi3516D.",
        "comment_ca_marche": "Documentation technique en mandarin sans implémentation de référence dans le repo.",
        "specificite_chinoise": "Lié à HiSilicon, suit les conventions OpenHarmony pour les périphériques.",
        "type": "Documentation",
        "equivalent_occidental": "À confirmer",
    }
    assert translator._looks_like_empty_fiche(llm) is False


def test_looks_like_empty_fiche_two_criteria_returns_true():
    """Critères C1 + C3 cochés (LLM avoue archivage + double 'à confirmer') → vide."""
    llm = {
        "probleme_resolu": "Le dépôt est archivé et n'a pas de contenu technique exploitable.",
        "comment_ca_marche": "Aucun code de production présent dans le repo, juste un avis de migration.",
        "specificite_chinoise": "Hébergé chez openharmony-tpc, à confirmer via le repo successeur.",
        "type": "Library",
        "equivalent_occidental": "À confirmer",
    }
    assert translator._looks_like_empty_fiche(llm) is True


def test_looks_like_empty_fiche_three_criteria_returns_true():
    """Cas limite : tous les critères cochés."""
    llm = {
        "probleme_resolu": "Aucun problème spécifique ne peut être identifié à partir des informations disponibles.",
        "comment_ca_marche": "À confirmer.",
        "specificite_chinoise": "À confirmer.",
        "type": "Library",
        "equivalent_occidental": "À confirmer",
    }
    assert translator._looks_like_empty_fiche(llm) is True


def test_generate_fiche_returns_none_on_empty_signal(monkeypatch):
    """generate_fiche doit propager None quand _call_claude_for_fiche signale vide."""
    empty_llm = {
        "probleme_resolu": "Le dépôt est archivé.",
        "comment_ca_marche": "À confirmer.",
        "specificite_chinoise": "à confirmer",
        "type": "Library",
        "equivalent_occidental": "À confirmer",
    }
    monkeypatch.setattr(translator, "_call_claude_for_fiche",
                        lambda **kwargs: empty_llm)
    repo = {"full_name": "owner/dead", "description": "x", "pushed_at": "2026-01-01T00:00:00+00:00"}
    score_info = {"score_total": 30, "scores_par_domaine": {"Embarqué": 20}, "domaine_principal": "Embarqué"}
    assert translator.generate_fiche(repo, "raw readme", score_info) is None


def test_clean_text_unescapes_markdown():
    text = "Hello \\(world\\) and \\[brackets\\]"
    assert translator._clean_text(text) == "Hello (world) and [brackets]"


def test_extract_hardware_from_readme():
    readme = "Supports STM32F103, ESP32-S2, RK3568, and Hi3516DV300."
    hw = translator._extract_hardware(readme)
    assert "STM32F103" in hw
    assert "ESP32" in str(hw)
    assert any("RK3568" in h for h in hw)
    assert any("Hi3516" in h for h in hw)


def test_parse_directory_structure_simple():
    readme = """# My Project

## Directory Structure

```
├── src         # source files
├── docs        # documentation
└── tests       # unit tests
```

## Other section
"""
    out = translator._parse_directory_structure(readme)
    assert out.get("src") == "source files"
    assert out.get("docs") == "documentation"


def test_infer_type_rtos():
    repo = {"full_name": "some/rtos-kernel", "description": "tiny kernel", "language": "C"}
    assert translator.infer_type(repo) == "RTOS"


def test_infer_type_documentation():
    repo = {"full_name": "rtthread/docs", "description": "documentation", "language": "Markdown"}
    # 'docs' is in DOC_KEYWORDS, but RTOS_KEYWORDS includes 'rt-thread' AND 'thread' so
    # rtthread (sans tiret) ne contient pas 'rt-thread' substring exact, mais 'thread' oui.
    # On vérifie au moins que ça classe en RTOS ou Documentation.
    result = translator.infer_type(repo)
    assert result in ("RTOS", "Documentation")


def test_clean_readme_strips_badge_lines():
    """Lignes 100% badges shields.io → supprimées."""
    readme = """# My Project

[![Build](https://img.shields.io/travis/foo/bar.svg)](https://travis-ci.org/foo/bar) [![Version](https://img.shields.io/npm/v/foo.svg)](https://npmjs.com/package/foo)

This is a real description of the project.
"""
    out = translator._clean_readme_paragraphs(readme)
    assert "shields.io" not in out
    assert "travis" not in out
    assert "real description" in out
    assert "# My Project" in out


def test_clean_readme_strips_html_blocks():
    readme = """# Title

<p align="center">
  <img src="logo.png" width="200">
</p>

<table><tr><td>Decorative</td></tr></table>

Real technical content here.
"""
    out = translator._clean_readme_paragraphs(readme)
    assert "<img" not in out
    assert "<table" not in out
    assert "Real technical content" in out


def test_clean_readme_strips_license_section():
    readme = """# Project

Some technical content.

## License

MIT License

Copyright (c) 2024 Author

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute.

## Architecture

More technical content.
"""
    out = translator._clean_readme_paragraphs(readme)
    assert "Permission is hereby granted" not in out
    assert "MIT License" not in out
    assert "Some technical content" in out
    assert "More technical content" in out


def test_clean_readme_strips_toc():
    readme = """# Project

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
- [Examples](#examples)

## Installation

Run `npm install`.
"""
    out = translator._clean_readme_paragraphs(readme)
    assert "[Installation](#installation)" not in out
    assert "[Usage](#usage)" not in out
    assert "Run `npm install`" in out


def test_clean_readme_truncates_long_code_blocks():
    """Bloc de code > 300 chars → tronqué au 6 premières lignes + marqueur."""
    long_code = "\n".join([f"line_{i}_with_some_content_to_pad_out_the_length" for i in range(40)])
    readme = f"""# Project

Documentation paragraph.

```python
{long_code}
```

After block.
"""
    out = translator._clean_readme_paragraphs(readme)
    assert "[bloc tronqué]" in out
    assert "After block" in out
    assert "line_0_" in out  # premières lignes conservées
    assert "line_39" not in out  # dernières lignes supprimées


def test_clean_readme_collapses_blank_lines():
    readme = "Para 1.\n\n\n\n\n\nPara 2.\n\n\n\nPara 3."
    out = translator._clean_readme_paragraphs(readme)
    # Triples sauts ou plus → doubles saut max
    assert "\n\n\n" not in out
    assert "Para 1." in out
    assert "Para 3." in out


def test_clean_readme_truncates_to_max_chars():
    readme = "Header.\n\n" + ("Para text. " * 1000) + "\n\nFinal."
    out = translator._clean_readme_paragraphs(readme, max_chars=500)
    assert len(out) <= 600  # 500 + marqueur "[...tronqué]"
    assert "[…tronqué]" in out


def test_clean_readme_handles_none_and_empty():
    assert translator._clean_readme_paragraphs(None) is None
    assert translator._clean_readme_paragraphs("") == ""


def test_clean_readme_idempotent():
    """Appliquer 2 fois la fonction donne le même résultat (idempotence)."""
    readme = """# Project

[![Build](https://img.shields.io/x.svg)](https://x)

Content.

## License

MIT. Copyright stuff.
"""
    once = translator._clean_readme_paragraphs(readme)
    twice = translator._clean_readme_paragraphs(once)
    assert once == twice


def test_call_claude_fallback_without_key(monkeypatch):
    """Sans ANTHROPIC_API_KEY, _call_claude_for_fiche doit utiliser le fallback."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    # Force le rechargement et s'assure que _ensure_dotenv_loaded ne récupère pas la clé
    monkeypatch.setattr(translator, "_dotenv_loaded", True)
    monkeypatch.setattr(translator, "ENV_FILE", translator.ROOT / "nonexistent.env")
    monkeypatch.setattr(translator, "_dotenv_loaded", False)

    result = translator._call_claude_for_fiche(
        description="Test description",
        readme=None,
        repo_name="owner/test",
        language="EN",
        dir_structure={},
        hardware=[],
    )
    assert "probleme_resolu" in result
    assert "type" in result
    # Le fallback retourne soit la description tronquée, soit "Information non disponible"
    assert result["probleme_resolu"]


def test_generate_fiche_domaine_from_score_info_ignores_llm_contradiction(monkeypatch):
    """Le champ markdown **Domaine :** doit venir de score_info, pas du LLM.

    Même si _call_claude_for_fiche retourne un dict contenant une clé "domaine"
    contradictoire (cas hypothétique d'un LLM qui ignorerait l'instruction "ne réécris
    pas ce label"), generate_fiche doit IGNORER cette valeur et utiliser uniquement
    score_info["scores_par_domaine"] / score_info["domaine_principal"].
    """
    # LLM retourne un dict valide + une clé "domaine" parasite contradictoire
    llm_with_contradiction = {
        "probleme_resolu": "Framework d'inférence neuronale optimisé mobile.",
        "comment_ca_marche": "C++ avec optimisations ARM NEON et Vulkan, modèles convertis depuis ONNX.",
        "specificite_chinoise": "Développé par Tencent.",
        "type": "Library",
        "equivalent_occidental": "TensorFlow Lite (Google)",
        "domaine": "Embarqué",  # parasite : doit être ignoré
    }
    monkeypatch.setattr(translator, "_call_claude_for_fiche",
                        lambda **kwargs: llm_with_contradiction)

    repo = {
        "full_name": "Tencent/ncnn",
        "description": "neural network inference framework for mobile",
        "language": "C++",
        "pushed_at": "2026-04-01T00:00:00+00:00",
        "stargazers_count": 300,
    }
    score_info = {
        "score_total": 81,
        "scores_par_domaine": {"Embarqué": 30, "IoT": 10, "Edge AI": 75},
        "domaine_principal": "Edge AI",
    }
    # Défaut = anglais : label "Domain", "Embarqué" traduit en "Embedded".
    fiche = translator.generate_fiche(repo, "raw readme", score_info)
    assert fiche is not None
    assert "**Domain:** Edge AI" in fiche
    assert "**Domain:** Embedded" not in fiche

    # Langue 2 = français : label "Domaine", nom de domaine en français.
    fiche_fr = translator.generate_fiche(repo, "raw readme", score_info, lang="fr")
    assert "**Domaine :** Edge AI" in fiche_fr
    assert "**Domaine :** Embarqué" not in fiche_fr


# ─── generate_fiche_pair (bilingue natif) ────────────────────────────────────

_PAIR_REPO = {
    "full_name": "rtthread/rt-thread",
    "description": "RTOS for IoT devices",
    "language": "C",
    "pushed_at": "2026-06-01T00:00:00+00:00",
    "stargazers_count": 5000,
    "forks_count": 2000,
}
_PAIR_SCORE = {
    "score_total": 90,
    "scores_par_domaine": {"Embarqué": 80, "IoT": 40, "Edge AI": 10},
    "domaine_principal": "Embarqué",
}
_PAIR_LLM_EN = {
    "probleme_resolu": "Provide a scalable RTOS for constrained MCUs.",
    "comment_ca_marche": "C kernel with scheduler, IPC, device framework and BSP layer for ARM/RISC-V targets.",
    "specificite_chinoise": "Developed by RT-Thread Ltd. (Shanghai).",
    "type": "RTOS",
    "equivalent_occidental": "FreeRTOS (Amazon), Zephyr (Linux Foundation)",
}
_PAIR_PROSE_FR = {
    "probleme_resolu": "Fournir un RTOS scalable pour MCU contraints.",
    "comment_ca_marche": "Noyau C avec ordonnanceur, IPC, framework device et couche BSP pour cibles ARM/RISC-V.",
    "specificite_chinoise": "Développé par RT-Thread Ltd. (Shanghai).",
    "equivalent_occidental": "FreeRTOS (Amazon), Zephyr (Linux Foundation)",
}


def test_generate_fiche_pair_one_generation_one_translation(monkeypatch):
    """La paire vient d'UNE génération EN + UNE traduction — pas deux générations."""
    calls = {"gen": 0, "trans": 0}

    def fake_llm(**kwargs):
        calls["gen"] += 1
        assert kwargs["lang"] == "en"  # la génération source est toujours EN
        return dict(_PAIR_LLM_EN)

    def fake_translate(prose, target_lang="en"):
        calls["trans"] += 1
        assert target_lang == "fr"
        return dict(_PAIR_PROSE_FR)

    monkeypatch.setattr(translator, "_call_claude_for_fiche", fake_llm)
    monkeypatch.setattr(translator, "translate_fiche_prose", fake_translate)

    fiche_en, fiche_fr = translator.generate_fiche_pair(_PAIR_REPO, "readme", _PAIR_SCORE)

    assert calls == {"gen": 1, "trans": 1}
    # EN : labels anglais + prose anglaise
    assert "**Problem solved:** Provide a scalable RTOS" in fiche_en
    assert "**Domain:** Embedded" in fiche_en
    # FR : labels français + prose traduite
    assert "**Problème résolu :** Fournir un RTOS scalable" in fiche_fr
    assert "**Domaine :** Embarqué" in fiche_fr
    # Faits partagés : même type, même score dans les deux langues
    assert "**Type:** RTOS" in fiche_en and "**Type :** RTOS" in fiche_fr
    assert "90/100" in fiche_en and "90/100" in fiche_fr


def test_generate_fiche_pair_empty_signal_returns_none_none(monkeypatch):
    empty = {
        "probleme_resolu": "Information not available",
        "comment_ca_marche": "See the project README",
        "specificite_chinoise": "Chinese open-source project",
        "type": "Library",
        "equivalent_occidental": "Not identified",
    }
    monkeypatch.setattr(translator, "_call_claude_for_fiche", lambda **k: empty)
    monkeypatch.setattr(translator, "_looks_like_empty_fiche", lambda llm: True)
    assert translator.generate_fiche_pair(_PAIR_REPO, None, _PAIR_SCORE) == (None, None)


def test_generate_fiche_pair_translation_failure_falls_back_to_en_prose(monkeypatch):
    """Si la traduction échoue (renvoie la prose source), la fiche FR garde les
    labels FR et la prose EN — jamais de repo perdu pour un échec de traduction."""
    monkeypatch.setattr(translator, "_call_claude_for_fiche",
                        lambda **k: dict(_PAIR_LLM_EN))
    # translate_fiche_prose est fail-safe : sur échec elle renvoie la prose inchangée
    monkeypatch.setattr(translator, "translate_fiche_prose",
                        lambda prose, target_lang="en": dict(prose))

    fiche_en, fiche_fr = translator.generate_fiche_pair(_PAIR_REPO, "readme", _PAIR_SCORE)
    assert fiche_fr is not None
    assert "**Problème résolu :** Provide a scalable RTOS" in fiche_fr  # prose EN, label FR
    assert "**Maturité :**" in fiche_fr  # champs déterministes bien localisés FR
