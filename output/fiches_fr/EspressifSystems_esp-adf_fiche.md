---
## EspressifSystems/esp-adf [MODIFIÉ]
**Type :** Framework
**Domaine :** Embarqué
**Score de pertinence :** 73/100
**Problème résolu :** Fournir un cadre d'application orienté produit pour le développement audio et vidéo ESP32/ESP32-S2, en abstrayant la complexité de bas niveau d'IDF. ADF v3.0 restructure le pipeline média en utilisant ESP-GMF et modularise les services (lecture audio, lecture vidéo, surveillance de batterie) appelables via Model Context Protocol.
**Comment ça marche :** ADF v3.0 est construit sur ESP-IDF (v5.5.2+) et intègre ESP-GMF comme cadre multimédia principal. Il fournit des composants fonctionnels autonomes (playlist, gestionnaire de carte) et des services produits modulaires accessibles via MCP. Supporte le développement en C/C++, MicroPython et Arduino. L'architecture sépare les pilotes bas niveau (gérés par ESP-IDF) des services haut niveau (lecture audio/vidéo, OTA, service batterie) en mettant l'accent sur la faible empreinte mémoire et CPU.
**Spécificité chinoise :** Espressif Systems (乐鑫, Shanghai) est le fabricant des SoCs ESP32/ESP32-S2 et maintient ce cadre officiel. Le référentiel Gitee est un miroir officiel synchronisé depuis GitHub ; aucune conformité à une norme chinoise particulière ou intégration de plateforme domestique mentionnée.
**Équivalent occidental :** Zephyr (Linux Foundation, extensions multimédia), FreeRTOS avec bibliothèques audio (Amazon), TinyOS avec composants média
**Maturité :** Actif (★ 72, 9 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/EspressifSystems/esp-adf
---
