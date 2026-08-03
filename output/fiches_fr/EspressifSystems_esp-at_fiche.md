---
## EspressifSystems/esp-at [MODIFIÉ]
**Type :** Framework
**Domaine :** IoT
**Score de pertinence :** 84/100
**Problème résolu :** Fournir une interface de commande AT standardisée pour les SoCs Espressif ESP32/ESP8266 afin de permettre aux microcontrôleurs hôtes de contrôler la connectivité sans fil (WiFi, Bluetooth, cellulaire) sans implémenter des piles réseau complètes, réduisant ainsi la complexité du micrologiciel sur les plates-formes à ressources limitées.
**Comment ça marche :** ESP-AT est un framework de micrologiciel construit sur ESP-IDF et ESP8266-RTOS-SDK qui s'exécute sur les SoCs Espressif (ESP32, ESP32-C2, ESP32-C3, ESP32-C5, ESP32-C6, ESP32-C61, ESP32-S2) et expose des ensembles de commandes AT pour les opérations WiFi, Bluetooth et TCP/IP. L'hôte communique via UART ou SPI en utilisant des commandes AT basées sur du texte et reçoit des réponses structurées. Le framework inclut des gestionnaires de commandes intégrés, des commandes AT définies par l'utilisateur personnalisables et des binaires de micrologiciel précompilés pour chaque variante de puce. Le développement cible Windows, Linux et macOS.
**Spécificité chinoise :** Espressif Systems (Shanghai) est le fabricant des SoCs ESP32/ESP8266 et maintient ce projet en tant que projet officiel ; le référentiel Gitee est un miroir domestique officiel synchronisé depuis GitHub. Aucune intégration avec les plates-formes cloud chinoises (Baidu, Alibaba, Tencent) ou les API WeChat/Alipay n'est évidente dans le contexte fourni.
**Équivalent occidental :** Bibliothèque Arduino AT (pour les cartes Arduino), framework de commandes AT Quectel (pour les modules cellulaires), ensembles de commandes AT u-blox (pour les modules GNSS/cellulaires)
**Maturité :** Actif (★ 50, 4 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/EspressifSystems/esp-at
---
