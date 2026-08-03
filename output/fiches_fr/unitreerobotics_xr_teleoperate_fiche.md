---
## unitreerobotics/xr_teleoperate [MODIFIÉ]
**Type :** Application
**Domaine :** Robotique
**Score de pertinence :** 88/100
**Problème résolu :** Activer la téléopération en temps réel des robots humanoïdes Unitree (séries H2, R1, G1) à partir de casques XR (Apple Vision Pro, Meta Quest, PICO) en mappant la pose main/bras des contrôleurs XR aux commandes articulaires du robot via une pile de contrôle basée sur Python.
**Comment ça marche :** Le système s'exécute sur Ubuntu 20.04/22.04 avec un environnement conda Python 3.10, utilisant pinocchio pour la cinématique inverse et unitree_sdk2_python pour la communication avec le robot. Les modules principaux incluent teleimager (vision/estimation de pose), teleop_hand_and_arm.py (boucle de contrôle principale) et le support de plusieurs modes d'entrée (suivi des mains, contrôleur BrainCo). Supporte à la fois les robots matériels et la simulation Isaac Lab avec des effecteurs configurables (dex3, dex5) et des types de bras (G1_29, G1_23, H2, R1_A5, R1_A7).
**Spécificité chinoise :** Hébergé sur GitHub par unitreerobotics (Unitree Robotics, un fabricant chinois de robots humanoïdes) ; le projet est étroitement couplé aux modèles de robots propriétaires d'Unitree et à l'écosystème SDK, sans intégration évidente de normes chinoises plus larges ou de fournisseurs de puces.
**Équivalent occidental :** OpenTeleVision (framework de téléopération open-source), APIs de téléopération Spot de Boston Dynamics (propriétaire), pile de téléopération Shadow Robot
**Maturité :** Stable (★ 1585, 306 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/unitreerobotics/xr_teleoperate
---
