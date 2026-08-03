---
## unitreerobotics/unitree_ros2
**Type :** Framework
**Domaine :** Robotique
**Score de pertinence :** 71/100
**Problème résolu :** Activer la communication native ROS2 avec les robots quadrupèdes Unitree (Go2, B2, H1) en exposant leur SDK basé sur CycloneDDS en tant que types de messages ROS2 standard, éliminant le besoin d'encapsuler les interfaces SDK propriétaires.
**Comment ça marche :** Le projet relie Unitree SDK2 (construit sur CycloneDDS 0.10.2) avec ROS2 en fournissant des définitions de messages ROS2 et des packages d'exemple. Il nécessite Ubuntu 20.04/22.04, ROS2 foxy/humble, le middleware CycloneDDS (compilé séparément pour foxy), libyaml-cpp-dev et rmw-cyclonedds-cpp. L'espace de travail contient cyclonedds_ws avec les packages de messages unitree_go et unitree_api, plus des applications d'exemple démontrant le contrôle et la communication du robot.
**Spécificité chinoise :** Hébergé sur GitHub par unitreerobotics (Unitree Robotics, un fabricant chinois de robots quadrupèdes) ; aucune norme chinoise particulière ou lien avec un fournisseur de chipset au-delà de la plateforme robotique commerciale de l'auteur.
**Équivalent occidental :** MoveIt2 (planification de mouvement ROS2), packages ROS2 de Clearpath Robotics (intégration ROS2 de robots commerciaux)
**Maturité :** Stable (★ 779, 229 forks, mis à jour 2026-07)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree_ros2
---
