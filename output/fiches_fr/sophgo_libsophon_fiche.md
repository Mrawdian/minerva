---
## sophgo/libsophon
**Type :** Driver
**Domaine :** Embarqué
**Score de pertinence :** 71/100
**Problème résolu :** Fournir les pilotes du noyau Linux et les bibliothèques d'exécution pour les puces accélératrices IA Sophgo (modules TPU, VPU, JPU, VPP), permettant aux systèmes hôtes de décharger les charges de travail d'inférence et de traitement multimédia vers ces processeurs spécialisés.
**Comment ça marche :** libsophon comprend les pilotes du noyau Linux (module sg_x86_pcie_device pour PCIe), la bibliothèque d'exécution bmlib, le runtime TPU avec support de quantification statique (int8), la bibliothèque de traitement multimédia bmcv, et l'outil de surveillance bm-smi. Écrit en C/C++, construit avec CMake/Ninja, supporte les architectures x86_64 PCIe, ARM64 (aarch64) et LoongArch64 via des chaînes d'outils de compilation croisée. Le chargement du micrologiciel via /lib/firmware et l'insertion du module noyau (insmod) sont requis pour le fonctionnement.
**Spécificité chinoise :** Sophgo est un fournisseur chinois de puces IA ; libsophon est la pile officielle de pilotes et d'exécution pour leurs processeurs BM1684x et apparentés. Aucune intégration avec les plateformes cloud chinoises ou les normes documentées dans le README.
**Équivalent occidental :** NVIDIA CUDA (propriétaire, x86/ARM), Intel OpenVINO (runtime d'inférence), Qualcomm Hexagon SDK (pilotes DSP/NPU)
**Maturité :** Actif (★ 26, 16 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/libsophon
---
