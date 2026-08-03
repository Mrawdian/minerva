---
## sophgo/cviruntime
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 59/100
**Problème résolu :** Fournir une bibliothèque runtime et un SDK pour développer des applications ciblant les accélérateurs TPU SOPHGO (séries CV181x, BM1880v2). Permet l'exécution d'inférence sur matériel TPU avec capacités de chargement de modèles, d'exécution et de profilage.
**Comment ça marche :** Bibliothèque runtime C/C++ qui charge et exécute des modèles de réseaux de neurones (via format cvimodel, utilisant la sérialisation FlatBuffers) sur matériel TPU SOPHGO. Dépendances principales : cvibuilder (compilation de modèles), cvikernel (bibliothèque de noyaux TPU), flatbuffers (format de modèle), cnpy (interopérabilité NumPy). Se compile en libcviruntime.so et libcviruntime-static.a. Supporte plusieurs modes d'exécution : SOC (sur appareil), CMODEL (simulation). Inclut l'outil test_cvimodel pour la validation et l'analyse comparative.
**Spécificité chinoise :** SOPHGO est une entreprise chinoise de semi-conducteurs spécialisée dans les accélérateurs IA et la conception de TPU. cviruntime est la pile runtime officielle pour les puces TPU de la série CV et de la série BM de SOPHGO, intégrale à leur écosystème d'inférence IA en périphérie.
**Équivalent occidental :** TensorFlow Lite (Google), NCNN (Tencent), TVM runtime (Apache), ONNX Runtime (Microsoft)
**Maturité :** Expérimental (★ 5, 11 forks, mis à jour 2025-11)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/cviruntime
---
