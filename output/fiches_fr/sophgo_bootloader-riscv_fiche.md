---
## sophgo/bootloader-riscv [MODIFIÉ]
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 55/100
**Problème résolu :** Amorcer les systèmes RISC-V en fournissant une implémentation de bootloader pour les SoCs basés sur RISC-V. Active le chargement du firmware et l'initialisation du système sur les architectures RISC-V où les bootloaders des fournisseurs peuvent être propriétaires ou indisponibles.
**Comment ça marche :** Un bootloader RISC-V écrit en C et en assembleur, responsable de l'initialisation matérielle en phase précoce, de la configuration de la mémoire et du transfert vers le noyau ou le bootloader de l'étape suivante. Cible l'architecture du jeu d'instructions RISC-V ; prend probablement en charge les SoCs RISC-V courants. Les dépendances et les cibles matérielles spécifiques doivent être confirmées par inspection du code source.
**Spécificité chinoise :** Hébergé par SOPHGO (une entreprise chinoise de semi-conducteurs spécialisée dans les SoCs d'IA et d'informatique en périphérie avec des cœurs RISC-V). Les processeurs BM1684, BM1688 et autres de SOPHGO utilisent des cœurs RISC-V ou compatibles RISC-V, ce qui rend ce bootloader pertinent pour leur écosystème de produits.
**Équivalent occidental :** U-Boot (port RISC-V), OpenSBI (Interface binaire superviseur RISC-V), Coreboot (support RISC-V)
**Maturité :** Actif (★ 26, 44 forks, mis à jour 2026-07)
**Langue :** Anglais
**GitHub :** https://github.com/sophgo/bootloader-riscv
---
