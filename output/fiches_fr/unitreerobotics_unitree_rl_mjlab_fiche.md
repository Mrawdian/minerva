---
## unitreerobotics/unitree_rl_mjlab
**Type :** Framework
**Domaine :** Robotique
**Score de pertinence :** 74/100
**Problème résolu :** Fournir un framework d'apprentissage par renforcement léger et modulaire pour l'entraînement et le déploiement de politiques de locomotion sur les robots quadrupèdes et humanoïdes Unitree en utilisant la simulation physique MuJoCo, avec transfert direct sim-to-real via export ONNX.
**Comment ça marche :** Construit sur mjlab (qui combine l'API d'Isaac Lab avec la physique MuJoCo), le framework implémente des boucles d'entraînement RL en Python en utilisant l'optimisation de politique basée sur les récompenses. Supporte l'entraînement multi-GPU via PyTorch, exporte les politiques entraînées en tant que modèles ONNX pour le déploiement. Cible les robots Unitree Go2, A2, As2, G1, R1, H1_2 et H2. Le déploiement nécessite cyclonedds et unitree_sdk2 pour la communication avec le robot.
**Spécificité chinoise :** Hébergé par unitreerobotics (Unitree Robotics, un fabricant chinois de robots quadrupèdes/humanoïdes) ; aucune intégration particulière de fournisseur de chipset chinois ou de norme au-delà de la plateforme commerciale de robots de l'auteur.
**Équivalent occidental :** Isaac Lab (NVIDIA), Legged Gym (ETH Zurich), rsl_rl (ETH Zurich)
**Maturité :** Stable (★ 558, 157 forks, mis à jour 2026-04)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree_rl_mjlab
---
