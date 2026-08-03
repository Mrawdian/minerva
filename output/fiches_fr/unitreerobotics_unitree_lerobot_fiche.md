---
## unitreerobotics/unitree_lerobot
**Type :** Framework
**Domaine :** Edge AI
**Score de pertinence :** 77/100
**Problème résolu :** Activer l'entraînement et le déploiement de politiques d'apprentissage par imitation sur les robots bi-bras Unitree G1 en utilisant le framework LeRobot, avec des utilitaires de conversion de données pour les formats propriétaires de mains Unitree (Dex1, Dex3, BrainCo, Inspire1) en datasets compatibles LeRobot.
**Comment ça marche :** Le projet encapsule le framework d'entraînement LeRobot (commit 0878c68) avec des extensions spécifiques à Unitree : un module `utils` pour la conversion de datasets depuis les robots Unitree au format LeRobot v3.0, un module `eval_robot` pour la validation d'inférence en conditions réelles via unitree_sdk2_python (communication basée sur DDS), et le support de plusieurs architectures de politiques (PI05, GROOT). Les dépendances incluent PyTorch, le cœur LeRobot, et unitree_sdk2_python pour le contrôle du robot ; les langages principaux sont Python et YAML pour la configuration.
**Spécificité chinoise :** Unitree Robotics est un fabricant chinois de robotique spécialisé dans les plateformes quadrupèdes et humanoïdes ; ce projet intègre directement le matériel propriétaire du robot G1 et les variantes de mains dextères (Dex1, Dex3) avec le framework open-source LeRobot, permettant aux roboticiens chinois de tirer parti de l'apprentissage par imitation sur les plateformes Unitree.
**Équivalent occidental :** LeRobot (Hugging Face), Mobile ALOHA (Stanford), Diffusion Policy (UC Berkeley) — tous des frameworks d'apprentissage par imitation, mais unitree_lerobot est un adaptateur spécifique au matériel plutôt qu'une architecture de politique autonome.
**Maturité :** Stable (★ 728, 133 forks, mis à jour 2026-05)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/unitreerobotics/unitree_lerobot
---
