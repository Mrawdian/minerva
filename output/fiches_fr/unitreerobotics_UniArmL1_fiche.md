---
## unitreerobotics/UniArmL1
**Type :** Framework
**Domaine :** Edge AI
**Score de pertinence :** 71/100
**Problème résolu :** Fournir un framework de téléopération de bras robotique 6-DOF léger avec collecte de données standardisée pour l'apprentissage par imitation. Permet l'intégration transparente des modes de contrôle par contrôleur VR, clavier et leader-follower avec enregistrement multi-caméra synchronisé à fréquence fixe pour les pipelines d'entraînement en aval.
**Comment ça marche :** Stack de téléopération basée sur Python supportant trois modes d'entrée (VR via XRoboToolkit, clavier, leader-follower) communiquant avec le firmware du bras via série (par défaut /dev/ttyACM1). La collecte de données enregistre les angles articulaires et les images de caméra à une fréquence configurable (par défaut 50 Hz) dans un format standardisé compatible avec unitree_lerobot (fork HuggingFace LeRobot). Utilise URDF pour la cinématique, Meshcat pour la visualisation optionnelle, et conda pour la gestion des dépendances. Nécessite une nomenclature matérielle et des composants imprimés en 3D documentés séparément.
**Spécificité chinoise :** Hébergé sur GitHub par unitreerobotics (Unitree Robotics, une entreprise chinoise de systèmes quadrupèdes/robotiques). Aucune conformité spécifique à un fournisseur de chipset ou à une norme chinoise documentée ; le projet est un framework logiciel pour une conception de bras 6-DOF personnalisée dérivée du matériel open-source SO-ARM100.
**Équivalent occidental :** LeRobot (HuggingFace), DOPE (NVIDIA), Mobile ALOHA (Stanford)
**Maturité :** Actif (★ 11, 4 forks, mis à jour 2026-05)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/unitreerobotics/UniArmL1
---
