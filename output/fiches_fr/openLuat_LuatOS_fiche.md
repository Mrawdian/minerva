---
## openLuat/LuatOS [MODIFIÉ]
**Type :** Framework
**Domaine :** Embarqué
**Score de pertinence :** 82/100
**Problème résolu :** Permettre le développement rapide d'applications IoT sur les modules cellulaires Hezhou (série Air8000/Air8101/Air780E) en utilisant le scripting Lua au lieu de C/C++, réduisant les cycles de développement du firmware pour les appareils IoT industriels.
**Comment ça marche :** LuatOS encapsule la VM Lua 5.3 avec 74 bibliothèques principales et 55 bibliothèques d'extension (totalisant plus de 1000 API) compilées en tant que composants C. L'architecture se compose de : noyau interpréteur Lua, couche framework LuatOS (dossier luat), implémentations BSP spécifiques au matériel pour les modules Air8000/Air8101/Air780E, et bibliothèques de scripts Lua. Le firmware est flashé sur les modules Hezhou ; le développement utilise des scripts Lua exécutés par la VM embarquée avec accès aux API cellulaires, GPIO, UART, SPI et capteurs.
**Spécificité chinoise :** Développé par openLuat (division logicielle de 合宙) spécifiquement pour la gamme propriétaire de modules cellulaires de Hezhou (série Air8000/Air8101/Air780E), qui domine les déploiements IoT industriels chinois. Hezhou est un fournisseur majeur de modules cellulaires dans la chaîne d'approvisionnement IoT chinoise.
**Équivalent occidental :** MicroPython (Python Software Foundation), Espressif ESP-IDF avec liaisons Lua, NodeMCU (Lua sur ESP8266)
**Maturité :** Stable (★ 1862, 514 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/openLuat/LuatOS
---
