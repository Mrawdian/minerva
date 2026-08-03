---
## unitreerobotics/unitree_rl_gym
**Type :** Framework
**Domaine :** Robotique
**Score de pertinence :** 73/100
**Problème résolu :** Fournit un pipeline d'entraînement par apprentissage par renforcement et un cadre de déploiement sim-to-real pour le contrôle de la locomotion des robots à pattes, comblant l'écart entre l'entraînement des politiques en simulation Isaac Gym et l'exécution sur des robots quadrupèdes et humanoïdes Unitree physiques (Go2, G1, H1).
**Comment ça marche :** Construit sur legged_gym (ETH Zurich) pour l'environnement d'entraînement RL, rsl_rl pour l'optimisation des politiques, et MuJoCo pour la simulation physique. Les scripts d'entraînement basés sur Python génèrent des politiques de contrôle ; les modules de déploiement ciblent le transfert sim-to-sim MuJoCo et le matériel réel via unitree_sdk2_python (communication basée sur UDP). Inclut des binaires de déploiement C++ pour le robot G1 compilés avec CMake. Supporte le mode d'entraînement sans interface graphique et le chargement de modèles basé sur des points de contrôle.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par unitreerobotics ; aucune spécificité chinoise particulière au-delà de l'auteur. Unitree Robotics est un fabricant chinois de robots à pattes, mais le cadre lui-même est construit sur des fondations open-source occidentales (legged_gym d'ETH Zurich, MuJoCo de Google DeepMind) sans intégration de plateformes cloud chinoises ou de fournisseurs de puces.
**Équivalent occidental :** legged_gym (ETH Zurich), Isaac Gym (NVIDIA), Gazebo avec ROS (Open Robotics)
**Maturité :** Expérimental (★ 3461, 570 forks, mis à jour 2025-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/unitreerobotics/unitree_rl_gym
---
