---
## sophgo/tpu-mlir
**Type :** Tool
**Domaine :** Embarqué
**Score de pertinence :** 78/100
**Problème résolu :** Compiler des modèles de réseaux de neurones pré-entraînés (PyTorch, ONNX, TFLite, Caffe, HuggingFace) en binaires optimisés (bmodel) exécutables sur les TPU Sophgo, avec support complet de la quantification (INT8, BF16, F16) et des LLM.
**Comment ça marche :** Pipeline MLIR à deux étages : front-end d'import (model_transform.py) convertit les formats standards en dialecte MLIR Top, puis back-end (model_deploy.py) abaisse vers dialecte Tpu avec optimisations (layer-group memory planning, pattern rewrites, quantification symétrique/asymmétrique, AWQ/GPTQ/AutoRound). Outils complémentaires : model_runner (inférence), model_tool (inspection), simulator, visualizer. Déploiement via Docker (sophgo/tpuc_dev) avec Python ≥3.10 sur Ubuntu 22.04.
**Spécificité chinoise :** Sophgo est un fabless chinois spécialisé dans les SoC TPU ; ce compilateur cible directement ses architectures TPU (bm1684x cité). Intégration native de modèles HuggingFace populaires en Chine (Qwen, MiniCPM-V). Documentation bilingue CN-EN et communauté active sur Gitee.
**Équivalent occidental :** TVM (Apache), ONNX Runtime (Microsoft), TensorFlow Lite Converter (Google), PyTorch Export (Meta) — mais aucun n'offre la même intégration compilateur MLIR + quantification + ciblage TPU propriétaire.
**Maturité :** Stable (★ 954, 226 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/tpu-mlir
---
