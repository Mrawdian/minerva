---
## unitreerobotics/dex1_1_service
**Type :** Driver
**Domaine :** Embarqué
**Score de pertinence :** 62/100
**Problème résolu :** Fournit un pont série-DDS pour la pince parallèle Unitree Dex1-1 (moteurs M4010 doubles), permettant aux applications ROS 2 de commander et surveiller les positions des doigts gauche/droit via des sujets DDS standardisés (rt/dex1/left/cmd, rt/dex1/right/cmd, etc.) au lieu de protocoles série bruts.
**Comment ça marche :** Application C++ qui encapsule libserialport (bibliothèque de communication série) pour interfacer deux contrôleurs de moteur M4010 sur UART, traduisant les messages de commande DDS entrants en trames de contrôle moteur et publiant les retours d'état moteur en tant que sujets DDS. Inclut un utilitaire d'étalonnage (dex1_1_gripper_server) pour la détection du point zéro et l'intégration systemd pour le démarrage automatique. Dépendances : libserialport 0.1.1, middleware DDS ROS 2, compilateur C++17.
**Spécificité chinoise :** Hébergé sur Gitee par unitreerobotics, la division robotique d'Unitree Robotics (fabricant chinois de robots quadrupèdes/humanoïdes). La pince Dex1-1 et le moteur M4010 sont des composants matériels propriétaires d'Unitree ; aucune intégration avec des plateformes ou normes cloud chinoises détectée.
**Équivalent occidental :** Aucun équivalent direct connu — spécifique au matériel de pince propriétaire d'Unitree et au protocole moteur ; comparable en portée aux pilotes ROS 2 fournis par le fournisseur pour les pinces industrielles (par exemple, Schunk, OnRobot) mais pas un cadre à usage général.
**Maturité :** Actif (★ 19, 5 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/unitreerobotics/dex1_1_service
---
