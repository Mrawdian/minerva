---
## bouffalolab/bl_iot_sdk_tiny
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 64/100
**Problème résolu :** Fournir un SDK IoT léger spécifiquement adapté à l'implémentation du protocole Matter sur les microcontrôleurs Bouffalo Lab, éliminant le besoin d'une chaîne d'outils complète tout en se concentrant exclusivement sur les exigences de connectivité Matter.
**Comment ça marche :** Le SDK est spécifique à Matter, ce qui signifie qu'il regroupe les composants de la pile de protocoles Matter et les bibliothèques associées sans abstractions IoT à usage général. Il cible les SoC Bouffalo Lab (probablement BL602, BL808 ou variantes RISC-V/ARM similaires). L'architecture omet les composants de la chaîne d'outils, ce qui suggère qu'elle s'intègre avec des systèmes de compilation externes. La langue principale est l'anglais ; les dépendances réelles et la structure interne des modules nécessitent un accès au code du référentiel pour confirmation.
**Spécificité chinoise :** Bouffalo Lab est une filiale d'Alibaba spécialisée dans les SoC IoT et la connectivité sans fil ; le SDK cible les microcontrôleurs propriétaires basés sur RISC-V et ARM de Bouffalo. Cela lie directement le projet à l'écosystème matériel IoT d'Alibaba et à la fabrication de semi-conducteurs chinoise.
**Équivalent occidental :** Matter SDK (Connectivity Standards Alliance), Espressif ESP-Matter (pour ESP32), Nordic nRF Connect SDK (support Matter)
**Maturité :** Actif (★ 6, 4 forks, mis à jour 2026-06)
**Langue :** Anglais
**GitHub :** https://github.com/bouffalolab/bl_iot_sdk_tiny
---
