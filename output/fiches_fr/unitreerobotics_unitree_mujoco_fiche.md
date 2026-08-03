---
## unitreerobotics/unitree_mujoco
**Type :** Tool
**Domaine :** Robotique / Edge AI
**Score de pertinence :** 70/100
**Problème résolu :** Permettre un transfert sim-to-real transparent des programmes de contrôle écrits pour les robots quadrupèdes Unitree (Go2, B2, H1, G1, etc.) en fournissant un simulateur basé sur MuJoCo qui parle nativement le protocole de messages Unitree SDK2 (LowCmd, LowState, SportModeState, IMUState) sans nécessiter de réécriture de code.
**Comment ça marche :** Le simulateur encapsule le moteur physique MuJoCo avec des liaisons Unitree SDK2 en C++ (principal) et variantes Python. Il accepte des commandes moteur bas niveau (LowCmd) et retourne l'état moteur (LowState) et les données IMU/odométrie (SportModeState, IMUState) via des types de messages basés sur DDS (unitree_go IDL pour Go2/B2/H1, unitree_hg IDL pour G1/H1-2). Les morphologies de robot sont définies au format MJCF ; un outil de génération de terrain est inclus. Dépendances : libyaml-cpp, libspdlog, libboost, libglfw3, MuJoCo 3.3.6+, unitree_sdk2.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par unitreerobotics ; aucune spécificité chinoise particulière au-delà de l'auteur. Unitree Robotics est un fabricant chinois de robotique quadrupède, mais le simulateur utilise des outils open-source occidentaux (MuJoCo par DeepMind, DDS standard) sans lien propriétaire à une puce ou conformité spécifique au fournisseur.
**Équivalent occidental :** Gazebo (Open Robotics) avec plugin Unitree personnalisé, Isaac Sim (NVIDIA) avec adaptateurs spécifiques au robot, CoppeliaSim avec liaisons Unitree SDK — mais aucun n'offre une compatibilité native et clé en main avec les messages Unitree SDK2.
**Maturité :** Stable (★ 1111, 378 forks, mis à jour 2026-06)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree_mujoco
---
