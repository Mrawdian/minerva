---
## unitreerobotics/kinect_teleoperate
**Type :** Application
**Domaine :** Robotique
**Score de pertinence :** 70/100
**Problème résolu :** Activer la téléopération des robots humanoïdes Unitree H1/G1 à l'aide de la caméra Azure Kinect DK pour le suivi du squelette et la capture de mouvement, en reliant le matériel de détection de profondeur de Microsoft à la pile de contrôle des robots Unitree.
**Comment ça marche :** Le système intègre le SDK Azure Kinect (SDK caméra v1.4.1 et SDK de suivi corporel v1.1.2) s'exécutant sur Ubuntu 20.04 pour capturer la vidéo RGB-D et les positions des articulations du squelette via k4abt_simple_3d_viewer. Il traduit les poses humaines détectées en commandes d'articulation de robot pour la plateforme H1/G1. Les dépendances incluent libk4a1.4, libk4abt1.1, les fichiers de configuration CMake (k4abtConfig.cmake) et les règles udev pour l'accès aux appareils USB 3.0. La base de code est écrite en C++ avec intégration ROS (à confirmer).
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par unitreerobotics ; aucune spécificité chinoise particulière au-delà de l'auteur. Unitree Robotics est un fabricant chinois de robots quadrupèdes et humanoïdes, mais ce projet utilise le matériel Microsoft Azure Kinect et n'intègre pas de capteurs, puces ou plateformes cloud spécifiques à la Chine.
**Équivalent occidental :** Exemples Microsoft Azure Kinect (Microsoft), piles de téléopération OpenPose + ROS (CMU/Facebook), cadres de téléopération Kinect v2 (recherche académique)
**Maturité :** Expérimental (★ 117, 28 forks, mis à jour 2024-08)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/kinect_teleoperate
---
