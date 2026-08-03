---
## unitreerobotics/unilidar_sdk2
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 62/100
**Problème résolu :** Fournir un SDK C++ unifié et une couche d'intégration ROS/ROS2 pour le LiDAR Unitree L2 afin d'acquérir les données de nuage de points et d'IMU, configurer les paramètres du capteur et publier les données vers le middleware de robotique sans pilotes propriétaires fermés.
**Comment ça marche :** Le SDK se compose de trois composants principaux : une bibliothèque C++ centrale (unitree_lidar_sdk) qui communique avec le LiDAR L2 via UDP ou port série pour récupérer les trames de nuage de points et les échantillons d'IMU, un wrapper ROS (unitree_lidar_ros) qui publie les topics sensor_msgs/PointCloud2 et sensor_msgs/Imu, et un équivalent ROS2 (unitree_lidar_ros2) pour les environnements ROS2. La bibliothèque expose des interfaces pour définir les modes de fonctionnement (commutation du champ de vision, activation/désactivation de l'IMU), récupérer les paramètres d'étalonnage et gérer les transformations de repères de coordonnées entre les systèmes de coordonnées du LiDAR et de l'IMU. Les dépendances incluent CMake, les bibliothèques principales ROS/ROS2 et C++11 standard.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par unitreerobotics ; aucune spécificité chinoise particulière au-delà de l'auteur. Unitree Robotics est une entreprise chinoise de robotique, mais le LiDAR L2 et le SDK suivent des interfaces de capteur standard (UDP/série, middleware ROS/ROS2) sans intégration aux plateformes cloud chinoises ou aux normes propriétaires.
**Équivalent occidental :** Pilotes ROS pour LiDARs Velodyne/Ouster, livox_ros_driver (DJI), paquets ROS SICK LiDAR
**Maturité :** Expérimental (★ 93, 58 forks, mis à jour 2025-03)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/unitreerobotics/unilidar_sdk2
---
