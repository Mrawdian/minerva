---
## sophgo/fsbl
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 57/100
**Problème résolu :** Fournir un chargeur d'amorçage de première étape (FSBL) pour les SoC de la série CV18xx qui agit comme étape BL2 d'ARM Trusted Firmware (ATF), permettant l'amorçage sécurisé et le chargement du micrologiciel sur les processeurs de Sophgo.
**Comment ça marche :** FSBL est un chargeur d'amorçage écrit en C/assembleur qui initialise le matériel du SoC CV18xx, configure la mémoire et les horloges, et transfère le contrôle à l'étape d'amorçage suivante (généralement ATF BL31 ou le noyau du système d'exploitation principal). Il fonctionne au niveau de privilège le plus bas avant l'exécution de tout noyau de système d'exploitation. Le projet s'intègre aux pilotes spécifiques au SoC de Sophgo et aux définitions de disposition de la mémoire. Les détails des dépendances et du système de compilation doivent être confirmés à partir de la structure du référentiel.
**Spécificité chinoise :** Sophgo est une entreprise chinoise de semi-conducteurs spécialisée dans les accélérateurs d'IA et les SoC ; la série CV18xx est leur ligne de processeurs propriétaire. Ce chargeur d'amorçage est une infrastructure essentielle pour l'écosystème de produits d'IA embarqués et périphériques de Sophgo.
**Équivalent occidental :** ARM Trusted Firmware (ATF) étape BL2, U-Boot SPL (Das U-Boot), miniloader Rockchip
**Maturité :** Actif (★ 11, 24 forks, mis à jour 2026-06)
**Langue :** Anglais
**GitHub :** https://github.com/sophgo/fsbl
---
