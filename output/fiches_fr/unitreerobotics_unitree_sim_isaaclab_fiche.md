---
## unitreerobotics/unitree_sim_isaaclab
**Type :** Application
**Domaine :** Robotique
**Score de pertinence :** 81/100
**Problème résolu :** Fournir un environnement de simulation basé sur DDS pour les robots humanoïdes Unitree (G1, H1-2) qui reproduit les protocoles de communication des robots réels, permettant l'apprentissage de tâches hors ligne, la génération de jeux de données et la validation d'algorithmes sans accès au matériel.
**Comment ça marche :** Construit sur NVIDIA Isaac Lab (framework de simulation robotique basé sur Python) et Isaac Sim 4.5.0/5.x (moteur physique basé sur Omniverse). Implémente la publication/souscription de sujets DDS (Data Distribution Service) pour correspondre aux interfaces des robots Unitree réels. Supporte plusieurs scénarios de tâches (locomotion, manipulation, contrôle du corps entier) avec les modèles de robots G1/H1-2. Nécessite des GPU série RTX 30/40/50 ; installation via le script auto_setup_env.sh ou configuration manuelle pip/conda sur Ubuntu 20.04/22.04+.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par unitreerobotics (Unitree Robotics, un fabricant chinois de robots quadrupèdes et humanoïdes). Aucune intégration particulière de chipset ou de norme chinoise au-delà de la plateforme robotique commerciale de l'auteur.
**Équivalent occidental :** NVIDIA Isaac Sim avec modèles de robots personnalisés, Gazebo (écosystème ROS), MuJoCo avec liaisons spécifiques aux robots
**Maturité :** Stable (★ 530, 139 forks, mis à jour 2026-03)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/unitreerobotics/unitree_sim_isaaclab
---
