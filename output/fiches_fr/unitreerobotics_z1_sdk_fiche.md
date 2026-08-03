---
## unitreerobotics/z1_sdk
**Type :** Framework
**Domaine :** Robotique
**Score de pertinence :** 56/100
**Problème résolu :** Fournir un kit de développement logiciel pour contrôler le bras manipulateur Unitree Z1, permettant aux utilisateurs d'interfacer les actionneurs, capteurs et cinématique du robot via une API standardisée plutôt que de rétro-ingénier les protocoles de communication propriétaires.
**Comment ça marche :** Le SDK expose les interfaces de contrôle du bras manipulateur Z1 (un manipulateur 6-DDL) via des liaisons C++ et Python. Il abstrait le contrôle moteur bas niveau, la rétroaction articulaire et le calcul de cinématique inverse. Le projet référence la documentation officielle Unitree (anglais et chinois) mais l'extrait README ne détaille pas les dépendances spécifiques, les protocoles de communication (CAN/Ethernet/propriétaire), ni s'il encapsule une couche micrologicielle fermée.
**Spécificité chinoise :** Hébergé sur Gitee par unitreerobotics (Unitree Robotics, un fabricant chinois de robotique basé à Hangzhou). Unitree est connu pour ses plateformes quadrupèdes et manipulatrices dans l'écosystème de la robotique chinoise ; aucune intégration explicite avec les plateformes cloud chinoises ou les fournisseurs de puces n'est documentée.
**Équivalent occidental :** MoveIt (planification de manipulation basée sur ROS), URScript de Universal Robots (SDK propriétaire de bras UR), SDK FANUC ROBOGUIDE
**Maturité :** Expérimental (★ 45, 39 forks, mis à jour 2025-09)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/z1_sdk
---
