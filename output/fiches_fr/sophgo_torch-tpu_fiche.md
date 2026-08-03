---
## sophgo/torch-tpu
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 56/100
**Problème résolu :** Activer l'exécution de modèles PyTorch sur les dispositifs TPU Sophgo (SG2260, TPU1686) avec support des frameworks d'entraînement distribué (DeepSpeed, Megatron) et des grands modèles de langage, comblant le fossé entre l'écosystème CPU/GPU de PyTorch et le matériel TPU propriétaire de Sophgo.
**Comment ça marche :** Torch-TPU est une extension C++ PyTorch qui fournit les modes d'exécution JIT et Eager pour l'inférence et l'entraînement sur TPU Sophgo. Il s'intègre avec tpuv7-runtime (runtime TPU de Sophgo), firmware_core (compilation de noyau pour SG2260/TPU1686) et tpu-train (support d'entraînement distribué). Le projet utilise Docker pour l'isolation de l'environnement, CMake pour les compilations, et supporte DeepSpeed Zero Stage 1/2 avec déchargement CPU et parallélisme tensoriel Megatron pour des modèles comme Qwen2.
**Spécificité chinoise :** Sophgo est une entreprise chinoise de semi-conducteurs spécialisée dans les accélérateurs IA et la conception de TPU. Torch-TPU cible directement les dispositifs TPU propriétaires de Sophgo (SG2260, TPU1686) et s'intègre avec la pile runtime et firmware fermée de Sophgo, ce qui en fait une infrastructure essentielle pour déployer les charges de travail PyTorch sur le matériel Sophgo dans l'écosystème IA chinois.
**Équivalent occidental :** PyTorch XPU (Intel), backends PyTorch CUDA/ROCm, TensorRT (NVIDIA), OpenVINO (Intel) — bien qu'aucun ne cible directement les TPU Sophgo ; l'analogue fonctionnel le plus proche est la couche d'abstraction de dispositif de PyTorch pour les accélérateurs personnalisés.
**Maturité :** Expérimental (★ 12, mis à jour 2026-01)
**Langue :** Anglais
**GitHub :** https://github.com/sophgo/torch-tpu
---
