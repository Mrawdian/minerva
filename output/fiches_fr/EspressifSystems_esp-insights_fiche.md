---
## EspressifSystems/esp-insights [MODIFIÉ]
**Type :** Framework
**Domaine :** Edge AI
**Score de pertinence :** 77/100
**Problème résolu :** Capturer et transmettre à distance les diagnostics des appareils (journaux d'erreurs/avertissements, plantages, métriques, raisons de réinitialisation) depuis les appareils ESP32/ESP8266 déployés sur le terrain vers un tableau de bord cloud, permettant aux développeurs de diagnostiquer les problèmes qui ne surviennent que dans des environnements de déploiement spécifiques sans accès physique.
**Comment ça marche :** L'agent Insights est un composant firmware (C/C++) intégré à ESP-IDF qui s'accroche au système de journalisation (macros ESP_LOGE, ESP_LOGW), capture les coredumps, les métriques de heap et les événements personnalisés via les appels ESP_DIAG_EVENT, puis télécharge ces données via HTTPS vers le backend cloud ESP Insights. La configuration est gérée via menuconfig (Component config → ESP Insights) et nécessite une clé d'authentification intégrée au firmware. Le cloud traite et visualise les données collectées dans un tableau de bord web affichant les journaux d'erreurs, les avertissements, les raisons de réinitialisation, les traces de pile, les métriques dans le temps et les analyses de groupe.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par EspressifSystems ; aucune spécificité chinoise particulière au-delà de l'auteur. Espressif Systems (乐鑫, Shanghai) est le fabricant des SoCs ESP8266 et ESP32, et ce projet est leur framework officiel de diagnostics à distance pour leur écosystème de puces.
**Équivalent occidental :** AWS IoT Device Defender (AWS), diagnostics Azure IoT Hub (Microsoft), journalisation Google Cloud IoT Core, Memfault (SaaS indépendant pour diagnostics embarqués)
**Maturité :** Actif (★ 2, mis à jour 2026-07)
**Langue :** Anglais
**Gitee :** https://gitee.com/EspressifSystems/esp-insights
---
