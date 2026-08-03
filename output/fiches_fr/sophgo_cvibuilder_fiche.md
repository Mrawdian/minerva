---
## sophgo/cvibuilder
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 43/100
**Problème résolu :** Définir et analyser le format binaire des fichiers CVIMODEL utilisés par les accélérateurs TPU CV18xx de Sophgo, permettant aux outils et frameworks tiers de sérialiser et désérialiser les modèles de réseaux de neurones pour le déploiement sur ces SoCs.
**Comment ça marche :** La bibliothèque fournit des définitions de structures de données et des routines de sérialisation/désérialisation pour CVIMODEL, le format propriétaire de conteneur de modèles pour les accélérateurs d'inférence TPU CV18xx de Sophgo. Écrite en C/C++, elle abstrait la disposition binaire des réseaux de neurones compilés, permettant l'intégration avec les pipelines de conversion de modèles et les moteurs d'inférence d'exécution. Le projet cible la famille de SoC CV18xx de Sophgo (CV1835, CV1838, etc.) et sert de pont entre les frameworks d'entraînement et l'exécution TPU sur appareil.
**Spécificité chinoise :** Sophgo est une entreprise chinoise de semi-conducteurs spécialisée dans les SoCs d'IA embarquée et de traitement vidéo ; CV18xx est leur ligne de processeurs propriétaires équipés de TPU. Le format CVIMODEL est la norme interne de Sophgo pour le déploiement de réseaux de neurones sur leur écosystème matériel.
**Équivalent occidental :** Schéma TensorFlow Lite (Google), format de modèle ONNX Runtime (Microsoft/Facebook), représentation intermédiaire du compilateur TVM — tous fournissent la sérialisation de modèles pour l'inférence embarquée, mais CVIMODEL est spécifique à l'ISA TPU de Sophgo.
**Maturité :** Expérimental (★ 2, 7 forks, mis à jour 2024-10)
**Langue :** Anglais
**GitHub :** https://github.com/sophgo/cvibuilder
---
