---
## bouffalolab/bouffalo_drivers
**Type :** Driver
**Domaine :** Embarqué
**Score de pertinence :** 76/100
**Problème résolu :** Fournir une couche d'abstraction matérielle (HAL), une gestion des paramètres RF et des pilotes au niveau du SoC pour les microcontrôleurs et SoCs sans fil de Bouffalo Lab, permettant aux développeurs de firmware d'accéder aux interfaces périphériques (GPIO, UART, SPI, I2C, ADC, RF) sans manipulation directe des registres.
**Comment ça marche :** Le projet regroupe trois composants de pilote : lhal (abstraction matérielle bas niveau), rfparam (configuration des paramètres de radiofréquence) et pilotes soc (pilotes périphériques système sur puce). Écrit en C, il cible les SoCs basés RISC-V de Bouffalo Lab BL602, BL604 et apparentés. Les dépendances et l'organisation exacte des modules ne sont pas documentées dans les README accessibles ; l'intégration se fait généralement au stade de la compilation du firmware via CMake ou Make.
**Spécificité chinoise :** Bouffalo Lab est un fabricant de semi-conducteurs chinois spécialisé dans les SoCs sans fil basse consommation (BLE, WiFi, Zigbee). Ce dépôt de pilotes est la distribution HAL officielle pour leur écosystème de puces, supportant directement leur gamme de produits commerciaux.
**Équivalent occidental :** STMicroelectronics STM32Cube HAL, Nordic nRF5 SDK, couche HAL Espressif ESP-IDF
**Maturité :** Actif (★ 6, 2 forks, mis à jour 2026-07)
**Langue :** Anglais
**GitHub :** https://github.com/bouffalolab/bouffalo_drivers
---
