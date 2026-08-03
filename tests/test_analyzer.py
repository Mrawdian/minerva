"""Tests de src/analyzer.py — scoring sémantique, hard filters, seuils.

Note : les tests de scoring sémantique chargent le vrai modèle d'embeddings au
premier appel (~3-5 s), puis bénéficient du cache disque pour les runs suivants.
Les tests purement structurels (hard filters, _keyword_in_text) n'ont pas besoin
du modèle.
"""

import analyzer


DOMAINS = [
    {
        "nom": "Embarqué",
        "definition": "Systèmes embarqués bas niveau, RTOS, microcontrôleurs ARM Cortex-M, "
                      "drivers HAL, BSP pour STM32 ESP32, firmware bare-metal, programmation C/C++",
        "mots_cles": ["mcu", "rtos", "firmware", "embedded"],
    },
    {
        "nom": "IoT",
        "definition": "Internet des objets, MQTT, LoRa, Zigbee, BLE, modules cellulaires, "
                      "OS pour objets connectés, brokers, passerelles edge, smart home",
        "mots_cles": ["iot", "mqtt", "esp32"],
    },
    {
        "nom": "Edge AI",
        "definition": "Inférence d'IA mobile et embarquée, ncnn MNN TFLite, NPU, "
                      "quantification, OCR, vision par ordinateur, détection d'objets",
        "mots_cles": ["ncnn", "tflite", "ocr", "neural"],
    },
]


def make_repo(**overrides):
    base = {
        "full_name": "owner/repo",
        "description": "",
        "language": "C",
        "stargazers_count": 0,
        "forks_count": 0,
        "pushed_at": "2026-01-01T00:00:00+00:00",
    }
    base.update(overrides)
    return base


# ─────────────────────────────────────────────────────────────────────────────
# Tests structurels (pas besoin du modèle)
# ─────────────────────────────────────────────────────────────────────────────

def test_hard_filter_third_party():
    repo = make_repo(full_name="openharmony/third_party_zlib", description="zlib port")
    r = analyzer.score_repo(repo, DOMAINS, watched_owners=["openharmony"])
    assert r["score_total"] == 0
    assert r["best_similarity"] == 0.0
    # Hard filter shortcut : pas de keyword matching effectué
    assert r["mots_cles_matches"] == []


def test_hard_filter_mirror_unwatched():
    repo = make_repo(full_name="mirrors/qt", description="Qt framework")
    r = analyzer.score_repo(repo, DOMAINS, watched_owners=["openharmony"])
    assert r["score_total"] == 0


def test_hard_filter_archived_repo():
    """Un repo sans push depuis > 2 ans doit être hard-filtré (score 0, pas de scoring)."""
    repo = make_repo(
        full_name="someone/legacy-rtos",
        description="real-time operating system RTOS embedded MCU firmware",
        stargazers_count=2000,
        pushed_at="2023-01-01T00:00:00+00:00",  # > 2 ans avant 2026-04
    )
    r = analyzer.score_repo(repo, DOMAINS, watched_owners=["someone"])
    assert r["score_total"] == 0
    assert r["best_similarity"] == 0.0
    assert r["mots_cles_matches"] == []


def test_active_repo_not_filtered_as_archived():
    """Un repo poussé récemment doit être scoré normalement, même avec strong description."""
    repo = make_repo(
        full_name="someone/active-rtos",
        description="real-time operating system RTOS embedded MCU firmware",
        stargazers_count=2000,
        pushed_at="2026-03-01T00:00:00+00:00",  # récent
    )
    r = analyzer.score_repo(repo, DOMAINS, watched_owners=["someone"])
    assert r["score_total"] > 0
    assert r["best_similarity"] > 0.0


def test_keyword_in_text_ascii_in_cjk():
    """Bug régression : 'OCR' doit matcher dans '基于飞桨的OCR和文档解析' (texte CJK)."""
    assert analyzer._keyword_in_text("ocr", "基于飞桨的OCR和文档解析工具库") is True
    assert analyzer._keyword_in_text("OCR", "基于飞桨的OCR和文档解析工具库") is True


def test_keyword_in_text_word_boundary_ascii():
    assert analyzer._keyword_in_text("ai", "main project") is False
    assert analyzer._keyword_in_text("ai", "ai inference engine") is True


def test_keyword_in_text_cjk_substring():
    assert analyzer._keyword_in_text("嵌入式", "中国嵌入式系统") is True
    assert analyzer._keyword_in_text("嵌入式", "embedded system") is False


# ─────────────────────────────────────────────────────────────────────────────
# Tests sémantiques (chargent le modèle d'embeddings)
# ─────────────────────────────────────────────────────────────────────────────

def test_score_repo_returns_correct_schema():
    """Le contrat de sortie doit rester stable (clés + types)."""
    repo = make_repo(
        full_name="rtthread/rt-thread",
        description="A real-time embedded RTOS for MCU firmware",
        stargazers_count=2000,
        forks_count=100,
    )
    r = analyzer.score_repo(repo, DOMAINS, watched_owners=["rtthread"])
    assert "score_total" in r and isinstance(r["score_total"], int)
    assert 0 <= r["score_total"] <= 100
    assert "scores_par_domaine" in r and isinstance(r["scores_par_domaine"], dict)
    assert set(r["scores_par_domaine"].keys()) == {"Embarqué", "IoT", "Edge AI"}
    assert "domaine_principal" in r
    assert r["domaine_principal"] in {"Embarqué", "IoT", "Edge AI"}
    assert "best_similarity" in r and isinstance(r["best_similarity"], float)
    assert 0.0 <= r["best_similarity"] <= 1.0
    assert "mots_cles_matches" in r and isinstance(r["mots_cles_matches"], list)
    # rt-thread description matche "rtos", "embedded", "firmware", "mcu"
    assert any(k in r["mots_cles_matches"] for k in ("rtos", "embedded", "mcu", "firmware"))


def test_score_repo_rtos_classified_as_embarque():
    """Un RTOS clair doit avoir Embarqué comme domaine principal."""
    repo = make_repo(
        full_name="rtthread/rt-thread",
        description="An open source real-time operating system for embedded devices, RTOS kernel for ARM Cortex-M microcontrollers",
        stargazers_count=2000,
    )
    r = analyzer.score_repo(repo, DOMAINS, watched_owners=["rtthread"])
    assert r["domaine_principal"] == "Embarqué"
    assert r["best_similarity"] > 0.30  # bon signal sémantique


def test_score_repo_ocr_classified_as_edge_ai():
    """Un projet OCR avec description chinoise doit basculer vers Edge AI."""
    repo = make_repo(
        full_name="paddlepaddle/PaddleOCR",
        description="基于飞桨的OCR和文档解析工具库 (OCR toolkit based on PaddlePaddle)",
        stargazers_count=4000,
    )
    r = analyzer.score_repo(repo, DOMAINS, watched_owners=["paddlepaddle"])
    assert r["domaine_principal"] == "Edge AI"
    assert r["best_similarity"] > 0.28  # signal sémantique clair


def test_score_repo_unrelated_repo_low_similarity():
    """Un repo hors-sujet (web framework) doit avoir une faible similarité."""
    repo = make_repo(
        full_name="someone/webapp",
        description="A modern web framework with React components and GraphQL",
        language="JavaScript",
    )
    r = analyzer.score_repo(repo, DOMAINS, watched_owners=[])
    # Pas en haut, similarité modeste
    assert r["best_similarity"] < 0.40


def test_watched_bonus_case_insensitive():
    """ByteDance/repo doit recevoir +8 watched bonus malgré sources.json='bytedance'."""
    repo = make_repo(
        full_name="ByteDance/iot-thing",
        description="iot mqtt sensor framework for industrial monitoring",
    )
    r_match = analyzer.score_repo(repo, DOMAINS, watched_owners=["bytedance"])
    r_nomatch = analyzer.score_repo(repo, DOMAINS, watched_owners=["other-owner"])
    # Score total différent uniquement à cause du bonus watched
    assert r_match["score_total"] - r_nomatch["score_total"] == analyzer.BONUS_WATCHED_OWNER


def test_filter_repos_drops_no_keyword_low_sim():
    """Un repo sans aucun keyword ET sim < 0.55 doit être filtré (hybride)."""
    keyword_repo = make_repo(
        full_name="rtthread/rt-thread",
        description="real-time operating system RTOS embedded MCU firmware",
        stargazers_count=2000,
    )
    off_topic_repo = make_repo(
        full_name="someone/cooking-recipes",
        description="A cookbook of family recipes",
        language="Markdown",
    )
    out = analyzer.filter_repos(
        [keyword_repo, off_topic_repo],
        DOMAINS,
        min_score=15,
        watched_owners=["rtthread"],
    )
    names = [s["repo_full_name"] for s in out]
    assert "rtthread/rt-thread" in names
    assert "someone/cooking-recipes" not in names


def test_filter_repos_keyword_anchor_admits_sparse_desc():
    """Un repo à description sparse mais avec keyword discriminant (ocr) doit
    être admis même si la similarité sémantique est modérée."""
    sparse_ocr_repo = make_repo(
        full_name="paddlepaddle/PaddleOCR",
        description="OCR toolkit",  # très sparse
        stargazers_count=4000,
        forks_count=600,
    )
    out = analyzer.filter_repos(
        [sparse_ocr_repo],
        DOMAINS,
        min_score=15,
        watched_owners=["paddlepaddle"],
    )
    names = [s["repo_full_name"] for s in out]
    assert "paddlepaddle/PaddleOCR" in names


def test_filter_repos_rejects_ml_research_no_specific_keyword():
    """Un repo ML research générique (transformer, image) sans keyword
    discriminant doit être rejeté (transformer/image NE sont plus dans la
    liste mots_cles Edge AI après le tightening)."""
    ml_research_repo = make_repo(
        full_name="bytedance/some-vision-research",
        description="Transformer-based image segmentation research, deep learning",
        stargazers_count=500,
    )
    out = analyzer.filter_repos(
        [ml_research_repo],
        DOMAINS,
        min_score=15,
        watched_owners=[],
    )
    names = [s["repo_full_name"] for s in out]
    assert "bytedance/some-vision-research" not in names


def test_filter_repos_sorted_by_score_desc():
    """La liste retenue doit être triée par score décroissant."""
    repos = [
        make_repo(
            full_name="a/low",
            description="real-time operating system RTOS embedded",
            stargazers_count=10,
        ),
        make_repo(
            full_name="b/high",
            description="real-time operating system RTOS kernel for ARM Cortex-M microcontroller",
            stargazers_count=2000, forks_count=200,
        ),
    ]
    out = analyzer.filter_repos(repos, DOMAINS, min_score=15, watched_owners=["a", "b"])
    if len(out) >= 2:
        scores = [s["score_total"] for s in out]
        assert scores == sorted(scores, reverse=True)


def test_score_repo_multi_domain_assigned():
    """Un repo qui matche plusieurs domaines a des scores > 0 sur plusieurs."""
    repo = make_repo(
        full_name="some/iot-rtos",
        description="real-time IoT framework with MQTT, BLE for ESP32 microcontrollers",
    )
    r = analyzer.score_repo(repo, DOMAINS, watched_owners=[])
    # Au moins 2 domaines avec score > 0 (Embarqué et IoT)
    nonzero = sum(1 for v in r["scores_par_domaine"].values() if v > 0)
    assert nonzero >= 2


# ─── Admission v2 : anti-domaines + orgs généralistes ────────────────────────

ANTI_DOMAINS = [
    {
        "nom": "ML research & large models",
        "definition": "Recherche académique en apprentissage automatique, entraînement de "
                      "grands modèles de langage LLM multi-milliards de paramètres, fine-tuning, "
                      "papiers de recherche, benchmarks, datasets d'entraînement, cloud GPU",
    },
    {
        "nom": "Web & app development",
        "definition": "Développement web frontend, frameworks JavaScript React Vue, players "
                      "vidéo HTML5, plateformes low-code par glisser-déposer, mini-programs, "
                      "sites e-commerce, dashboards web d'entreprise",
    },
]


def test_filter_v2_contrastive_rejects_llm_research():
    """Un repo LLM/recherche SANS mot-clé curé doit être rejeté par le filtre
    contrastif (anti-sim > wedge-sim) — c'est la voie d'entrée du bruit."""
    repo = {
        "full_name": "bigtech/mega-llm",
        "description": "Training framework for 300B parameter large language model, "
                       "distributed GPU cluster, research paper benchmarks",
        "language": "Python",
        "stargazers_count": 5000,
        "forks_count": 900,
        "pushed_at": "2026-06-01T00:00:00+00:00",
    }
    out = analyzer.filter_repos([repo], DOMAINS, min_score=15,
                                anti_domains=ANTI_DOMAINS)
    assert out == []


def test_filter_v2_contrastive_skipped_when_keyword_anchored():
    """Un mot-clé curé (signal humain haute précision) immunise contre le
    rejet contrastif — cas sophgo/tpu-mlir ('Machine learning compiler'
    penche ML-research mais 'tflite' est un ancrage wedge délibéré)."""
    repo = {
        "full_name": "vendor/edge-compiler",
        "description": "Machine learning compiler and research toolkit, converts "
                       "models to tflite for deployment",
        "language": "C++",
        "stargazers_count": 500, "forks_count": 100,
        "pushed_at": "2026-06-01T00:00:00+00:00",
    }
    out = analyzer.filter_repos([repo], DOMAINS, min_score=15,
                                anti_domains=ANTI_DOMAINS)
    assert len(out) == 1


def test_match_keywords_underscore_separated_names():
    """Les noms de repos type 'unitree_ros' doivent matcher les mots-clés
    ('_' et '/' normalisés en espaces ; les tirets sont préservés)."""
    repo = {"full_name": "unitreerobotics/unitree_ros", "description": ""}
    domains_kw = [{"nom": "Robotique", "mots_cles": ["ros", "unitree"]}]
    matched = analyzer._match_keywords(repo, domains_kw)
    assert "ros" in matched and "unitree" in matched


def test_filter_v2_contrastive_keeps_edge_inference():
    """Un vrai framework d'inférence edge reste admis (wedge-sim domine)."""
    repo = {
        "full_name": "Tencent/ncnn",
        "description": "High-performance neural network inference framework optimized "
                       "for mobile platforms, ARM NEON, no third-party dependencies, ncnn",
        "language": "C++",
        "stargazers_count": 19000,
        "forks_count": 4000,
        "pushed_at": "2026-06-01T00:00:00+00:00",
    }
    out = analyzer.filter_repos([repo], DOMAINS, min_score=15,
                                anti_domains=ANTI_DOMAINS)
    assert len(out) == 1
    assert out[0]["best_anti_similarity"] <= out[0]["best_similarity"] + analyzer.ANTI_MARGIN


def test_filter_v2_generalist_needs_both_signals():
    """Org généraliste : mot-clé + plancher sémantique (GENERALIST_MIN_SIM)
    requis ensemble — un mot-clé sur un repo sémantiquement hors-wedge ne
    suffit plus ; la même description sous une org vendor reste admise par
    ancrage mot-clé (règle v1 inchangée)."""
    desc = "Enterprise dashboard toolkit with OCR export plugin"  # kw 'ocr', sim wedge faible
    generalist = {
        "full_name": "alibaba/dashboard-toolkit",
        "description": desc, "language": "TypeScript",
        "stargazers_count": 500, "forks_count": 80,
        "pushed_at": "2026-06-01T00:00:00+00:00",
    }
    vendor = dict(generalist, full_name="rtthread/dashboard-toolkit")

    out_gen = analyzer.filter_repos([generalist], DOMAINS, min_score=15,
                                    generalist_owners=["alibaba"])
    out_ven = analyzer.filter_repos([vendor], DOMAINS, min_score=15,
                                    generalist_owners=["alibaba"])
    gen_names = [s["repo_full_name"] for s in out_gen]
    ven_names = [s["repo_full_name"] for s in out_ven]
    assert "alibaba/dashboard-toolkit" not in gen_names
    assert "rtthread/dashboard-toolkit" in ven_names


def test_filter_v2_backward_compatible_without_new_params():
    """Sans anti_domains ni generalist_owners, le comportement v1 est inchangé."""
    repo = {
        "full_name": "rtthread/rt-thread",
        "description": "RT-Thread is an open source IoT real-time operating system RTOS",
        "language": "C",
        "stargazers_count": 5000, "forks_count": 2000,
        "pushed_at": "2026-06-01T00:00:00+00:00",
    }
    out = analyzer.filter_repos([repo], DOMAINS, min_score=15)
    assert len(out) == 1


def test_load_anti_domains_from_config():
    antis = analyzer.load_anti_domains()
    assert len(antis) >= 3
    assert all("definition" in a and "nom" in a for a in antis)


# ─── Utility demotion (owner decision 2026-07-31) ────────────────────────────

def _score_with_penalty(repo, penalty):
    """Score the SAME repo with the demotion set to `penalty` — isolates the
    penalty from name-embedding variance (the name is part of the embedded text,
    so comparing two different names drifts by a point or two)."""
    old = analyzer.UTILITY_PENALTY
    analyzer.UTILITY_PENALTY = penalty
    try:
        return analyzer.score_repo(repo, DOMAINS)["score_total"]
    finally:
        analyzer.UTILITY_PENALTY = old


def test_utility_repo_is_demoted_not_excluded():
    """A helper-tool repo (name ends in 'tools') loses exactly UTILITY_PENALTY
    points but keeps a score — demotion, not exclusion."""
    util = make_repo(full_name="vendor/rtos-sdk-tools",
                     description="RTOS firmware SDK for ARM Cortex-M MCU, bare-metal drivers")
    with_pen = _score_with_penalty(util, 25)
    without = _score_with_penalty(util, 0)
    assert with_pen == max(0, without - 25)
    assert with_pen >= 0


def test_utility_patterns_docs_download_toolchain():
    """docs / download / toolchain names all trigger the demotion."""
    desc = "RTOS firmware SDK for ARM Cortex-M MCU, bare-metal drivers"
    for name in ("v/k230_rtos_docs", "v/hal_download_data", "v/toolchain_riscv_linux64"):
        repo = make_repo(full_name=name, description=desc)
        assert _score_with_penalty(repo, 25) < _score_with_penalty(repo, 0), name


def test_utility_pattern_not_overbroad():
    """Names merely containing 'doc'/'tool' mid-word are untouched — the
    docs?$/tools$ patterns anchor at the end."""
    desc = "RTOS firmware SDK for ARM Cortex-M MCU, bare-metal drivers"
    for name in ("v/doc-generator", "v/tooling-support", "v/board-sdk"):
        repo = make_repo(full_name=name, description=desc)
        assert _score_with_penalty(repo, 25) == _score_with_penalty(repo, 0), name
