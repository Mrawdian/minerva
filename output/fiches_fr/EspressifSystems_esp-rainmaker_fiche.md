---
## EspressifSystems/esp-rainmaker [MODIFIÉ]
**Type :** Framework
**Domaine :** IoT / Edge AI
**Score de pertinence :** 75/100
**Problème résolu :** Permet le contrôle à distance et la surveillance des appareils IoT basés sur ESP32 sans configuration manuelle du cloud. Fournit un agent firmware qui gère automatiquement la revendication d'appareil, la connectivité cloud et le rendu dynamique de l'interface utilisateur sur les clients mobiles.
**Comment ça marche :** ESP RainMaker se compose d'un agent firmware (ce référentiel) écrit en C pour ESP-IDF, un service de revendication pour l'approvisionnement en identifiants, et un backend cloud. L'agent s'exécute sur les SoCs de la série ESP32 (ESP32, ESP32-S2, ESP32-S3, ESP32-C2, ESP32-C3, ESP32-C6, ESP32-H2, ESP32-C5) et communique avec le cloud RainMaker via MQTT ou HTTP. Les développeurs définissent des appareils et des paramètres personnalisés dans le firmware ; le cloud et les applications mobiles (Android/iOS) restituent dynamiquement l'interface utilisateur en fonction des métadonnées de l'appareil. Nécessite ESP-IDF 4.1 ou version ultérieure.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par EspressifSystems ; aucune spécificité chinoise particulière au-delà de l'auteur. Espressif Systems (乐鑫, Shanghai) est le fabricant des SoCs ESP32 et maintient ce référentiel officiel.
**Équivalent occidental :** Amazon FreeRTOS avec AWS IoT Core, Google Cloud IoT Core avec des bibliothèques clientes intégrées, kits de développement Azure IoT Hub
**Maturité :** Actif (★ 11, mis à jour 2026-07)
**Langue :** Anglais
**Gitee :** https://gitee.com/EspressifSystems/esp-rainmaker
---
