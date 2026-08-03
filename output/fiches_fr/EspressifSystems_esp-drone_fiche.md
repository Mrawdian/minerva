---
## EspressifSystems/esp-drone [MODIFIÉ]
**Type :** Application
**Domaine :** Edge AI
**Score de pertinence :** 73/100
**Problème résolu :** Fournir une pile de firmware de quadricoptère contrôlée par Wi-Fi pour les microcontrôleurs ESP32/ESP32-S2/ESP32-S3, permettant les modes de stabilisation de vol et de maintien de position sans plateformes de drones propriétaires. Porté depuis Crazyflie pour réduire les frictions de développement pour les projets de drones éducatifs et amateurs.
**Comment ça marche :** Logique de contrôle de vol principal (stabilisation, maintien de hauteur, maintien de position) portée depuis le firmware Crazyflie (GPL 3.0) ; s'exécute sur ESP-IDF v5.0 (framework basé sur FreeRTOS d'Espressif). Les cibles matérielles sont les SoCs ESP32, ESP32-S2, ESP32-S3 avec radio Wi-Fi ; contrôle via des applications mobiles (iOS/Android) ou le client Python cfclient sur Wi-Fi, ou protocole ESP-NOW depuis le joystick ESP-BOX3. Inclut la bibliothèque DSP (esp32-lin) pour la fusion de capteurs et le contrôle moteur.
**Spécificité chinoise :** Développé et maintenu par Espressif Systems (Shanghai), le fabricant des SoCs ESP32 ; miroir officiel Gitee synchronisé depuis GitHub. Exploite l'écosystème ESP-IDF d'Espressif et la plateforme matérielle comme seule architecture cible.
**Équivalent occidental :** Firmware Crazyflie (Bitcraze), ArduCopter (ArduPilot), autopilote PX4
**Maturité :** Actif (★ 64, 21 forks, mis à jour 2026-06)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/EspressifSystems/esp-drone
---
