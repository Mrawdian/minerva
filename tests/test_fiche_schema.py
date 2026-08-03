"""Tests de src/fiche_schema.py — round-trip et erreurs de parsing."""

import pytest
from pydantic import ValidationError

from fiche_schema import Fiche, FicheParseError, confidence_tier


SAMPLE_FICHE = """---
## Tencent/ncnn
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 81/100
**Problème résolu :** Fournir un framework d'inférence de réseaux de neurones optimisé pour l'exécution CPU sur appareils mobiles avec latence et consommation mémoire minimales.
**Comment ça marche :** ncnn est écrit en C++ avec support natif des architectures ARM (32/64-bit) et x86. Il charge des modèles au format propriétaire ncnn.
**Spécificité chinoise :** Développé par Tencent (groupe internet majeur chinois), déployé en production dans QQ, WeChat, Qzone, Pitu.
**Équivalent occidental :** TensorFlow Lite (Google), ONNX Runtime (Microsoft/Linux Foundation), MobileNet (Google), PyTorch Mobile (Meta)
**Maturité :** Actif (★ 298, 3 forks, mis à jour 2026-04)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/Tencent/ncnn
---
"""


# ─── Round-trip ─────────────────────────────────────────────────────────────

def test_round_trip_real_fiche():
    """Une fiche réelle doit traverser parse → re-serialize sans diff."""
    f = Fiche.from_markdown(SAMPLE_FICHE)
    assert f.full_name == "Tencent/ncnn"
    assert f.type == "Library"
    assert f.domaine == "Embarqué"
    assert f.score_de_pertinence == 81
    assert f.langue == "Bilingue CN-EN"
    assert f.modified_flag is False

    # Re-serialize et reparse
    serialized = f.to_markdown()
    f2 = Fiche.from_markdown(serialized)
    assert f == f2
    # Le markdown doit être strictement identique au source
    assert serialized == SAMPLE_FICHE


def test_round_trip_modified_flag():
    """Le flag [MODIFIÉ] doit survivre au round-trip."""
    src = SAMPLE_FICHE.replace("## Tencent/ncnn\n", "## Tencent/ncnn [MODIFIÉ]\n")
    f = Fiche.from_markdown(src)
    assert f.modified_flag is True
    assert f.full_name == "Tencent/ncnn"
    serialized = f.to_markdown()
    assert "[MODIFIÉ]" in serialized
    assert serialized == src


def test_computed_fields():
    """Les champs computed doivent dériver correctement de maturite et full_name."""
    f = Fiche.from_markdown(SAMPLE_FICHE)
    assert f.owner == "Tencent"
    assert f.stars == 298
    assert f.forks == 3
    assert f.pushed_at_month == "2026-04"


# ─── Erreurs de parsing ─────────────────────────────────────────────────────

def test_missing_title_raises():
    """Un markdown sans titre H2 doit lever FicheParseError."""
    bad = SAMPLE_FICHE.replace("## Tencent/ncnn\n", "")
    with pytest.raises(FicheParseError, match="titre H2"):
        Fiche.from_markdown(bad)


def test_invalid_score_value_raises():
    """Un score hors-bornes (>100) doit lever ValidationError de Pydantic."""
    bad = SAMPLE_FICHE.replace("**Score de pertinence :** 81/100",
                               "**Score de pertinence :** 250/100")
    with pytest.raises(ValidationError):
        Fiche.from_markdown(bad)


def test_corrupted_markdown_raises():
    """Markdown vide ou sans la moindre structure doit lever FicheParseError."""
    with pytest.raises(FicheParseError, match="markdown vide"):
        Fiche.from_markdown("")
    with pytest.raises(FicheParseError, match="markdown vide"):
        Fiche.from_markdown("   \n  \n")
    # Texte non-vide mais sans titre → aussi FicheParseError
    with pytest.raises(FicheParseError, match="titre H2"):
        Fiche.from_markdown("Just some random text without structure.")


def test_missing_score_field_raises():
    """Score de pertinence absent → FicheParseError (champ critique)."""
    bad = SAMPLE_FICHE.replace("**Score de pertinence :** 81/100\n", "")
    with pytest.raises(FicheParseError, match="Score illisible"):
        Fiche.from_markdown(bad)


# ─── Confidence score ───────────────────────────────────────────────────────

def test_confidence_tier_low_on_fallback_marker():
    # A fallback phrase means thin enrichment → Low, regardless of length.
    long_fallback = "See the project README. " + ("x" * 300)
    assert confidence_tier(long_fallback, len(long_fallback), True) == "Low"


def test_confidence_tier_low_on_short_prose():
    assert confidence_tier("too short", 20, True) == "Low"


def test_confidence_tier_high_on_deep_prose_with_metadata():
    deep = "A" * 200
    assert confidence_tier(deep, 200, True) == "High"


def test_confidence_tier_medium_without_metadata():
    # Deep prose but no stars/date → not High, but not thin → Medium.
    deep = "A" * 200
    assert confidence_tier(deep, 200, False) == "Medium"


def test_confidence_tier_stale_downgrades_to_medium():
    # Deep prose + metadata but stale last-push → not High.
    deep = "A" * 200
    assert confidence_tier(deep, 200, True, is_recent=False) == "Medium"


def test_confidence_tier_unverified_downgrades():
    deep = "A" * 200 + " to be confirmed"
    assert confidence_tier(deep, len(deep), True, is_recent=True) == "Medium"


def test_fiche_confidence_is_valid_tier():
    f = Fiche.from_markdown(SAMPLE_FICHE)
    assert f.confidence in {"High", "Medium", "Low"}
