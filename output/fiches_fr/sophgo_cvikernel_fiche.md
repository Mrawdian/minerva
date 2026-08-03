---
## sophgo/cvikernel
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 51/100
**Problème résolu :** Générer des instructions TPU pour les unités de traitement tensoriel de SOPHGO sans écrire d'assembleur brut. Fournit une API C/C++ pour construire et émettre programmatiquement des séquences d'instructions TPU, remplaçant le codage assembleur manuel.
**Comment ça marche :** cvikernel est une bibliothèque C/C++ qui traduit les définitions d'instructions de haut niveau en code machine TPU pour les puces SOPHGO (familles cv181x et bm1880v2). Construite avec CMake et Ninja, elle produit une bibliothèque partagée (libbmkernel.so) et une archive statique (libbmkernel-static.a), plus un utilitaire readcmdbuf pour l'inspection du tampon de commandes. La bibliothèque expose des en-têtes (bm_kernel.h, variantes spécifiques aux puces) et sert de couche intermédiaire entre le code applicatif et l'exécution matérielle TPU.
**Spécificité chinoise :** SOPHGO est une entreprise chinoise de semi-conducteurs spécialisée dans les accélérateurs IA et les SoCs informatique en périphérie. cvikernel supporte directement l'architecture d'ensemble d'instructions TPU de SOPHGO (cv181x, bm1880v2), ce qui la rend intégrale à l'écosystème IA embarqué SOPHGO.
**Équivalent occidental :** NVIDIA CUDA (compilation de noyaux GPU), Qualcomm Hexagon SDK (génération d'instructions DSP), génération de code TensorFlow Lite Micro — aucun équivalent direct unique pour l'assemblage d'instructions spécifiques à TPU.
**Maturité :** Expérimental (★ 2, 8 forks, mis à jour 2024-10)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/cvikernel
---
