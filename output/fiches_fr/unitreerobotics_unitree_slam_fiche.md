---
## unitreerobotics/unitree_slam
**Type :** Library
**Domaine :** Edge AI
**Score de pertinence :** 61/100
**Problème résolu :** Fournir une interface C++ et un code d'exemple pour intégrer le système SLAM propriétaire d'Unitree avec les robots quadrupèdes Unitree (série H1) via Ethernet, permettant aux développeurs d'accéder aux données de localisation et de cartographie du module SLAM embarqué du robot.
**Comment ça marche :** Le projet est un wrapper C++ léger et un système de construction basé sur CMake qui se lie à la bibliothèque SLAM précompilée d'Unitree (située dans unitree_robotics/lib/). Il inclut une application de démonstration (demo_h1) qui se connecte au robot via une interface Ethernet spécifiée (par exemple, eth0 sur le sous-réseau 123.x.x.x) et expose vraisemblablement les sorties de pose/carte SLAM. La construction repose sur CMake standard et nécessite la configuration de LD_LIBRARY_PATH pour localiser le binaire SLAM Unitree propriétaire.
**Spécificité chinoise :** Hébergé sur Gitee par unitreerobotics (Unitree Robotics, un fabricant chinois de robots quadrupèdes). Le projet est étroitement couplé à la plateforme de robot humanoïde H1 propriétaire d'Unitree et à sa pile SLAM fermée ; aucune intégration avec HiSilicon, Rockchip ou d'autres fournisseurs de puces chinoises n'est évidente.
**Équivalent occidental :** Pile SLAM ROS 2 Nav2 (Open Robotics), Cartographer (Google), LOAM (Ji Zhang et al.) — bien que ceux-ci soient open-source et agnostiques au matériel, alors que celui-ci est une interface propriétaire au SLAM fermé d'Unitree.
**Maturité :** Actif (mis à jour 2026-07)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree_slam
---
