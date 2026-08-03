---
## unitreerobotics/point_lio_unilidar
**Type :** Application
**Domaine :** Edge AI
**Score de pertinence :** 71/100
**Problème résolu :** Adapter l'algorithme d'odomètrie lidar-inertielle Point-LIO pour fonctionner avec les capteurs LiDAR L1 et L2 d'Unitree (FOV 360° × 90°, balayage non répétitif) pour la localisation et la cartographie de robots mobiles à basse vitesse en conditions de vibration et de mouvement agressif.
**Comment ça marche :** Application ROS Noetic encapsulant l'algorithme Point-LIO avec les pilotes de capteurs pour Unitree L1 (via unilidar_sdk) et L2 (via unilidar_sdk2). Utilise Eigen pour l'algèbre linéaire, PCL pour le traitement des nuages de points, et la fusion IMU pour l'estimation de l'odomètrie. Produit des estimations de pose et des cartes 3D (format PCD) via les topics ROS ; testé sur Ubuntu 20.04 avec les ensembles de données rosbag fournis pour la validation hors ligne.
**Spécificité chinoise :** Hébergé sur GitHub par unitreerobotics (Unitree Robotics, fabricant chinois de robots quadrupèdes et de capteurs) ; intègre le matériel LiDAR propriétaire d'Unitree (L1, L2) et leurs SDK, mais aucune conformité aux normes chinoises ou aux services cloud domestiques n'est documentée.
**Équivalent occidental :** Fast-LIO2 (HKU-MARS), LOAM (Ji Zhang), Cartographer (Google)
**Maturité :** Expérimental (★ 505, 94 forks, mis à jour 2025-06)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/point_lio_unilidar
---
