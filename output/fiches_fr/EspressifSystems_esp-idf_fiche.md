---
## EspressifSystems/esp-idf [MODIFIÉ]
**Type :** Framework
**Domaine :** Embarqué
**Score de pertinence :** 94/100
**Problème résolu :** Fournir un framework de développement unifié et un système de compilation pour les SoCs Espressif ESP32 et ESP32-S2, incluant le bootloader, la génération de table de partitions et l'abstraction matérielle sur les plateformes hôtes Windows, Linux et macOS.
**Comment ça marche :** ESP-IDF est un framework de compilation basé sur CMake écrit en C/C++ avec des outils Python (CLI idf.py). Il inclut FreeRTOS comme noyau RTOS, les pilotes HAL pour les périphériques (GPIO, SPI, I2C, UART, WiFi, BLE), la gestion de la table de partitions et le support des mises à jour OTA. Le framework utilise les sous-modules git pour gérer les dépendances et fournit menuconfig pour la configuration du projet. Les cibles supportées incluent ESP32, ESP32-S2 et les anciens ESP8266/ESP8285 via un SDK RTOS séparé.
**Spécificité chinoise :** Espressif Systems (乐鑫, Shanghai) est le fabricant des SoCs ESP32/ESP32-S2 et maintient ce framework officiel. Le référentiel Gitee est un miroir officiel synchronisé quotidiennement depuis GitHub ; aucune norme ou intégration spécifique à la Chine n'est évidente au-delà de l'origine du fournisseur.
**Équivalent occidental :** Arduino IDE (pour les cartes ESP32), Zephyr RTOS (Linux Foundation), PlatformIO (développement embarqué multiplateforme)
**Maturité :** Stable (★ 877, 390 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/EspressifSystems/esp-idf
---
