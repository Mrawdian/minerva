---
## unitreerobotics/z1_ros
**Type :** Driver
**Domaine :** Robotique
**Score de pertinence :** 62/100
**Problème résolu :** Fournir une pile de pilotes ROS pour le bras robotique Unitree Z1, comblant le fossé entre le SDK Z1 propriétaire (communication basée sur UDP) et le middleware de planification de mouvement MoveIt par le biais d'une couche d'abstraction matérielle.
**Comment ça marche :** La suite de paquets se compose de z1_hw (interface matérielle MoveIt exposant joint_trajectory_controller et serveur d'action de pince), z1_controller (contrôle direct du bras et intégration SDK), z1_moveit_config (configuration MoveIt), z1_rviz (visualisation) et z1_examples (démonstrations d'utilisation). Écrit en C++ et Python, il dépend de ROS (version non spécifiée), MoveIt, et communique avec le bras Z1 via UDP. Le paquet z1_sdk fournit des exemples de communication UDP de bas niveau.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par unitreerobotics ; aucune spécificité chinoise particulière au-delà de l'auteur. Unitree Robotics est une entreprise chinoise de robotique, mais il s'agit d'un paquet d'intégration ROS standard sans liens avec les fournisseurs de puces ou les normes chinoises.
**Équivalent occidental :** Pilote ROS Universal Robots, paquets ROS Industrial ABB, interface ROS Franka Emika Panda
**Maturité :** Expérimental (★ 43, 31 forks, mis à jour 2024-12)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/z1_ros
---
