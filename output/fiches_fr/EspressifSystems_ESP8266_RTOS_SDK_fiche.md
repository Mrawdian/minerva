---
## EspressifSystems/ESP8266_RTOS_SDK [MODIFIÉ]
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 100/100
**Problème résolu :** Fournit un SDK basé sur RTOS pour le microcontrôleur ESP8266 avec FreeRTOS, lwIP et les pilotes Wi-Fi intégrés. Répond au besoin d'un environnement de développement complet pour construire des applications embarquées en réseau sur l'ESP8266 sans dépendre uniquement du SDK non-OS.
**Comment ça marche :** SDK basé sur C construit sur le noyau FreeRTOS avec pile TCP/IP lwIP intégrée, mbedTLS pour TLS/SSL et bibliothèques Wi-Fi propriétaires (libmain). La compilation utilise la chaîne d'outils Xtensa LX106 GCC (v8.4.0 ou v4.8.5 selon la version du SDK). Supporte la configuration de compilation pilotée par menuconfig. Les composants principaux incluent le système de fichiers SPIFFS, cJSON, libcoap et la bibliothèque WebSocket noPoll. Cible le SoC ESP8266 basé sur Xtensa monocœur.
**Spécificité chinoise :** Espressif Systems (乐鑫, Shanghai) est le fabricant des SoC ESP8266 et ESP32 ; il s'agit du SDK officiel maintenu par le fournisseur. Aucune conformité particulière aux normes chinoises ou intégration à l'écosystème domestique au-delà du rôle du fournisseur sur le marché mondial des puces IoT.
**Équivalent occidental :** ESP-IDF (framework plus récent d'Espressif pour ESP32), FreeRTOS avec pile lwIP sur d'autres microcontrôleurs, noyau Arduino pour ESP8266
**Maturité :** Actif (★ 101, 66 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/EspressifSystems/ESP8266_RTOS_SDK
---
