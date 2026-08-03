---
## unitreerobotics/dfx_inspire_service
**Type :** Application
**Domaine :** Edge AI
**Score de pertinence :** 57/100
**Problème résolu :** Fournit une interface de contrôleur pour la main dextère Unitree RH56DFX Inspire (12 moteurs sur les deux mains) via connexion série, traduisant les messages de commande moteur de haut niveau (MotorCmds_) en contrôle matériel de bas niveau et exposant la rétroaction d'état moteur (MotorStates_) via le middleware DDS.
**Comment ça marche :** Application C++ construite sur unitree_sdk2, utilisant Cyclone DDS pour la communication inter-processus sur des sujets (rt/inspire/cmd pour les commandes, rt/inspire/state pour la télémétrie). Dépend des bibliothèques Boost et spdlog. Communique avec les plateformes robotiques H1 ou G1 via port série (/dev/ttyUSB*), sérialisant/désérialisant les structures de messages définies par IDL (MotorCmds_, MotorStates_) en utilisant l'encodage xcdr_v2 d'Eclipse Cyclone DDS.
**Spécificité chinoise :** Hébergé sur GitHub par unitreerobotics ; aucune spécificité chinoise particulière au-delà de l'auteur. Unitree Robotics est une entreprise chinoise de robotique, mais ce projet est une interface de contrôleur standard sans liens avec les fournisseurs de puces, normes ou plateformes cloud chinois.
**Équivalent occidental :** Aucun équivalent direct connu — combinaison spécifique d'intégration SDK Unitree, middleware basé sur DDS et contrôle moteur de main dextère.
**Maturité :** Expérimental (★ 50, 15 forks, mis à jour 2025-09)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/dfx_inspire_service
---
