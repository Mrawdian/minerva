---
## unitreerobotics/unitree-app-templates
**Type :** Application
**Domaine :** Robotique
**Score de pertinence :** 59/100
**Problème résolu :** Fournir un modèle standardisé et un cadre d'empaquetage permettant aux développeurs de construire et déployer des applications sur les robots quadrupèdes Unitree (G1, etc.) sans réimplémenter l'infrastructure de déploiement. Abstrait les API de contrôle du robot et la distribution d'applications basée sur Docker.
**Comment ça marche :** Structure monorepo avec des projets d'exemple (G1 Mimic Learning Demo) écrits en C++ pour la logique de contrôle et en Python pour les couches de service. Les applications sont conteneurisées via Docker et doivent exposer un service HTTP sur le port 80, avec les métadonnées définies en YAML. Les développeurs empaquettent les binaires/scripts dans un dossier `app/` et les téléchargent sur UniStore. L'exemple G1 démontre les politiques d'apprentissage par imitation pour le contrôle des mouvements en utilisant le SDK propriétaire d'Unitree.
**Spécificité chinoise :** Unitree Robotics est un fabricant chinois de robots quadrupèdes ; ce référentiel sert de modèle officiel de distribution d'applications pour leur plateforme robotique. Aucune intégration avec les services cloud chinois (Baidu, Aliyun, WeChat) n'est documentée ; la spécificité réside principalement dans le rôle de l'organisation mère dans l'industrie robotique chinoise.
**Équivalent occidental :** Boston Dynamics Spot SDK (propriétaire), intégration ANYmal ROS2 (ANYbotics), cadres d'applications Clearpath Robotics Warthog/Husky
**Maturité :** Actif (★ 16, 5 forks, mis à jour 2026-06)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree-app-templates
---
