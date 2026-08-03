---
## unitreerobotics/unitree_rl_lab
**Type :** Framework
**Domaine :** Robotique / Edge AI
**Score de pertinence :** 75/100
**Problème résolu :** Fournir des environnements d'entraînement par apprentissage par renforcement pour les robots quadrupèdes et humanoïdes Unitree (Go2, H1, G1-29dof) intégrés au simulateur IsaacLab de NVIDIA, permettant le transfert de politique sim-to-sim et sim-to-real sans frameworks d'entraînement propriétaires.
**Comment ça marche :** Construit sur IsaacLab (framework de simulation physique de NVIDIA) et MuJoCo pour la définition d'environnements ; entraînement RL basé sur Python avec support du déploiement de politique via des contrôleurs de robot C++ compilés contre unitree_sdk2. Inclut des environnements IsaacLab autonomes installables via pip, simulation MuJoCo pour la validation, et des binaires de déploiement C++ (g1_ctrl, etc.) qui communiquent avec les robots via Ethernet en utilisant le protocole propriétaire de Unitree. Dépendances : YAML-cpp, Boost, Eigen3, spdlog, fmt pour la couche de contrôle.
**Spécificité chinoise :** Hébergé par Unitree Robotics, un fabricant chinois de robots quadrupèdes et humanoïdes ; aucune intégration avec les plateformes cloud chinoises ou les fournisseurs de chipsets (utilise les GPU NVIDIA pour l'entraînement, x86/ARM standard pour le déploiement). Le projet est spécifique au matériel Unitree mais suit autrement les conventions open-source occidentales.
**Équivalent occidental :** NVIDIA IsaacGym (baseline propriétaire), OpenAI Gym avec backend MuJoCo, Gazebo avec ROS 2 pour la simulation de robot et l'entraînement RL
**Maturité :** Stable (★ 1245, 301 forks, mis à jour 2026-05)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree_rl_lab
---
