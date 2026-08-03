---
## EspressifSystems/esp-skainet
**Type :** Framework
**Domaine :** Embarqué
**Score de pertinence :** 67/100
**Problème résolu :** Fournir une solution complète de reconnaissance de mots-clés de réveil et de commandes vocales offline sur microcontrôleurs ESP32 avec faible consommation mémoire et latence réduite.
**Comment ça marche :** ESP-Skainet intègre deux moteurs de traitement vocal : WakeNet pour la détection de mots-clés de réveil (Alexa, 天猫精灵, etc.) et MultiNet pour la reconnaissance de jusqu'à 200 commandes vocales sans reconnexion réseau. Le pipeline traite les flux audio provenant de microphones ou fichiers stockés en flash/SD via un module Audio Front-End (AFE) effectuant le prétraitement du signal. L'architecture exploite l'ESP32-S3 avec sa PSRAM octal SPI haute vitesse pour déployer les modèles d'inférence optimisés.
**Spécificité chinoise :** Intégration native de mots-clés chinois (天猫精灵 d'Alibaba, 小爱同学 de Xiaomi) et support des commandes vocales en mandarin. Développé par Espressif Systems, fabricant chinois de SoC WiFi/BLE dominant le marché IoT asiatique.
**Équivalent occidental :** Amazon Alexa Voice Service SDK, Google Assistant SDK (nécessitent connexion cloud) ; PocketSphinx (reconnaissance vocale offline mais moins optimisé pour microcontrôleurs)
**Maturité :** Actif (★ 24, 10 forks, mis à jour 2026-02)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/EspressifSystems/esp-skainet
---
