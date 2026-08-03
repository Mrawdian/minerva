---
## bouffalolab/bl_iot_sdk-components
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 70/100
**Problème résolu :** Fournir des composants modulaires et réutilisables pour les applications IoT construites sur la famille de SoC BL602/BL604, en découplant la logique du firmware des abstractions matérielles bas niveau pour réduire la duplication entre les projets utilisant les chipsets Bouffalo Lab.
**Comment ça marche :** Il s'agit d'un référentiel de bibliothèque de composants servant de sous-module pour bl_iot_sdk_tiny, offrant des modules pré-construits (incluant probablement l'intégration de la pile WiFi/BLE, les pilotes de périphériques et les intergiciels) écrits en C/C++. L'architecture sépare le code spécifique au matériel de la logique applicative, permettant aux développeurs d'importer uniquement les composants nécessaires plutôt que le SDK complet. Les dépendances et la liste exacte des modules ne sont pas documentées dans le README accessible ; la vérification des protocoles supportés (802.11b/g/n, BLE 5.x) et des interfaces de périphériques (UART, SPI, I2C, GPIO) nécessite l'inspection du référentiel.
**Spécificité chinoise :** Bouffalo Lab est une filiale de Nanjing Xiaoxiongpai Intelligent Technology Co., Ltd., une fabless chinoise spécialisée dans les SoC WiFi et BLE ultra-basse consommation (séries BL602, BL604, BL702). Cette bibliothèque de composants supporte directement l'écosystème de chipsets propriétaires de Bouffalo et fait partie de la distribution officielle du SDK IoT pour les fabricants IoT chinois.
**Équivalent occidental :** Registre de composants ESP-IDF (Espressif), écosystème de modules Zephyr (Linux Foundation), bibliothèques HAL STM32CubeMX (STMicroelectronics)
**Maturité :** Actif (★ 3, 3 forks, mis à jour 2026-06)
**Langue :** Anglais
**GitHub :** https://github.com/bouffalolab/bl_iot_sdk-components
---
