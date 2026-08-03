---
## sophgo/zsbl
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 52/100
**Problème résolu :** Fournir un chargeur d'amorçage RISC-V pour les SoC SOPHGO qui initialise le processeur, charge le chargeur d'amorçage de l'étape suivante ou le noyau, et gère la configuration matérielle précoce avant que le système d'exploitation principal prenne le contrôle.
**Comment ça marche :** ZSBL (Zero Stage BootLoader) est un chargeur d'amorçage minimal de première étape écrit pour les processeurs RISC-V SOPHGO. Il effectue l'initialisation du processeur, la configuration de la mémoire et le transfert vers un chargeur d'amorçage secondaire ou une image de noyau. Le projet est écrit en C et en assembleur, ciblant la gamme de SoC RISC-V de SOPHGO. Les dépendances et les séquences d'initialisation matérielle spécifiques doivent être confirmées à partir du code source.
**Spécificité chinoise :** SOPHGO est une entreprise chinoise de semi-conducteurs sans usine spécialisée dans les accélérateurs d'IA et les SoC RISC-V ; ce chargeur d'amorçage fait partie de leur pile logicielle open-source pour leur famille de processeurs RISC-V propriétaires.
**Équivalent occidental :** U-Boot (Denx), coreboot (Linux Foundation), OpenSBI (RISC-V Foundation)
**Maturité :** Actif (★ 33, 35 forks, mis à jour 2026-07)
**Langue :** Anglais
**GitHub :** https://github.com/sophgo/zsbl
---
