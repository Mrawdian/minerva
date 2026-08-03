---
## alibaba/AliOS-Things
**Type :** RTOS
**Domaine :** IoT
**Score de pertinence :** 75/100
**Problème résolu :** Fournir un système d'exploitation temps réel scalable et modulaire spécifiquement conçu pour les appareils IoT avec ressources limitées, supportant plusieurs architectures CPU et intégrant nativement la connectivité réseau et la sécurité.
**Comment ça marche :** AliOS Things utilise une architecture en couches composée d'un noyau RTOS Rhino, d'une couche HAL abstraisant le matériel (WiFi, Bluetooth, I2C, SPI, UART, Flash), d'une pile réseau légère (LwIP, BLE, LoRaWAN) et d'une couche sécurité (TLS, ID2, TEE). Les composants sont gérés via configuration YAML permettant une sélection modulaire des fonctionnalités, avec support de VFS unifié pour les pilotes et APIs standardisées pour les applications.
**Spécificité chinoise :** Intégration native avec l'écosystème Alibaba Cloud (LinkSDK, services de diagnostic et d'amorçage), support des standards chinois via les composants LoRaWAN et des solutions de configuration WiFi adaptées au marché local, avec documentation et exemples orientés vers les plateformes matérielles Alibaba (HaaS100, HaaS EDU K1, HaaS200).
**Équivalent occidental :** FreeRTOS, Zephyr Project, RIOT OS
**Maturité :** Expérimental (★ 1, 2 forks, mis à jour 2024-11)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/alibaba/AliOS-Things
---
