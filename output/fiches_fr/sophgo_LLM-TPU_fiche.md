---
## sophgo/LLM-TPU [MODIFIÉ]
**Type :** Tool
**Domaine :** Embarqué
**Score de pertinence :** 67/100
**Problème résolu :** Déployer des modèles de langage volumineux (LLM) et des modèles vision-langage (VLM) avec quantification et parallélisme multi-puces sur les accélérateurs TPU SOPHGO BM1684X/BM1688, en convertissant directement les poids HuggingFace au format bmodel sans optimisation manuelle.
**Comment ça marche :** Le projet fournit llm_convert.py, un compilateur basé sur Python qui ingère des modèles quantifiés (AWQ/GPTQ) depuis HuggingFace et génère des binaires bmodel pour les TPU SOPHGO via la chaîne d'outils TPU-MLIR. L'inférence est exécutée via des liaisons de runtime C++ et Python qui gèrent le cache KV, la compilation de forme dynamique et la distribution multi-puces. Des bmodels pré-compilés sont hébergés pour un déploiement rapide ; les modèles supportés incluent les familles Qwen, Llama, DeepSeek, InternVL, MiniCPM et Phi avec support multimodal (texte, image, vidéo, audio).
**Spécificité chinoise :** SOPHGO est un fournisseur de semi-conducteurs chinois spécialisé dans les accélérateurs IA ; les BM1684X et BM1688 sont des puces TPU propriétaires SOPHGO. Le projet est officiellement maintenu par SOPHGO et cible leur gamme de produits TPU domestiques, représentant un chemin de déploiement clé pour l'IA générative sur des accélérateurs conçus en Chine.
**Équivalent occidental :** TensorRT (NVIDIA), OpenVINO (Intel), ONNX Runtime (Microsoft/Linux Foundation) — bien que ces derniers ciblent des écosystèmes d'accélérateurs différents ; aucun équivalent occidental direct pour le déploiement TPU SOPHGO n'existe.
**Maturité :** Actif (★ 297, 49 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/LLM-TPU
---
