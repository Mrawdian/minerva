---
## bouffalolab/bl_iot_sdk
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 80/100
**Problème résolu :** Fournir un SDK unifié pour les chipsets combo RISC-V Wi-Fi/BLE (BL602) et Zigbee/BLE (BL70X) de Bouffalo Lab, remplaçant la documentation fragmentée du fournisseur et permettant le développement rapide de dispositifs IoT sur ces SoC.
**Comment ça marche :** Le SDK inclut les pilotes HAL, l'intégration du noyau FreeRTOS, les piles de protocoles Wi-Fi/BLE/Zigbee et les pilotes périphériques (UART, SPI, GPIO, ADC, PWM) pour les cœurs RISC-V BL602 et BL70X. Écrit en C avec documentation bilingue (chinois/anglais). Dépend de la chaîne d'outils GCC RISC-V et de FreeRTOS. Supporte le développement d'applications bare-metal et basées sur RTOS avec des projets d'exemple pour les cas d'usage IoT courants.
**Spécificité chinoise :** Bouffalo Lab est un fournisseur de semi-conducteurs chinois spécialisé dans les SoC IoT RISC-V à faible consommation. Les BL602 et BL70X sont des conceptions propriétaires de Bouffalo ; ce SDK est l'environnement de développement officiel pour ces chipsets au sein de l'écosystème IoT chinois.
**Équivalent occidental :** Espressif ESP-IDF (ESP32), Nordic nRF5 SDK, Silicon Labs Gecko SDK
**Maturité :** Actif (★ 292, 185 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/bouffalolab/bl_iot_sdk
---
