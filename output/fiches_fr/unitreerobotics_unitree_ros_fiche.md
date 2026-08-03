---
## unitreerobotics/unitree_ros
**Type :** Framework
**Domaine :** Robotique
**Score de pertinence :** 94/100
**Problème résolu :** Fournir des packages ROS pour la simulation et le contrôle bas niveau (couple, position, vitesse angulaire) des articulations de robots quadrupèdes et humanoïdes Unitree (A1, B1, B2, G1, GO1, GO2, H1, H2, R1, Z1, etc.) via Gazebo, ainsi qu'une interface de contrôle compatible avec les robots réels via unitree_ros_to_real.
**Comment ça marche :** Architecture ROS Melodic/Kinetic avec simulation Gazebo8 : packages de description URDF pour 19 modèles de robots, contrôleurs d'articulations (unitree_controller, z1_controller) utilisant ros-control (controller-interface, effort-controllers, joint-trajectory-controller), et modules de simulation (unitree_gazebo, unitree_legged_control). Dépend de unitree_legged_msgs (depuis unitree_ros_to_real) pour la communication. Pas de support NPU ou inférence embarquée — simulation et contrôle bas niveau uniquement.
**Spécificité chinoise :** Hébergé sur Gitee par unitreerobotics (fabricant chinois de robots quadrupèdes et humanoïdes) ; pas de spécificité chinoise particulière au-delà de l'auteur. Aucun chipset vendor chinois cité, aucune intégration cloud chinoise (Baidu, Aliyun, etc.), aucune conformité à standard chinois détectée.
**Équivalent occidental :** ROS Navigation Stack (Open Robotics), Gazebo (Open Robotics), Boston Dynamics Spot SDK (propriétaire), ANYmal ROS packages (ANYbotics)
**Maturité :** Stable (★ 1494, 442 forks, mis à jour 2026-07)
**Langue :** EN
**GitHub :** https://github.com/unitreerobotics/unitree_ros
---
