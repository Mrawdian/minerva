---
## unitreerobotics/unitree_sdk2_python
**Type :** Library
**Domaine :** Robotique
**Score de pertinence :** 72/100
**Problème résolu :** Fournit une couche de liaison Python pour le SDK2 de contrôle de robot quadrupède d'Unitree, permettant des commandes moteur de haut niveau (mode sport, suivi de trajectoire, contrôle d'attitude) et de bas niveau (PID articulaire, couple moteur) via Ethernet par le middleware CycloneDDS, éliminant le besoin d'écrire manuellement des liaisons C++.
**Comment ça marche :** Wrapper Python 3.8+ autour de unitree_sdk2 utilisant CycloneDDS 0.10.2 comme middleware DDS pour la communication inter-processus. Dépendances principales : numpy, opencv-python. Expose deux couches de contrôle : API haut niveau (StandUpDown, VelocityMove, BalanceAttitude, TrajectoryFollow, SpecialMotions) et API bas niveau (lecture d'état articulaire, contrôle PID moteur avec gains kp/kd, télémétrie IMU/batterie). Les exemples incluent des modèles éditeur/abonné, interrogation du statut du contrôleur sans fil et capture de trames de caméra frontale via OpenCV.
**Spécificité chinoise :** Hébergé sur GitHub par unitreerobotics (Unitree Robotics, un fabricant chinois de robotique quadrupède). Aucune conformité à un fournisseur de chipset chinois particulier ou à une norme citée ; le projet est une interface Python pour le SDK2 propriétaire d'Unitree destiné à leurs plateformes de robot Go1/Go2.
**Équivalent occidental :** Spot SDK (Python) de Boston Dynamics, pile de pilotes ROS2 ANYmal, SDK Warthog de Clearpath Robotics
**Maturité :** Stable (★ 750, 312 forks, mis à jour 2026-07)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree_sdk2_python
---
