# Changelog
**Langue :** 🇫🇷 Français · [English](CHANGELOG.md)

Toutes les évolutions notables du projet Minerva sont consignées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/).

## [0.25.2] — 2026-08-03

### Corrigé — Tripwire anti-effondrement de collecte (post-mortem du 1er cycle CI)

Le premier cycle planifié a tourné avec des secrets corrompus (valeurs collées
avec un retour à la ligne → HTTP 401 sur chaque appel Gitee ET GitHub). Chaque
owner s'est « énuméré » vide, et le pipeline a conclu que tout le corpus avait
disparu : **105/105 repos marqués supprimés**, state écrasé, 105 tombstones
enregistrées. Rien n'a atteint le repo/site public uniquement parce que le
rebuild a planté sur le corpus vide — un pare-feu accidentel, pas conçu.
Désormais conçu :

- **Fetchers (Gitee + GitHub)** : une erreur dure en page 1 avec zéro repo
  collecté (401/403/5xx/réseau) lève désormais l'erreur de pagination pour que
  l'owner rejoigne `failed_owners` et que ses repos soient protégés de la
  fausse suppression — avant, ça retournait une liste vide (« normal
  behavior »). 404 et comptes réellement vides inchangés.
- **Tripwire pipeline** : si >50 % des repos suivis seraient supprimés en un
  run (corpus ≥10), abandon avec `CollectionCollapseError` (exit 2) — state,
  fiches et diff intacts. Une suppression de masse est un échec de collecte
  jusqu'à preuve du contraire.
- **Garde miroir `build_history`** : refuse de tombstoner >50 % du ledger
  vivant (`--allow-mass-removal` pour passer outre délibérément) — l'artefact
  d'historique ne doit jamais enregistrer un échec comme du signal.
- +5 tests (**118** au total). La leçon de l'hystérésis d'admission (bearpi)
  est arrivée à l'échelle maximale dès le cycle nº1 — elle est désormais
  mécanisée aux trois niveaux.

## [0.25.1] — 2026-07-31

### Modifié — Adoucissement de l'esthétique de précision (verdict propriétaire, point 2)

Le cadre « instrument calme » suggérait une précision de mesure que le score n'a
pas. Adouci sans refonte : retrait du « top N% of corpus » solennel du readout
fiche (EN+FR) ; légende réécrite en vérité simple — « un signal de tri grossier …
une clé de tri, pas une mesure de l'écosystème » ; tooltip dashboard aligné ;
« most relevant » → « highest-scored » (un fait de score, pas une affirmation sur
le monde). `docs/SCORING.md` gagne une section **Honest limits** énonçant
platement les deux réserves structurelles : provenance du score partiellement
circulaire aujourd'hui (le rescore embedde la prose LLM de la fiche — le rescore
source-first est le correctif prévu) et admission qui respire au seuil (cas
bearpi). Les garde-fous V1.1 de la ROADMAP gagnent une précondition dure :
**hystérésis d'admission avant toute UI de signal** (admission collante, bande
morte, ou libellé explicite « left threshold »). 113 tests ; publish/ reconstruit.

## [0.25.0] — 2026-07-31

### Ajouté / Corrigé — Fresh run de lancement + bootstrap historique + demote corpus-wide

- **Fresh run du pipeline** (3 868 repos énumérés) : 0 nouveau, 6 paires
  modifiées régénérées, 99 inchangés, corpus **106 → 105** —
  `bearpi/bearpi-hm_nano` est passé sous le seuil d'admission à ce run (score
  limite, pas une suppression de fetch) ; ses fiches EN+FR et pages nettoyées.
- **`rescore.py` corrigé puis appliqué corpus-wide** : (a) le drift EN-seul
  connu — le jumeau FR reçoit désormais le MÊME score/domaine que le scoring EN
  (101 FR synchronisées) ; (b) un bug latent de corruption de domaine — il
  écrivait les noms BRUTS de la config (« Embarqué ») dans les fiches ; désormais
  localisé par langue via `_translate_domain`. 99 scores + 41 domaines mis à
  jour, 0 erreur de parse, `state.json["scores"]` normalisé (105 entrées — clôt
  le TODO schéma mixte).
- **Le demote des utilitaires est vivant dans le corpus** : `esp-gitee-tools`
  nº4 → **nº92** (86 → 52) ; les 7 repos utilitaires occupent désormais les
  rangs 92-105. Nouveau top-10 de l'explorateur entièrement décisionnel
  (rt-thread, ESP8266_RTOS_SDK, unitree_ros, esp-idf, ncnn, xr_teleoperate,
  esp-at, nncase, LuatOS, esp-iot-solution).
- **Artefact historique bootstrapé** (dry-run puis réel) : `repo_ledger.json`
  (105 repos, `first_seen` = baseline 2026-07-31) + première ligne
  `history.jsonl` (`bootstrap: true`, aucun NEW revendiqué — garde-fou 1
  respecté).
- Rééquilibrage des domaines par le rescoring sur prose : domaines primaires
  désormais Embarqué 59 / Edge AI 23 / Robotique 17 / IoT 6 (les chiffres de la
  landing sont calculés depuis les données au build, la page suit
  automatiquement).
- **`scripts/collect_public.py`** — le manifeste de déploiement rendu exécutable :
  copie allowlist `output/` → `publish/` (git-ignoré) + mode `--check` ; vérifié
  218 fichiers, zéro interne. Déployer `publish/`, jamais `output/`.
- Dashboard/site/newsletter reconstruits sur le corpus 105 (« as of
  2026-07-31 ») ; formulaires toujours désactivés (pas de handle) ; 113 tests
  verts.

## [0.24.0] — 2026-07-31

### Modifié — Doctrine stop-ship : la cadence suit l'opérateur ; demote des utilitaires

Doctrine propriétaire durcie (`docs/DECISIONS.md` §12) : aucun push tant qu'une
trahison d'honnêteté existe ; la vitrine doit être digne de la doctrine avant
tout sujet de croissance.

- **La cadence suit l'opérateur, structurellement.** Les builds par défaut ne
  promettent AUCUNE cadence — landing/pro/fiches (EN+FR) disent « after each
  corpus run » / « après chaque run du corpus » ; le mot « weekly » ne peut être
  produit que par le workflow CI hebdomadaire lui-même (`MINERVA_CADENCE=weekly`
  défini dans son step de rebuild, nulle part ailleurs). Vérifié dans les deux
  modes : build défaut = 0 claim de cadence dans le chrome ; build mode-CI =
  wording weekly présent. Un build manuel ne peut pas sur-promettre, par
  construction.
- **Demote des utilitaires dans la formule de score** (`analyzer.score_repo`) :
  `UTILITY_PENALTY = 25` pour les repos matchant `docs$|download|toolchain|tools$`
  — rétrogradation, pas exclusion ; même motif que la règle de curation de
  vitrine. Prend effet au fresh run (pas de rescore intermédiaire → évite le
  FR-drift connu de `rescore.py`). Vérification manuelle du top-10 post-fresh-run
  ajoutée à la revue pré-push. +3 tests isolant la pénalité (**113** au total).
- **Tiers payants requalifiés « Planned scope — not built yet »** : retrait de
  « guaranteed », « REST API (read, 10k req/month) », « 99.5% SLA », « Daily
  newsletter » comme des faits ; l'engagement −30 % waitlist conservé comme
  engagement. FAQ alignée (« planned, not built yet »).
- **Définition de « prêt à publier »** (7 cases stop-ship) consignée dans
  `docs/DEPLOYMENT.md` §6.

## [0.23.0] — 2026-07-31

### Ajouté / Corrigé — Arbitrages pré-lancement + correctifs de confiance (réponse à l'audit)

Quatre arbitrages propriétaire (consignés dans `docs/DECISIONS.md` §11), puis les correctifs :

- **Fraîcheur hébergée décidée** : `.github/workflows/scheduled-run.yml` — cron
  hebdo du lundi (pipeline → historique → rebuild → secret-scan → tests →
  commit auto), avec une garde explicite qui no-op en vert tant que les secrets
  du repo n'existent pas — le fichier est inerte avant le lancement. L'*envoi*
  de la newsletter reste un geste manuel du propriétaire.
- **Le placeholder Buttondown dégrade désormais** : `MINERVA_NEWSLETTER` n'a
  plus de valeur par défaut ; non défini ⇒ tous les formulaires email sont
  rendus désactivés (« sign-up opens at launch ») + avertissement bloquant au
  build — un formulaire vivant postant vers un compte non possédé aurait fait
  fuiter les emails des visiteurs. Asymétrie avec le placeholder d'URL fermée.
- **Curation de vitrine (scoring reformulé, formule gelée)** : Featured /
  Runners-up / preuve landing ne mettent en avant que des fiches décisionnelles ;
  les repos utilitaires (docs/download/toolchain/tools — ex. `esp-gitee-tools`,
  auparavant nº4) restent dans le corpus et l'explorateur mais ne portent plus
  la preuve. Les rangs affichés restent les vrais rangs du corpus. **Légende**
  score/confiance ajoutée (pages fiche + tooltips dashboard). Retraitement de la
  formule → backlog V1.1.
- **`legal.html`** — confidentialité (site statique, ni cookies ni analytics ;
  email seulement via abonnement volontaire Buttondown), provenance du contenu &
  mention LLM, politique corrections/retraits pour les mainteneurs, licences,
  contact. Lié depuis chaque footer. Fausse affirmation « EU-hosted » corrigée
  (Buttondown est américain).
- **106 pages fiches jumelles FR** — `f/<slug>.fr.html` avec surface de
  décision localisée (titres, labels, légende, panneau latéral), `lang="fr"`,
  paires hreflang (domaine réel uniquement), bascule EN↔FR dans le fil
  d'Ariane. La trust-line « EN + FR » est désormais vérifiable sur le site.
  Purge + sitemap couvrent les deux langues.
- **Balayage des chiffres périmés (dashboard)** : « $0.005/fiche » →
  « $0.01 par paire bilingue » ; « weekly incremental execution » →
  « incremental by design — every run is dated » ; « ~$2 (140 fiches) » →
  « ~$1 (106 paires bilingues) » ; « ~3 100 lignes » invérifié retiré ;
  description du scoring ère-mots-clés → embeddings sémantiques + admission v2.
  **Conflation « orgs surveillées » corrigée** (27 surveillées depuis la config
  vs 15 produisant des fiches) sur landing + dashboard.
- **Page Pro dé-datée** : « Launching Q3 2026 » (sur le point de devenir faux) →
  « launch when it's ready » ; roadmap Now/Next/Later/Exploring. Engagement
  −30 % waitlist conservé (un choix, pas une date).
- **Bug sticky toolbar-sous-nav du dashboard corrigé** (`top: 48px`) ; compte de
  fiches de la carte OG paramétré (`__OG_N__`).
- Vérifié : 110/110 tests ; code `<script>` du dashboard identique au caractère
  près (seule la constante de données `RUNNER_NAMES` injectée a changé — l'effet
  voulu de la curation) ; 0 affirmation périmée restante dans les pages
  construites. Rien poussé ; pas de fresh run.
- **Attrapé par la revue de preuve** : le footer du dashboard (template séparé)
  n'avait pas de lien `legal.html` — ajouté. Chaque page construite lie
  désormais Legal & privacy.

## [0.22.0] — 2026-07-31

### Modifié — Passe corrective de design D5 : instrument, pas template

Deux audits indépendants (Grok, Lovable) ont convergé : structure/UX solides,
mais le rendu final lisait comme un « template premium » générique, pas un
« instrument analytique calme ». Vérifié dans le code : stack de police système
par défaut, rayons « friendly SaaS » 5-8px, grille décorative quasi invisible.
Décision corrective — une seule passe cohérente, pas une refonte — validée sur une
surface de référence unique (`docs/design/fiche-d5.html`) puis propagée
landing → dashboard → pro.

- **Nouveau registre borné `--slab`** (`#1B1E20` fond / `#F5F6F4` texte) pour
  exactement deux surfaces structurelles par page : une **status-line** partagée
  sous la nav (marque + « Snapshot · as of {date} » + compte de fiches) et, là où
  des données de fiche existent, **un** panneau readout (score/confiance/domaine)
  réordonné **avant** le titre lisible. Garde-fou appliqué : 1 readout max par
  surface, 0 sur Pro (pas de données de fiche), et l'Explorer du dashboard reste
  délibérément sur le registre clair — 106 lignes qui se re-rendent à chaque
  frappe/flèche rendraient un basculement slab surchargeant.
- **Échelle de rayons aplatie** (`--r-0`/`--r-sm`/`--r-pill` remplaçant les
  valeurs ad hoc 2-8px) sur tous les conteneurs de landing/dashboard/fiche/pro —
  le correctif à plus fort effet de levier contre le look « carte SaaS
  générique ».
- **Règle typographique resserrée** (décision propriétaire en cours de passe) :
  le mono est cantonné à status-line / wordmark / score / métriques / labels /
  repères de section / IDs uniquement. Les H1/H2 éditoriaux restent en **sans**,
  plus fermes (poids 700, tracking −0,03em, interligne resserré) — jamais mono
  par défaut. Le H1 de fiche qui reste mono est l'exception identifiant (un id
  owner/repo), pas un précédent ; la prose d'analyse est inchangée.
- **Contraste vérifié et un vrai problème corrigé** : `--signal-on-slab`
  (`#5B948F` sur `--slab`) donne 4,93:1 (calcul WCAG, passe l'AA). Trouvé que la
  valeur domaine du readout était en texte teinté domaine sur slab à ≈3,78:1
  (échec AA) — recolorée en `--slab-ink` ; l'identité couleur du domaine est
  désormais portée uniquement par le liseré gauche du readout.
- **Bloc `<script>` du dashboard intact** — diffé au caractère près contre
  l'extraction pré-passe ; identique. Toute l'interactivité (recherche/filtres/
  tri/clavier/presets) non affectée ; le « point » de domaine dans la liste de
  l'Explorer est devenu un liseré gauche calme en CSS pur (simple re-style de
  l'élément existant, aucun changement DOM/JS).
- **Vérifié** : 110/110 tests, `node --check` du JS dashboard propre, 0 token
  sombre résiduel, 0 wording « live » factice, garde-fous confirmés sur le vrai
  rendu de build. Rien poussé, aucun fresh run.

## [0.21.0] — 2026-07-31

### Modifié — Design Track câblé : système visuel « instrument analytique calme »

- **Re-skin complet câblé dans `build_site.py` et `build_dashboard.py`**,
  remplaçant le look dark-startup-SaaS (quasi-noir + rouge-alarme + glow) par le
  langage validé « instrument analytique calme » clair d'abord (D1–D4, voir
  `docs/DESIGN_TRACK.md`) : papier technique + encre (`#F5F6F4`/`#1B1E20`), un
  accent signal unique teal-ardoise minéral (`#2F5A5C`, séché depuis un `#0F766E`
  initial), mono pour toute valeur quantitative/identifiant/label, confiance rendue
  en marques d'encre en losange (◆◆◆/◆◆◇/◆◇◇) au lieu d'un point coloré,
  composants plats à filet (zéro ombre flottante), grille de fond quasi
  subliminale.
- **Landing / Pro / Fiche** (`build_site.py`) : `BASE_CSS` + chrome partagés (nav,
  footer, atomes tag/conf/score/form) factorisés une fois ; labels de section mono
  numérotés (`01 · …`) ; le bloc équivalent occidental de la fiche reste le héros de
  lecture surligné en sans humaniste (le mono est réservé aux
  identifiants/métriques/labels — règle de vigilance propriétaire de D3, contraignante
  au câblage) ; `<link rel="icon">` + méta `og:image` câblés (og:image émis
  seulement avec un vrai `MINERVA_SITE_URL`, cohérent avec la règle de dégradation
  placeholder existante).
- **Dashboard** (`build_dashboard.py`) : sections Hero, Featured, Landscape
  (graphiques), Runners-up, Explorer 2-panneaux et Pipeline re-skinnées dans le même
  système. **Toute l'interactivité reste inchangée au caractère près** — recherche,
  chips domaines, selects compte/type/maturité, tri, presets, reset, focus `/`,
  Escape, navigation clavier ↑/↓ intacts ; seule la présentation a bougé. Ajout d'un
  helper JS `confMarks()` (miroir du nouveau `conf_dm()` Python) pour que la
  confiance s'affiche en marques d'encre dans la liste et le panneau détail, cohérent
  avec toutes les autres surfaces.
- **Assets de marque** : `favicon.svg` (repère de registre/ouverture + tick minéral,
  lisible sur onglet clair ou sombre) et `og.svg` (carte sociale 1200×630 : mark +
  wordmark, ligne de stats mono, le pont équivalent-occidental comme moment-signal)
  désormais générés par `build_site.py` dans `output/`.
- **Vérifié** : 110/110 tests verts (aucun changement de couche données —
  `build_items`, `compute_aggregates`, tier de confiance, logique
  sitemap/robots/dégradation-placeholder toutes intactes) ; JS inline du dashboard
  revalidé via `node --check` ; balayage complet confirmant 0 token dark-theme
  résiduel, 0 wording « live » factice, 0 `minerva.example` dans un fichier servi.
  **Rien poussé, aucun fresh run** — `scripts/build_history.py` reste en attente
  selon le checkpoint en vigueur.
- **Ouvert** : `output/og.svg` doit encore être rasterisé en `og.png` au moment du
  déploiement (aucun rasteriseur câblé dans le build) ; voir `docs/DEPLOYMENT.md`.

## [0.20.0] — 2026-07-30

### Ajouté — Fondation historique Track 2 (implémentée, non exécutée) + parité docs

- **`scripts/build_history.py`** — le générateur de l'artefact d'historique de runs
  (committé) : une fonction pure `compute_history()` (baseline `first_seen` au
  bootstrap, MODIFIED via diff de `pushed_at`, DELETED en **tombstone**, détection
  de source Gitee/GitHub) + les I/O qui écrivent `output/repo_ledger.json` (état
  durable par repo) et ajoutent `output/history.jsonl` (une ligne par run).
  `--dry-run` supporté. **Non exécuté à ce stade** — il doit être bootstrapé par le
  run de lancement frais pour ne pas gâcher la baseline. Schéma dans
  `docs/HISTORY_ARTIFACT.md`.
- **Tests** : +5 (**110** au total) — `tests/test_build_history.py` fige les deux
  garde-fous d'honnêteté et la détection new/modified/removed/retour sur données
  synthétiques (aucun artefact réel généré).
- **`docs/DEPLOYMENT.md`** — manifeste de déploiement V1 explicite : le set web
  public exact (`index/dashboard/pro/f/sitemap/robots`), ce qui ne doit jamais être
  servi (`state.json`, caches, logs, newsletters, fiches brutes), l'exception de
  l'artefact d'historique (servi seulement quand la couche signal arrivera), et les
  deux préconditions avant push.
- **Parité de `CHANGELOG.fr.md` rétablie** — back-fill 0.11.0 → 0.19.0 (9 versions
  de retard) ; changelogs EN/FR désormais à parité complète de versions.

## [0.19.0] — 2026-07-30

### Corrigé — Hygiène de publication Track 1 + cohérence narrative (local, rien poussé)

- **Dégradation propre du placeholder** (`build_site`) : tant que `MINERVA_SITE_URL` vaut le placeholder `minerva.example`, le build ne produit **plus aucune URL absolue factice** — il omet `<link rel=canonical>`, `og:url`, toutes les entrées `<loc>` du sitemap (`sitemap.xml` vide et commenté) et la ligne `Sitemap:` du robots. Un vrai domaine les réactive. `MINERVA_CONTACT` dégrade de même le CTA Enterprise vers la newsletter.
- **Fin du wording « live » factice** (garde-fou Track 2) : badge dashboard `Live · updated` → **`Snapshot · as of {last_run}`** (point pulsé rendu statique) ; hero « currently live on the radar » → « tracked in this snapshot » ; CTA landing « Explore the **live** dashboard » → « Explore the dashboard ».
- **Corrections de cohérence des fiches** : le « top N % » par fiche était figé à 100 % pour toutes → vrai percentile de score ; le CTA source affichait toujours « View on Gitee » → désormais adapté à la source (« View on GitHub » pour les 67 fiches issues de GitHub, « View on Gitee » pour les 39 de Gitee).
- **Libellés dashboard** : « Gitee organizations » → « Organizations », stack/légende → « Gitee + GitHub » (les deux sources) ; retrait d'un « 27 orgs » périmé.
- **Éditorial stale retiré** de l'arbre publié : `output/dispatch_00.md` (édition d'ouverture de l'ancien corpus, désormais factuellement fausse) déplacé vers `archive/` (préservé, git-ignoré, jamais servi). `output/dispatch_*.md` + `archive/` ajoutés au `.gitignore`.
- Vérifié : 106 fiches EN ↔ 106 FR (zéro asymétrie), 106 pages `f/` = 106 repos `state.json` = 0 orphelin, 105/105 tests verts. `docs/UX_REDESIGN.md` et `ROADMAP.md` mis à jour (statut hygiène résolu + réserve sur le manifeste de déploiement : ne publier que `index/dashboard/pro/f/sitemap/robots`, pas `state.json` etc.).

## [0.18.0] — 2026-07-30

### Modifié — Refonte UX Phase 2 : explorateur de dashboard fiche-first

- **« Explore » du dashboard transformé d'une grille de cartes en explorateur 2 panneaux** (`build_dashboard`) : une **liste** compacte et scannable (gauche) + un **panneau détail léger, sticky** (droite) montrant la couche décision (Problème / Comment / Spécificité chinoise / **Équivalent occidental** mis en avant / maturité / confiance + liens source & fiche complète). Ouvre sur la fiche du haut (fiche-first) ; `↑`/`↓` et clic parcourent le corpus rapidement — la sensation d'exploration rapide est préservée (exigence propriétaire).
- **Vues rapides par cas d'usage** (presets) : benchmarking Edge-AI, stacks robotique, RTOS/BSP/firmware, haute confiance uniquement — en plus des filtres domaine/type/compte/maturité, de la recherche et du tri (tous conservés). Nouveau filtre de confiance côté client.
- Texte « how it works » du diagramme corrigé (Gitee+GitHub, sémantique + anti-bruit, EN+FR). JS inline validé via `node --check`.

### Modifié — Refonte UX Phase 1 : landing + hygiène de publication

- **Landing reconstruite** (`build_site.build_landing`) autour du cadrage validé (`docs/UX_REDESIGN.md`) : hero de proposition de valeur (« Decision-ready intelligence on China's open-source hardware », B2B mais accessible aux ingénieurs) ; une **vraie fiche mise en scène** (sophgo/tpu-mlir) rendant la couche décision avec l'équivalent occidental surligné + badge de confiance — la preuve anti-annuaire ; une section **cas d'usage** (tech scouting / competitive intelligence / sourcing-BOM / benchmarking edge-AI) ; un « how it works » exact (Gitee+GitHub, scoring sémantique, EN+FR) ; des chiffres de corpus honnêtes (106 fiches, part vendors) ; un bandeau de confiance sources & méthode ; des CTA d'entonnoir (dashboard → brief hebdo → Pro).
- **`docs/UX_REDESIGN.md`** — le cadrage validé + plan de phases + décisions propriétaire.

### Corrigé — Hygiène de publication

- `build_site` **purge désormais les pages fiches orphelines** (141 pages stales de l'ancien corpus retirées ; sitemap 179 → 109 URLs, ne reflétant que les 106 fiches vivantes).
- `build_site` **avertit clairement** quand `MINERVA_SITE_URL` vaut encore le placeholder `minerva.example` (canonical/OG/sitemap seraient faux) — mettre le vrai domaine avant tout déploiement public.
- Newsletters datées stales retirées (dernière conservée).

## [0.17.0] — 2026-07-30

### Ajouté — Moisson des orgs GitHub (corpus 43 → 106)

- Moisson complète authentifiée des 5 orgs vendors GitHub configurées (bouffalolab, sophgo, unitreerobotics, kendryte, allwinner-zh) via `GITHUB_TOKEN`. L'admission v2 a retenu **63 nouveaux repos wedge-purs** sur 221 énumérés : Unitree 31 (robotique), Sophgo 24 (edge-AI / RISC-V), Bouffalo 9 (MCU), Kendryte 3.
- **Corpus 43 → 106 fiches**, 15 owners ; **part big-tech 30 % → 12 %** (77 % avant recalibrage). Domaines : Embarqué 55, Edge AI 45, **Robotique 2 → 9**, IoT 2.
- Invariant incrémental confirmé de bout en bout : un run anonyme a généré 44 fiches avant la limite de 55 req/h, puis la relance avec token a bootstrapé ces 44 gratuitement et n'a généré que les ~20 restantes (~45 s au total).
- Dashboard, newsletter et site statique reconstruits sur le corpus de 106 fiches ; chiffres README (EN/FR) mis à jour.

## [0.16.0] — 2026-07-30

### Ajouté — Durcissement sécurité (pré-publication)

- **`.gitignore` durci** : ignore désormais toutes les variantes `.env.*` (pas seulement `.env`) plus les formes de secrets courantes (`*.pem`, `*.key`, `*.p12`, `secrets.json`, `credentials.json`) ; `.env.example` explicitement autorisé. Vérifié par simulation que `.env.local` / `.env.production` / `.env.bak` ne sont plus committables.
- **`.env.example`** — gabarit placeholder pour les trois clés (GITEE_TOKEN, ANTHROPIC_API_KEY, GITHUB_TOKEN optionnel).
- **`scripts/secret_scan.py`** — scan local pré-push : échoue si un motif de vraie clé (Anthropic / PAT GitHub / access_token Gitee) apparaît dans un fichier committable, ou si un vrai `.env` est suivi par git. Vérifié : détecte une clé plantée ; le vrai repo est propre (45 fichiers).
- **`SECURITY.md`** — politique de gestion des secrets, checklist obligatoire avant premier push (rotation des clés dev, lancer le scan, confirmer `.env` non staged, `GITHUB_TOKEN` moindre privilège), et guidance de divulgation responsable.
- **Garde CI consolidée** pour lancer `scripts/secret_scan.py` (source unique de vérité) au lieu d'un grep inline.

### Vérifié

- Balayage complet des secrets : les vrais GITEE_TOKEN / ANTHROPIC_API_KEY n'apparaissent **que** dans le `.env` local (gitignoré) ; aucun token dans les logs ou un artefact généré.

## [0.15.0] — 2026-07-30

### Modifié — Recalibrage du corpus : admission v2 (anti bruit big-tech)

Décision produit : le corpus doit visiblement coller au wedge (embarqué / IoT / robotique / edge-AI sur silicium chinois), pas de l'OSS big-tech générique. Implémenté comme deux règles d'admission pilotées par la config — la **formule de score est intacte** et les invariants incrémentaux préservés :

- **Filtre anti-domaines contrastif** (repos sans mot-clé uniquement) : 3 « anti-domaines » embarqués (recherche ML & grands modèles, dev web & app, infra cloud & big-data) dans `config/domains.json` ; un repo à zéro mot-clé curé est rejeté quand `best_anti_similarity > best_similarity + ANTI_MARGIN (0.08)`. Les mots-clés curés donnent l'immunité (un ancrage humain prime sur une similarité statistique).
- **Les orgs généralistes exigent un mot-clé curé** (`generalist_orgs` dans `config/sources.json`) : la calibration a montré que tout le bruit confirmé entrait par la voie sémantique-seule sans mot-clé, tandis que les vrais positifs (MNN, PaddleOCR) en portent un. Admission pour ces orgs = ≥1 mot-clé ET `sim ≥ 0.35`.
- **Chirurgie de la liste de mots-clés** : ajout de termes wedge haute précision (risc-v, riscv, toolchain, u-boot, openharmony, harmonyos, ros, ros2, quadruped, unitree, motor, servo, motion control, tpu, maix, maixpy, maixcdk) ; retrait des ouvreurs de bruit prouvés (`sdk`, `control`, `motion`, `量化` — ce dernier matché en sous-chaîne dans 轻量化 « léger »).
- **Le matching de mots-clés normalise `_` et `/`** en espaces pour que des noms comme `unitree_ros` s'ancrent correctement (traits d'union préservés pour `risc-v`).
- **Les seeds GitHub remplacent désormais les miroirs stales de même slug** (`pipeline._fetch_github_seeds`) : Kendryte/Bouffalo gardaient des miroirs Gitee morts qui masquaient les vrais repos GitHub et les faisaient hard-filtrer silencieusement.

**Effet corpus (run complet frais, 3 660 repos énumérés) :** 176 → **43 fiches**, 12 → **15 owners**, part big-tech **77 % → 30 %** ; 141 repos génériques retirés (alibaba 76, ByteDance 50, paddlepaddle 13…), 8 repos wedge ajoutés (Sipeed MaixPy, bearpi, AliOS-Things, MNNKit, Dummy-RISC-V-VPU…). Set de calibration live : 17/17.

### Découvert — Gitee s'assèche pour le wedge (constat structurel)

La moisson complète a hard-filtré **2 313/3 660 repos comme stales >2 ans**, dont **1 617 repos OpenHarmony** (openharmony, -sig, -tpc) : l'écosystème OpenAtom a migré hors de Gitee (vers AtomGit/GitCode) et plusieurs vendors hardware publient surtout sur GitHub. Documenté dans `data-sources-and-compliance.md` (priorités candidates relevées) et la ROADMAP (voie de couverture = moisson GitHub avec token + connecteur AtomGit/GitCode). Les « 15/27 orgs à zéro fiche » de l'audit externe étaient des miroirs stales, pas des échecs de fetch.

### Tests

- +9 (désormais **105**) : admission v2 (rejet/immunité contrastifs, règle mot-clé généraliste, rétro-compat sans nouveaux paramètres, `load_anti_domains`, matching mot-clé avec underscore) et override des miroirs stales par seed GitHub.

## [0.14.1] — 2026-07-30

### Corrigé — Alignement à la réalité (constats d'un audit externe indépendant)

Un audit indépendant en lecture seule (Grok, 2026-07-30) a fait remonter des affirmations doc/site ayant dérivé de la réalité. Tous les constats vérifiés corrigés :

- **Comptes de tests périmés** (77/78 → **96**) dans les badges README, README.fr, chiffres clés, commentaire de structure projet, CONTRIBUTING, ROADMAP, ARCHITECTURE.
- **Coût LLM périmé** (~0,005 $/fiche → **~0,01 $ par paire bilingue de repo**) dans README, README.fr, ARCHITECTURE, BUSINESS.
- **Badge landing** « Live · updated this week » (faux : dernier run pipeline 2026-04-27) → remplacé par l'honnête « last pipeline run {date} ».
- **FAQ Pro « Why not GitHub ? »** prétendait que GitHub était un travail futur alors que le connecteur est intégré depuis 0.10.0 → réécrite (« Gitee only, or GitHub too ? »).
- **Wording landing** mis à jour vers Gitee **et** GitHub (lede hero + libellé stat orgs).
- **Artefact de test Phase-0** `output/fiches/test_claude_kernel_liteos_a.md` retiré (ancien fichier FR, invisible à l'outillage, hors state.json).
- **Badges `[MODIFIÉ]` périmés** (ère avril) retirés des 4 fiches stockées (EN + FR).
- **Note d'honnêteté README** : le corpus de démo courant couvre 12 des 27 orgs surveillées.
- **Garde secret CI** : le workflow échoue désormais si `.env` est suivi ou si un motif de clé API apparaît dans les fichiers suivis.
- **ROADMAP** : nouveaux TODO issus de l'audit — rééquilibrage du corpus (biais 77 % Alibaba+ByteDance, 15/27 orgs à zéro fiche), fraîcheur hébergée, risque de drift EN-seul de `rescore.py`, schéma mixte des scores `state.json`.

## [0.14.0] — 2026-07-30

### Ajouté — Pipeline bilingue natif (comble le dernier gap de la roadmap V1)

- **`translator.generate_fiche_pair(repo, readme, score_info)`** — produit la paire de fiches EN + FR depuis une SEULE source de faits : une génération LLM anglaise + une traduction de prose EN→FR (température 0), les deux markdowns composés par le nouvel helper déterministe `_compose_fiche` (extrait de `generate_fiche`, dont l'API mono-langue est inchangée). Fail-safe : si la traduction échoue, la fiche FR garde la prose anglaise sous des libellés français plutôt que de faire échouer le repo.
- **Le pipeline enregistre les deux jeux nativement** (`pipeline._process_llm`) : chaque repo NEW / MODIFIED écrit `output/fiches/<slug>_fiche.md` (EN) **et** `output/fiches_fr/<slug>_fiche.md` (FR) ; le badge `[MODIFIÉ]` est appliqué aux deux. `python src/pipeline.py` seul maintient désormais les deux langues — plus d'étape manuelle séparée.
- **Le bootstrap exige la paire** : `_classify_only` court-circuite vers BOOTSTRAP seulement si les DEUX fiches existent (`_both_fiches_exist`) ; une langue manquante route le repo vers NEEDS_LLM (auto-guérison, pas de drift silencieux).
- **DELETED géré des deux côtés** : `scripts/clean_fiches.py` retire désormais les orphelins de `output/fiches/` et `output/fiches_fr/` ensemble.
- **Tests** : +11 (96 au total) — `generate_fiche_pair` (1 génération + 1 traduction, signal vide, fallback échec-traduction) et un nouveau `tests/test_pipeline.py` (paire écrite au NEW, badge sur les deux au MODIFIED, SKIPPED_EMPTY, dry-run, bootstrap-exige-les-deux, classification auto-guérissante).

### Modifié

- `scripts/build_lang_fiches.py` rétrogradé en outil de migration/backfill one-shot (docstring mise à jour) — plus dans le flux normal.
- Le coût LLM par repo est désormais 1 génération + 1 petite traduction (~2 appels Haiku, toujours ≈ 0,01 $/repo) ; la logique incrémentale (courts-circuits UNCHANGED/SKIPPED_EMPTY) est inchangée.

## [0.13.0] — 2026-07-29

### Ajouté — Livrables V1 publiable

- **`data-sources-and-compliance.md`** — registre de conformité par source (méthode d'accès, statut API-vs-scraping, ce qu'on republie, risques, décision) pour les sources intégrées **et** les sources chinoises candidates (GitCode, GitLink/Trustie, AtomGit, portails vendors), avec une règle d'intégration explicite. Lié depuis `docs/SOURCES.md` et le README.
- **Score de confiance** — tier de qualité de données transparent (High/Medium/Low) par fiche, calculé depuis la profondeur d'enrichissement, la complétude des métadonnées, la récence et un drapeau « non vérifié » (`confidence_tier` dans `src/fiche_schema.py`, partagé avec le dashboard). Exposé en badge de carte ; documenté dans `docs/SCORING.md`. Répartition réelle sur le corpus courant : 108 High / 68 Medium. +7 tests (85 au total).
- **`docs/SCORING.md`** — explique le score de pertinence et le tier de confiance.

### Modifié

- **`ROADMAP.md`** restructurée en **MVP / V1 / V2** avec des TODO explicites.
- **README** — note de statut (MVP fonctionnel), confiance dans « What you get », index des docs mis à jour (registre de conformité, scoring).

## [0.12.0] — 2026-07-29

### Ajouté — Durcissement produit pour publication (docs, cadrage, polissage démo)

- **Suite de docs produit** sous `docs/` : `POSITIONING.md` (proposition de valeur, ICP, cas d'usage, différenciation), `BUSINESS.md` (modèles de revenus, packaging/pricing, go-to-market), `SOURCES.md` (sources de données, méthode d'accès, rate limits, posture IP & conformité), `ARCHITECTURE.md` (modules, flux de données, décisions de design), plus `ROADMAP.md` de haut niveau, `CONTRIBUTING.md`, et un worklog `docs/DECISIONS.md`.
- **Diagramme d'architecture honnête** `docs/assets/pipeline.svg` (cohérent charte, theme-safe, rendu GitHub) utilisé comme hero du README.
- **README recadré produit-first** : proposition de valeur en une ligne, « Who it's for » + cas d'usage, « What you get », index des docs et badges — profondeur technique préservée. README français reflété (badges, proposition de valeur, diagramme, index des docs).

### Modifié

- **Polissage de la démo dashboard** : hero réécrit vers la proposition de valeur (Gitee **et** GitHub, mapping équivalent-occidental) ; ajout d'une ligne de confiance sources & méthode en footer (APIs officielles, métadonnées publiques seulement, liens retour, convention « à confirmer »).
- Commentaires du `.gitignore` traduits en anglais (cohérence défaut-anglais).

## [0.11.0] — 2026-07-29

### Ajouté — Sortie bilingue anglais-first (i18n)

- **L'anglais est désormais la langue par défaut, le français langue 2** — pour la publication GitHub.
- **README et CHANGELOG bilingues** : `README.md` / `CHANGELOG.md` (anglais, défaut) + `README.fr.md` / `CHANGELOG.fr.md` (français), avec un sélecteur de langue en tête de chaque.
- **`translator.py` internationalisé** : `generate_fiche(..., lang="en"|"fr")`. Anglais par défaut. Libellés de champs localisés (`FIELD_LABELS`), catégories de maturité (`MATURITY_LABELS`), libellés de langage de repo (`CODE_LANGUAGE_LABELS`), affichage des noms de domaine (`DOMAIN_DISPLAY`), un `SYSTEM_PROMPT_EN` anglais complet + prompt utilisateur anglais, et typographie des deux-points par langue (EN `Type:`, FR `Type :`). Nouveau `translate_fiche_prose(prose, target_lang)` pour une traduction fidèle inter-langues sans re-fetch.
- **`fiche_schema.py` bilingue** : `Fiche.from_markdown` parse les libellés EN et FR (`_LABEL_ALIASES`), détecte la langue de la fiche (`_detect_lang` → `Fiche.lang`), et `to_markdown` ré-émet les libellés/typographie correspondants — round-trip préservé par langue (utilisé par `rescore.py`).
- **352 fiches bilingues** : 176 anglaises dans `output/fiches/` (défaut) + 176 françaises dans `output/fiches_fr/` (langue 2), générées par le nouveau `scripts/build_lang_fiches.py` (traduit le set français existant vers l'anglais, remappe les champs déterministes, sans re-fetch réseau).
- **Builders de sortie internationalisés** : `build_dashboard.py`, `build_site.py`, `build_newsletter.py` UI traduits en anglais ; leurs parsers de fiches acceptent libellés EN et FR ; clés de matching domaine/statut/langue canonicalisées en anglais (`Embedded`/`Robotics`/`Active`/`Bilingual CN-EN`) pour que graphiques, filtres et couleurs de tags fonctionnent sur les fiches anglaises.
- **Commentaires de code et docstrings** à travers `src/` et `scripts/` traduits en anglais (messages de log runtime et prompts LLM laissés intentionnellement tels quels).

## [0.10.0] — 2026-07-29

### Added — Connecteur GitHub (orgs chinoises absentes de Gitee)

- **`src/github_fetcher.py`** : nouveau connecteur API GitHub REST v3, miroir de l'API publique de `fetcher.py` (`configure`, `list_all_repos_by_owner`, `fetch_repo`, `fetch_readme`). Normalise les repos GitHub sur le schéma exact de Minerva et les tague `_minerva_source="github"`. Gère : rate-limit auto-imposé (55 req/h anonyme, 4500 avec `GITHUB_TOKEN`), respect de `X-RateLimit-Remaining`/`Reset`, retry sur 403/429 (secondary rate limit), pagination auto, filtre des forks purs (`SKIP_FORKS`), et `GitHubPaginationError` pour protéger un owner d'une fausse détection de suppression (miroir de `FetchPaginationError`).
- **Câblage pipeline** (`pipeline.py`) : `_fetch_github_accounts` / `_fetch_github_seeds` mergent les repos GitHub dans le dict `repos` (Gitee prioritaire en cas de collision de slug). Les orgs GitHub entrent dans le set `watched_owners` (bonus scoring) et dans la protection des owners en échec. `_process_llm` route désormais le fetch du README vers le bon hôte selon `_minerva_source`.
- **Fiches source-aware** : `translator.generate_fiche` émet `**GitHub :** https://github.com/{full_name}` pour les repos GitHub (au lieu de `**Gitee :** …`). Les 4 parseurs aval (`fiche_schema`, `build_dashboard`, `build_site`, et `build_newsletter` via le schéma) acceptent les deux libellés. `Fiche.source_label` (computed) garantit le round-trip correct via `rescore.py`.
- **`config/sources.json`** : nouvelles clés `comptes_github` (bouffalolab, sophgo, unitreerobotics, kendryte, allwinner-zh — orgs vérifiées live) et `seeds_github`.
- **Tests** : `tests/test_github_fetcher.py` (13 tests — normalisation, pagination, forks, rate-limit, README, `GitHubPaginationError`). Total suite : **77 tests** (était 64).

### Fixed

- **`src/embedder.py`** : force `USE_TF=0` / `USE_FLAX=0` avant tout import de `transformers`, pour éviter le crash `TypeError: Descriptors cannot be created directly` sur les machines où TensorFlow + un protobuf récent sont installés. Minerva n'utilise que le backend PyTorch. (La CI Ubuntu n'était pas affectée car TF n'y est pas installé.)
- **`src/analyzer.py`** : docstring de `filter_repos` corrigée (`HIGH_SIM_THRESHOLD` = 0.45, était noté 0.55 par erreur).

## [0.9.0] — 2026-04-26

### Added — Scoring hybride keyword + sémantique

- **Logique d'admission hybride** dans `analyzer.filter_repos` : un repo est retenu si **(a)** `best_similarity ≥ 0.45` (semantic-strong) **OU** **(b)** au moins 1 mot-clé discriminant matché (keyword-anchored). Plus le seuil `score_total ≥ min_score` (15) inchangé. Résout le tradeoff identifié en 0.8.0 : récupère les vrais positifs à description sparse (PaddleOCR via "ocr"; LuatOS via "esp32") sans rouvrir la porte au bruit ML research générique. Calibration : 0.55 testé d'abord (86 retenus, trop strict — la majorité des vrais positifs embedded sont en sim 0.40-0.55), puis 0.45 retenu (**371 retenus** sur 3621, signal/bruit acceptable).
- **`analyzer._match_keywords(repo, domains)`** : nouvelle helper privée qui parcourt les `mots_cles` de tous les domaines et matche dans `full_name + description` via `_keyword_in_text` (CJK substring + ASCII frontières case-insensitive, déjà existant). Le langage est exclu pour éviter les faux positifs type "C" qui matche partout.
- **`mots_cles_matches`** est désormais réellement peuplé dans la sortie de `score_repo` (était `[]` en 0.8.0). Utilisable par fiches/dashboard/newsletter pour expliciter le keyword-anchor.
- **Tests pytest** : 3 nouveaux scénarios dans `tests/test_analyzer.py` (`test_filter_repos_drops_no_keyword_low_sim`, `test_filter_repos_keyword_anchor_admits_sparse_desc`, `test_filter_repos_rejects_ml_research_no_specific_keyword`). Schema test mis à jour pour vérifier `mots_cles_matches` non vide quand des mots-clés sont effectivement présents.

### Changed — Resserrement keywords Edge AI

- **`config/domains.json` Edge AI mots_cles** : retiré les termes génériques amorçant le bruit ML research (`ai`, `ml`, `neural`, `deep-learning`, `transformer`, `llm`, `image`, `vision`, `detection`, `recognition`, `segmentation`, `quantization`, `inference`). Conservés les termes deployment-specific (`ncnn`, `tflite`, `onnx`, `tensorrt`, `mnn`, `tnn`, `paddle-lite`, `openvino`, `mindspore lite`, `ocr`, `npu`, `kpu`, `dpu`, `推理`, `神经网络`, `量化`). Ajoutés `rknn`, `snpe`, `coreml`, `paddlelite` (variantes orthographiques fréquentes).
- **Constants analyzer.py** : suppression de `MIN_SIM_WATCHED` / `MIN_SIM_UNWATCHED` (logique désormais hybride). Remplacé par `HIGH_SIM_THRESHOLD = 0.55` unique.

### Cleanup repository
- Suppression des caches Python (`__pycache__/`, `.pytest_cache/`).
- Suppression des logs de dev (gardé les 3 plus récents) et de tous les `probe_*.log`.
- Suppression des scripts one-shot diagnostiques : `probe_gitee_search.py`, `probe_luatos.py`, `probe_new_seeds.py`, `probe_owner_casing.py`, `probe_seeds.py`, `test_claude_api.py`, `test_real_data.py`, `compare_scoring.py`. Leur intention est documentée dans le CHANGELOG, leur sortie n'est plus pertinente après le tightening.
- Suppression de `output/state.json.before_semantic` (snapshot obsolète, plus comparable depuis le passage à l'hybride) et `output/diff_20260425.md`.
- Suppression de `test_batch/` (artefact de la phase 0).
- 923 fiches markdown orphelines supprimées via `clean_fiches.py` (state.json source de vérité après calibration 0.30/0.40 du 0.8.0).

## [0.8.0] — 2026-04-25 (nuit, suite)

### Added — Scoring sémantique par embeddings

- **`src/embedder.py`** : wrapper lazy autour de `sentence-transformers` avec modèle `paraphrase-multilingual-MiniLM-L12-v2` (~118 MB, 50 langues, vecteurs 384-dim L2-normalisés). API : `get_embedder()` (singleton), `embed(text)`, `embed_batch(texts)`, `cosine(a, b)`. Cache disque persistant `output/embeddings_cache.json` indexé par hash SHA-256 du texte source — invalidation automatique si on change de modèle.
- **`config/domains.json` v2** : chaque domaine a désormais une `definition` (paragraphe dense de 80-120 mots décrivant l'intention sémantique). Les `mots_cles` restent disponibles pour fallback offline / autres outils.
- **Refactor `analyzer.score_repo`** : remplacement total du keyword matching par cosine similarity contre les embeddings de définitions de domaines. Schema de sortie préservé (`score_total`, `scores_par_domaine`, `mots_cles_matches=[]`, `domaine_principal`) + nouveau champ `best_similarity` (float [0, 1]).
- **Pré-batch embeddings dans `filter_repos`** : 1 appel `model.encode()` sur tous les repos non hard-filtered au lieu de N appels unitaires (~10× plus rapide à froid).
- **Nouveaux seuils de similarité** :
  - `MIN_SIM_WATCHED = 0.18` (comptes curated)
  - `MIN_SIM_UNWATCHED = 0.25` (autres)
  Remplace l'ancienne garde "≥1 mot-clé matché". Si un repo n'atteint pas le seuil dans aucun domaine → drop.
- **Tests pytest** (`tests/test_analyzer.py` réécrit) : 13 tests dont 8 nouveaux sémantiques (RTOS → Embarqué, OCR/CN → Edge AI, repo hors-sujet → faible sim, multi-domaine, schéma de sortie). Le modèle se charge au premier test (~3 s), bénéficie du cache pour les suivants.

### Changed
- Suppression complète du calcul `POINTS_KEYWORD` / `BONUS_KEYWORD_FULL_NAME` du score. Bonus globaux (stars, forks, recency, CJK, non-mirror, watched_owner) conservés et inchangés.
- `requirements.txt` : ajout de `sentence-transformers>=2.5.0,<3` et `numpy>=1.24.0`.
- `_keyword_in_text` conservé dans analyzer.py pour rétrocompatibilité (utilitaire public, pas dans le scoring).

### Validation et calibration empirique
- Self-test analyzer : Tencent/ncnn (description CN "高性能神经网络...") → Edge AI score 99 sim 0.63 ; openharmony/kernel_liteos_a → Embarqué sim 0.52 ; ByteDance/xgplayer (HTML5 player) → IoT sim 0.28.
- Run pipeline complet sur 3621 repos avec **3 calibrations successives** :
  - **0.18 / 0.25** (initial) → **2250 retenus** (over-inclusif : ML research ByteDance, ComfyUI, modèles diffusion, etc. matchent Edge AI par les mots "transformer/image/llm" sans être de l'inférence edge réelle).
  - **0.30 / 0.40** (mid) → **1336 retenus** (encore trop : la plupart des ML research projects passent encore le seuil watched, qui est trop laxiste pour les big-tech orgs avec 400+ repos).
  - **0.42 / 0.50** (final) → cible ~250-400 repos, signal/bruit acceptable.
- **Coût LLM one-shot** : 1575 fiches générées au premier passage (~$8 LLM Haiku 4.5). Restent sur disque, réutilisables via bootstrap si la calibration future les ramène. Coût réfléchi : architecture testée à grande échelle, validation empirique des seuils.
- 44/44 pytest verts.

### Tradeoff identifié (à creuser)
Le scoring sémantique pur a un angle mort : le modèle d'embedding ne distingue pas
suffisamment "inférence edge" de "ML research / vision cloud" — les deux ont une
similarité élevée avec une définition Edge AI qui mentionne transformers, vision,
quantification. Conséquence : les seuils doivent être très hauts (0.50 unwatched)
pour rejeter le bruit, ce qui peut faire perdre des projets edge legitimes mais
mal décrits (ex. alibaba/Mooncake — pool mémoire pour serving LLM, perdu au seuil 0.50).

**Évolution possible** (si la précision pose problème) : approche hybride keyword+
sémantique. Garde keyword obligatoire (≥1 mot-clé matché) + ranking par sémantique.
Combine la précision du keyword (PaddleOCR via "ocr") avec la nuance sémantique
(score gradué selon la force du match). Reviendrait au système 0.7.x mais avec
score affiné par embedding au lieu de simple comptage. Pas implémenté dans cette
version par fidélité à l'instruction "remplace le keyword matching".

## [0.7.1] — 2026-04-25 (nuit)

### Added
- `translator._clean_readme_paragraphs(readme, max_chars=3500)` : pré-traitement du README avant injection LLM. Supprime les badges shields.io, blocs HTML décoratifs (img/table/center), barres horizontales, sections License/Copyright entières, TOC HTML, et tronque les blocs de code > 300 chars (garde 6 lignes + marqueur). Idempotent.
- 9 tests pytest pour `_clean_readme_paragraphs` (badges, HTML, license, TOC, code blocks, blank lines, max_chars truncation, idempotence, None/empty handling).
- `scripts/probe_gitee_search.py` : 9 variantes testées sur `/search/repositories` (q-param, header-token, /search/repos, sort, language, fork, POST, mot-clé sans tiret, mot-clé chinois, nom de repo connu). Résultat : tous HTTP 200 + 0 résultats. /search/users marche avec le même token (sanity check) → bug serveur Gitee confirmé spécifique à /search/repositories.
- `scripts/probe_luatos.py` : 15 slugs testés. Résultat : `openLuat/LuatOS` existe en accès direct (1836★, Lua engine pour modules cellulaires Air8000/Air8101/Air780E de Hezhou) mais l'org `openLuat` ne s'énumère pas (404 sur /orgs et /users). C'est une org "shadow" — accès repo individuel uniquement.
- `openLuat/LuatOS` ajouté à `seeds_gitee` pour contourner l'absence d'énumération d'org.

### Changed
- `_call_claude_for_fiche` injecte désormais `_clean_readme_paragraphs(readme)` au lieu de `readme[:3500]` brut.
- Mention "(nettoyé : badges/license/TOC/blocs code longs supprimés)" dans le prompt pour que Claude sache que ce qu'il voit a été filtré.
- Commentaire `fetcher.search_repos` mis à jour avec le détail des 9 variantes testées (preuve que c'est bien un bug serveur, pas un format manqué).

### Quality (LuatOS, fiche fraîchement générée avec nouveau prompt + clean_readme)
- Chipsets nommés précisément : Air8000, Air8101, Air780E
- Compteurs concrets : "Lua 5.3, 74 bibliothèques noyau, 55 extensions C, ~1000 APIs"
- Outils nommés : "GitHub Actions pour CI", "LuaTools pour flashage"
- Spécificité chinoise précise : "Hezhou (合宙), fabricant majeur de modules cellulaires LTE-M/NB-IoT"
- Honnêteté : "Aucune conformité à standard chinois spécifique détectée ; pas d'intégration WeChat/Alipay/Baidu Cloud mentionnée"

## [0.7.0] — 2026-04-25 (soir)

### Added
- **Parallélisation des appels LLM** dans `pipeline._generate_fiches` via `ThreadPoolExecutor`. Configurable via `MINERVA_LLM_WORKERS` (défaut 8). Bench observé : 8 fiches en 11 s (vs ~24 s séquentiel) ; bootstrap 140 fiches passe de ~7 min à ~1 min.
- Rate-limiter Gitee thread-safe : `_acquire_rate_permit()` regroupe check + sleep + reserve sous `threading.Lock`. Évite les dépassements de quota en parallèle.
- `Anthropic(max_retries=4)` : retry SDK natif sur 429/5xx avec backoff exponentiel — couvre les rafales contre la limite RPM Haiku 4.5.
- Validation du champ `type` LLM contre `ALLOWED_TYPES` ; fallback automatique sur `infer_type()` si valeur hors liste.
- Site statique multi-pages : `output/index.html` (landing + email capture), `output/pro.html` (3-tier pricing + waitlist), `output/f/<slug>.html × 140` (1 page par fiche, OpenGraph + canonical), `output/sitemap.xml`, `output/robots.txt`. Funnel de monétisation prêt (Buttondown/Substack/MailerLite via env var).

### Changed
- **Prompt Claude réécrit en français** avec ton ingénieur senior, règles anti-marketing strictes (interdiction des mots "puissant", "complet", "moderne"…), définitions précises des 8 types, contraintes de longueur par champ, instruction "à confirmer" plutôt qu'inventer. Système d'org context injecté (`ORG_SPECIFICITE`).
- `CLAUDE_MAX_TOKENS` 500 → 800, `CLAUDE_TEMPERATURE` 0.2 → 0.1 (plus déterministe). Slice README 2000 → 3500 chars.
- `DELAY_BETWEEN_REQUESTS_S` Gitee authentifié 0.5 s → 0.1 s (la cap horaire suffit, libère le parallélisme).
- Test `test_configure_authenticated_sets_higher_rate` adapté à la nouvelle valeur.

### Quality observations (échantillon avant/après)
- `Tencent/ncnn` : avant = "framework optimisé" générique ; après = "écrit en C++, support ARM 32/64-bit, format propriétaire ncnn (conversion via pnnx), Vulkan pour GPU mobile, NEON, OpenMP". Spécificité chinoise honnête : "pas de lien vendor chinois, cible SoC ARM généralistes".
- `paddlepaddle/PaddleOCR` : avant = "suite complète multilingue" ; après = "Python 3.8–3.12, distribution PyPI, runtime PaddleInference, sous-modèle PaddleOCR-VL nommé, équivalents contextualisés (LLaVA/Qwen-VL pour la partie vision-langage)".

## [0.6.0] — 2026-04-25

### Added
- `scripts/clean_fiches.py` : suppression des fiches markdown orphelines (présentes sur disque mais absentes de `state.json`).
- `scripts/probe_owner_casing.py` : vérification de la casse canonique des owners Gitee.
- Garde-fou « ≥1 mot-clé matché » dans `analyzer.filter_repos` : un repo sans aucun mot-clé de domaine est rejeté quel que soit son score (élimine les faux positifs purement portés par les bonus globaux).
- Comparaison case-insensitive des owners (`watched_owners` lowercased) dans `analyzer.score_repo` et `analyzer.filter_repos`.
- Persistance de la clé `scores` dans `state.json` à travers les runs du pipeline (préservation du travail de `rescore.py`).
- Élargissement de `config/domains.json` : Edge AI gagne 11 mots-clés (ocr, vision, ai, ml, deep-learning, transformer, llm, image, detection, recognition, segmentation), Embarqué 6 (cortex, arm, mips, dsp, fpga, soc), IoT 1 (coap).
- Suite de tests pytest (`tests/test_analyzer.py`, `test_fetcher.py`, `test_translator.py`) et workflow GitHub Actions CI (`.github/workflows/ci.yml`).
- LICENSE Apache 2.0.

### Changed
- `_keyword_in_text` utilise désormais `re.ASCII` pour les mots-clés ASCII : un mot anglais comme « OCR » matche au milieu d'un texte chinois (les caractères CJK ne sont plus vus comme des `\w`, donc les frontières de mot fonctionnent).
- README : titre + section Démo en 30 secondes + chiffres exprimés en relatif.
- `config/sources.json` : 6 owners normalisés vers leur casse canonique Gitee (Sipeed, ByteDance, paddlepaddle, JD-opensource, Tencent, TencentOS), ajout de starfive et starfive-tech, retrait d'`openLuat` (404 sur toutes variantes : org disparue de Gitee).

### Removed
- 181 fiches orphelines (`output/fiches/*.md`) : 171 `third_party_*`, 1 `mirrors_*`, 9 archives anciennes — corpus assaini.
- `openLuat` retiré de la liste des comptes surveillés.

### Fixed
- Bug Unicode word-boundary : les mots-clés ASCII ne pouvaient pas matcher au milieu d'un texte CJK (`\b` Unicode-aware). PaddleOCR et autres descriptions chinoises avec acronymes anglais étaient silencieusement filtrés.
- Casse Gitee : 5+ comptes (ByteDance, paddlepaddle, JD-opensource, Tencent, etc.) ne recevaient pas le bonus +8 watched ni le seuil bas (15 vs 20) à cause d'une comparaison string strict-case.

## [0.5.0] — 2026-04-25

### Added
- Domaine **Edge AI** dans `config/domains.json` (frameworks d'inférence mobile, NPU, accélération matérielle IA).
- 8 nouvelles big-tech orgs surveillées (alibaba, bytedance, baidu, paddlepaddle, jd-opensource, tencent, dongshanpi, licheepi).
- `scripts/rescore.py` : recalcul des scores de fiches existantes avec `domains.json` à jour, **sans appel LLM** (gratuit).
- Newsletter HTML + TXT (`scripts/build_newsletter.py`) : version riche pour navigateur + version texte brut envoyable par email.
- Probe scripts pour valider les seeds Gitee candidats.

### Changed
- `state.json` enrichi de la clé `scores` (par repo : score, domaine, edge_ai_score).

## [0.4.0] — 2026-04

### Added
- Dashboard interactif single-file (`scripts/build_dashboard.py` → `output/dashboard.html`) : filtres dynamiques par domaine/type/score, recherche full-text, tri, ouvrable sans serveur (file://).
- Diff incrémental : `output/diff_YYYYMMDD.md` listant NEW/MODIFIED/DELETED par run.
- `state.json` : mémoire persistante entre runs (`last_run`, `repos: {full_name: pushed_at}`).
- Bootstrap LLM-skip : si une fiche existe déjà sur disque pour un repo classé NEW (premier run avec corpus pré-existant), pas d'appel LLM, juste enregistrement de l'état.
- Retry exponentiel sur les pages intermédiaires de pagination Gitee + carry-forward de l'état pour les owners avec fetch incomplet (anti-fausse-suppression).

### Fixed
- Glitch de pagination Gitee qui causait de fausses détections de suppressions (271 false-deletes éliminés).

## [0.3.0] — 2026-04

### Added
- Enrichissement LLM via Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) pour les champs analytiques de la fiche (Problème résolu, Comment ça marche, Spécificité chinoise, Type, Équivalent occidental).
- `seeds_gitee` dans `config/sources.json` : mécanisme manuel de remplacement de la recherche par mot-clés.
- Filtres durs en amont du scoring : `third_party_*` et `mirrors/*` hors comptes surveillés.

### Removed
- Système de traduction par dictionnaire CN-FR (insuffisant pour des fiches techniques de qualité).

### Fixed
- Recherche Gitee par mot-clés (`/search/repositories`) : endpoint cassé côté serveur (renvoie [] systématiquement). Désactivé proprement, remplacé par `seeds_gitee`.
- Chargement `.env` : la convention python-dotenv (override des variables existantes) est appliquée pour éviter qu'une vieille clé persistée au niveau OS masque la valeur du fichier.

## [0.2.0] — 2026-04

### Added
- Pipeline d'orchestration complet (`src/pipeline.py`) : fetcher → analyzer → translator.
- Authentification Gitee via `GITEE_TOKEN` (rate-limit 4500 req/h vs 60 anonyme).
- Logging horodaté dans `output/logs/`.

## [0.1.0] — 2026-04

### Added
- Architecture initiale : `src/fetcher.py`, `src/analyzer.py`, `src/translator.py`.
- 3 domaines initiaux (Embarqué, IoT, Robotique) configurés dans `config/domains.json`.
- Format de fiche markdown standardisé (Type, Domaine, Score, Problème résolu, Comment ça marche, Spécificité chinoise, Équivalent occidental, Maturité, Langue, Gitee).
