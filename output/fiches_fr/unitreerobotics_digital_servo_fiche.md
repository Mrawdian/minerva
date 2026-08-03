---
## unitreerobotics/digital_servo
**Type :** Documentation
**Domaine :** Embarqué
**Score de pertinence :** 65/100
**Problème résolu :** Fournir des implémentations de référence pour communiquer avec les servomoteurs articulaires sans balais Unitree J288/S288 sur un bus TTL semi-duplex (6 Mbps, 8N1). Permet à la fois les tests basés sur PC via terminal série et l'intégration embarquée sur microcontrôleurs STM32 sans dépendre de pilotes propriétaires fermés.
**Comment ça marche :** Deux implémentations indépendantes partagent une spécification de protocole commune (paquets de contrôle de 20 octets, paquets de rétroaction de 26 octets, validation CRC32, conversion en virgule fixe). L'implémentation Python fournit un terminal série interactif pour le débogage sur PC ; l'implémentation STM32 est un projet Keil MDK ciblant STM32F413RGT6 avec intégration HAL. Le protocole définit l'adressage de bus à 16 nœuds (0–15), un débit en bauds fixe de 6 Mbps et des formules de conversion de rapport de réduction 288.35:1.
**Spécificité chinoise :** Hébergé sur Gitee par unitreerobotics, la division robotique d'Unitree Robotics (fabricant chinois de robots quadrupèdes). Cible le matériel de servo numérique propriétaire d'Unitree ; aucune intégration avec les plateformes cloud chinoises ou les organismes de normalisation détectée.
**Équivalent occidental :** Aucun équivalent direct connu — spécifique au protocole de servo Unitree ; comparable en portée aux bibliothèques de communication fournies par le fournisseur pour les actionneurs propriétaires (par exemple, documentation du protocole Dynamixel par Robotis).
**Maturité :** Actif (★ 1, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/unitreerobotics/digital_servo
---
