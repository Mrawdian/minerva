---
## sophgo/sophon-sail
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 54/100
**Problème résolu :** Simplifier le déploiement de modèles d'inférence d'apprentissage profond et de traitement d'images/vidéos sur les accélérateurs TPU SOPHON en fournissant des pipelines unifiés accélérés matériellement pour le décodage, le prétraitement et l'inférence avec liaisons C++ et Python.
**Comment ça marche :** SAIL encapsule les bibliothèques SOPHON de bas niveau (libsophon, bmruntime, bmcv, bmdecoder) et intègre sophon-ffmpeg et sophon-opencv pour le traitement vidéo/image de bout en bout. Offre des API C++ et Python ; C++ cible les performances natives tandis que Python privilégie la facilité du prototypage. Supporte plusieurs modes de déploiement : PCIe (hôte x86 avec carte BM168x), SoC (puces SOPHON basées sur ARM via compilation croisée) et ARM+PCIe. La mémoire des tenseurs est gérée automatiquement. Les dépendances incluent pybind11 (liaisons Python), spdlog (journalisation) et un système de compilation basé sur CMake avec des drapeaux de compilation configurables (BUILD_TYPE, ONLY_RUNTIME, LIBSOPHON_BASIC_PATH, etc.).
**Spécificité chinoise :** SOPHON est une gamme de produits TPU de Bitmain (算能), un grand fabricant chinois de puces IA. SAIL est le cadre de déploiement officiel pour les accélérateurs SOPHON, étroitement intégré à l'écosystème matériel de Bitmain et à la pile d'exécution propriétaire.
**Équivalent occidental :** TensorRT (NVIDIA), OpenVINO (Intel), MediaPipe (Google) — chacun fournit l'inférence accélérée matériellement et le prétraitement, bien que SOPHON-SAIL soit spécifique aux TPU Bitmain.
**Maturité :** Actif (★ 20, 2 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/sophon-sail
---
