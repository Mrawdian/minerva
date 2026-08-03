---
## unitreerobotics/unitree_sdk2
**Type :** Library
**Domaine :** Edge AI
**Score de pertinence :** 75/100
**Problème résolu :** Fournir un SDK C++ unifié pour contrôler les robots quadrupèdes Unitree (séries Go1, Go2, B1, H1) sur des plateformes de calcul hétérogènes (aarch64, x86_64) sans nécessiter de bibliothèques propriétaires fermées ni de chaînes d'outils spécifiques aux fournisseurs.
**Comment ça marche :** Le SDK est une bibliothèque C++ construite sur CMake, dépendant de libyaml-cpp, Eigen3, Boost, spdlog et libfmt. Elle abstrait les interfaces matérielles du robot (contrôle moteur, IMU, retour articulaire) et fournit des API de haut niveau pour la locomotion, les requêtes d'état et l'accès aux capteurs. Cible Ubuntu 20.04 LTS avec GCC 9.4.0 ; les exemples montrent l'intégration via le mécanisme find_package() de CMake. Aucun noyau RTOS n'est intégré ; la bibliothèque s'exécute sur Linux standard.
**Spécificité chinoise :** Unitree Robotics est un fabricant chinois de robots quadrupèdes (Go1, Go2, B1, H1) basé à Hangzhou ; ce SDK est l'interface de contrôle officielle de deuxième génération pour leur gamme de produits. Aucune intégration avec les plateformes cloud chinoises (Baidu, Alibaba) ou les normes cellulaires (NB-IoT, 5G) n'est documentée.
**Équivalent occidental :** Boston Dynamics Spot SDK (propriétaire), pile de pilotes ANYmal ROS2 (ETH Zurich), SDK Warthog de Clearpath Robotics
**Maturité :** Stable (★ 1258, 367 forks, mis à jour 2026-07)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree_sdk2
---
