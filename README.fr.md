# Minerva

**Langue :** 🇫🇷 Français · [English](README.md)

![tests](https://img.shields.io/badge/tests-96%20passing-brightgreen)
![license](https://img.shields.io/badge/license-Apache--2.0-blue)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![output](https://img.shields.io/badge/sortie-EN%20%2B%20FR-6b46c1)

**Minerva transforme l'écosystème open source hardware chinois — majoritairement
en chinois, fragmenté entre Gitee et GitHub — en intelligence technique prête à la
décision, en anglais et en français, que vous pouvez suivre dans le temps.**

Pipeline de veille technologique automatisée sur l'écosystème open source chinois (Gitee + GitHub), spécialisé **embarqué / IoT / robotique / edge-AI** : collecte, scoring sémantique, enrichissement LLM, et fiches techniques structurées bilingues + dashboard interactif + newsletter.

![Pipeline Minerva](docs/assets/pipeline.svg)

> 📚 Docs produit (en anglais) : [Positioning](docs/POSITIONING.md) · [Business](docs/BUSINESS.md) · [Sources & conformité](docs/SOURCES.md) · [Architecture](docs/ARCHITECTURE.md) · [Roadmap](ROADMAP.md)

## 🎯 Problème résolu

L'écosystème open source chinois publie une quantité massive de code embarqué, IoT, robotique et IA edge sur **Gitee** (et, pour certains fabricants, uniquement sur GitHub) — la plupart en **chinois**, dispersé entre des dizaines d'organisations (Alibaba, ByteDance, Baidu, Tencent, Huawei via OpenHarmony, Espressif, Rockchip, RT-Thread, Kendryte, Sipeed, Bouffalo, Sophgo, Unitree, etc.). Pour un ingénieur qui veut :

- repérer les frameworks RTOS, BSP, accélérateurs IA chinois équivalents (ou supérieurs) à ceux qu'il connaît côté ARM/x86,
- comprendre rapidement à quoi sert un projet sans parler mandarin,
- suivre l'évolution dans le temps (nouveautés / mises à jour) sans relire toute la liste à chaque fois,

…la barrière linguistique et la fragmentation des sources rendent la veille manuelle quasi impossible.

Minerva résout ce problème en **collectant**, **scorant**, **enrichissant via LLM** et **présentant en anglais (et français)** les repos pertinents, avec un dashboard interactif et une newsletter envoyable par email.

## 🧠 Fonctionnement

Pipeline en 3 étapes orchestrées par `src/pipeline.py` :

1. **Collecte (`fetcher.py` + `github_fetcher.py`)** — Interroge l'API Gitee v5 pour chaque organisation surveillée et chaque seed individuel. Authentifié via `GITEE_TOKEN` (rate-limit 4500 req/h), avec retry exponentiel sur les pages intermédiaires (anti-glitch d'API), filtrage des miroirs non surveillés et des repos `third_party_*`. Un **connecteur GitHub** (`github_fetcher.py`) capte en parallèle les organisations chinoises absentes de Gitee (Bouffalo Lab, Sophgo, Unitree, Kendryte/Canaan, Allwinner) via l'API REST GitHub (`GITHUB_TOKEN` optionnel), en produisant exactement le même schéma de repo — donc transparent pour le scoring et la génération de fiches.
2. **Scoring (`analyzer.py`)** — Score chaque repo sur 100 via des embeddings sémantiques multilingues (`sentence-transformers`) comparés aux 4 domaines configurés (`config/domains.json`), plus signaux de maturité (étoiles, dernier push, présence de README) et bonus pour les comptes officiels surveillés.
3. **Enrichissement (`translator.py`)** — Pour chaque repo au-dessus du seuil, appelle **Claude Haiku 4.5** avec la description et le README pour produire une fiche markdown structurée : type, problème résolu, fonctionnement, spécificité chinoise, équivalent occidental, maturité.

Diff incrémental : `state.json` mémorise `pushed_at` par repo. À chaque run, `output/diff_YYYYMMDD.md` liste **NEW / MODIFIED / DELETED** pour ne traiter que ce qui a bougé. Le LLM n'est appelé que pour les fiches manquantes ou modifiées.

## 📊 Chiffres clés

- **106 fiches techniques** (bilingues EN/FR) sur Gitee et GitHub — corpus délibérément *qualité-avant-quantité* : l'admission v2 a ramené le bruit big-tech de **77 % à 12 %** du corpus, plaçant les vendors hardware et la robotique au centre (Unitree 31, Sophgo 24, Espressif 13, Bouffalo 9, Kendryte, Sipeed, RT-Thread…)
- **22 organisations Gitee** + **5 organisations GitHub** surveillées, 15 représentées · **4 domaines** — Embarqué 55, Edge AI 45, Robotique 9, IoT 2. *Note : 2 313/3 660 repos Gitee sont stales > 2 ans (OpenHarmony a migré) — le prochain levier de couverture est un connecteur AtomGit/GitCode (roadmap).*
- **4 domaines** couverts (Embarqué, IoT, Robotique, Edge AI) avec scoring sémantique
- **Coût LLM** : ~$0.01 par repo (paire EN+FR, Haiku 4.5), bootstrap complet ~$2-4
- **Rescoring sans LLM** possible via `scripts/rescore.py` ($0)
- **Tests automatisés** : 96 tests pytest, CI GitHub Actions

## 🚀 Démo en 30 secondes

```bash
# 1. Cloner le repo et installer les dépendances
git clone <repo-url> minerva && cd minerva
pip install -r requirements.txt

# 2. Ouvrir le dashboard pré-généré (aucun token requis)
start output/dashboard.html      # Windows
xdg-open output/dashboard.html   # Linux
open output/dashboard.html       # macOS
```

Le dashboard charge instantanément (single-file HTML, JSON inliné), filtre par domaine/type/score, recherche full-text dans les fiches.

**Lancer un run complet du pipeline** (nécessite `.env` avec `GITEE_TOKEN` et `ANTHROPIC_API_KEY`) :

```bash
python src/pipeline.py
```

Génère/met à jour les fiches incrémentalement (~10 min, ~$0.10-$0.50 selon le nombre de nouveautés), puis :

```bash
python scripts/build_dashboard.py    # rebuild output/dashboard.html
python scripts/build_newsletter.py   # rebuild output/newsletter_YYYYMMDD.{html,txt}
```

## 🚀 Utilisation

### Pipeline complet (réseau, ~10 min en mode incrémental)

```bash
# .env doit contenir GITEE_TOKEN et ANTHROPIC_API_KEY (GITHUB_TOKEN optionnel)
python src/pipeline.py
```

### Dashboard interactif (single-file HTML)

```bash
python scripts/build_dashboard.py
# → output/dashboard.html (filtres, recherche, tri, autonome)
```

### Newsletter (HTML + TXT)

```bash
python scripts/build_newsletter.py
# → output/newsletter_YYYYMMDD.html (riche)
# → output/newsletter_YYYYMMDD.txt  (envoyable par email)
```

### Rescoring local sans appel LLM (après modif `domains.json`)

```bash
python scripts/rescore.py
# Met à jour les scores et domaines dans les fiches existantes, $0
```

## 📁 Structure du projet

```
minerva/
├── config/
│   ├── domains.json          # 4 domaines + mots-clés CN/EN + poids
│   └── sources.json          # comptes_gitee/github, seeds, min_score
├── src/
│   ├── fetcher.py            # API Gitee : pagination, retry, rate-limit
│   ├── github_fetcher.py     # API GitHub : orgs chinoises absentes de Gitee
│   ├── analyzer.py           # scoring sémantique multi-domaine + filtres durs
│   ├── embedder.py           # embeddings multilingues (sentence-transformers)
│   ├── translator.py         # appel Claude Haiku, génération fiche (EN/FR)
│   ├── fiche_schema.py       # schéma Pydantic parse/génère les fiches
│   └── pipeline.py           # orchestration + diff incrémental (Gitee + GitHub)
├── scripts/
│   ├── build_dashboard.py    # dashboard HTML interactif
│   ├── build_newsletter.py   # newsletter HTML + TXT
│   └── rescore.py            # rescore offline ($0)
├── output/                   # fiches, dashboard, newsletter, state.json, diffs
├── data/                     # JSON bruts Gitee + fiches Phase 0
├── .env                      # GITEE_TOKEN, ANTHROPIC_API_KEY, GITHUB_TOKEN (gitignoré)
└── requirements.txt
```

## 🗺️ Domaines couverts

Définis dans `config/domains.json` avec des mots-clés bilingues CN/EN et des poids relatifs.

| Domaine     | Exemples concrets repérés                                                    |
|-------------|------------------------------------------------------------------------------|
| Embarqué    | RT-Thread, AliOS-Things, TencentOS-tiny, ESP-IDF, OpenHarmony device drivers |
| IoT         | LuatOS, OpenHarmony OS, BL-MCU SDK, MQTT/LwIP stacks                          |
| Robotique   | RoboMaster RoboRTS, Unitree SDK, drones                                       |
| Edge AI     | ncnn (Tencent), PaddleOCR, MNN, K230 KPU SDK, nncase, Sophgo tpu-mlir         |

## ⚠️ Limitations connues

- **Gitee `/search/repositories` est cassé côté serveur** : retourne `[]` pour toutes les requêtes. Workaround : `seeds_gitee` (slugs `owner/repo` ajoutés à la main) + collecte exhaustive par organisation.
- **Token Gitee requis** pour les runs réels : sans token, le rate-limit est de 60 req/h + WAF Baidu BDWAF agressif (filtré comme bot après ~30 req).
- **Token Anthropic requis** pour générer de nouvelles fiches. Le rescoring local (`rescore.py`) fonctionne sans token Claude.
- **Certaines organisations chinoises ne sont que sur GitHub.** Le **connecteur GitHub** (`github_fetcher.py`) en capte désormais une partie (Bouffalo Lab, Sophgo, Unitree, Kendryte/Canaan, Allwinner) ; d'autres restent à ajouter (GigaDevice, DeepRobotics, Huawei en direct, Xiaomi…) — il suffit de compléter `comptes_github` / `seeds_github` dans `config/sources.json`.
- **API GitHub anonyme = 60 req/h** : un run complet multi-orgs nécessite un `GITHUB_TOKEN` (PAT, même en lecture seule → 5000 req/h). Sans token, la collecte GitHub fonctionne mais reste limitée.

## 📈 Roadmap

### Fait ✅

- **Connecteur GitHub** pour les organisations chinoises absentes de Gitee (Bouffalo, Sophgo, Unitree, Kendryte, Allwinner) — `src/github_fetcher.py`, branché dans le pipeline, testé.
- **Sortie bilingue native** — chaque run de `python src/pipeline.py` génère et maintient les deux jeux de fiches : anglais (par défaut) dans `output/fiches/`, français dans `output/fiches_fr/` — une seule génération de faits + traduction fidèle, zéro drift. README et CHANGELOG bilingues.
- **Tests unitaires + CI GitHub Actions** — 96 tests pytest (`analyzer`, `translator`, `fetcher`, `github_fetcher`, `fiche_schema`).
- Filtrage des repos archivés / abandonnés (`translator.is_archived` : flag `archived`, statut `关闭`, staleness > 2 ans).

### Court terme

- Ajouter des seeds confirmés pour WCH (CH32V), Sipeed/MaixPy, MilkV, StarFive.
- Étendre `comptes_github` (GigaDevice, DeepRobotics, Xiaomi…) une fois les logins d'org confirmés.

### Moyen terme

- Détection automatique des nouveaux comptes Gitee/GitHub pertinents (forks d'orgs surveillées, contributeurs récurrents).
- Génération d'une vue chronologique dans le dashboard (timeline des nouveautés).
- Envoi automatique de la newsletter par SMTP / Mailjet.

### Long terme

- Annotation manuelle (interface) pour valider/corriger les fiches LLM et créer un dataset de fine-tuning.
- Comparatif benchmark cross-projets pour les frameworks d'inférence (ncnn vs MNN vs TFLite vs ONNX Runtime sur ARM).
- Extension à d'autres écosystèmes asiatiques (japonais : Renesas, coréens : Samsung Tizen).

## 🛠️ Prérequis

```bash
pip install -r requirements.txt
```

`.env` à la racine :

```
GITEE_TOKEN=xxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxx        # optionnel — passe la collecte GitHub de 60 à 5000 req/h
```

## 📄 Licence

Voir [LICENSE](LICENSE).
