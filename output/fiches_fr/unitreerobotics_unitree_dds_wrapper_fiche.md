---
## unitreerobotics/unitree_dds_wrapper
**Type :** Library
**Domaine :** Edge AI
**Score de pertinence :** 49/100
**Problème résolu :** Abstrait la couche middleware DDS (Data Distribution Service) pour les robots quadrupèdes Unitree, éliminant le besoin d'écrire manuellement du code passe-partout pour les éditeurs/abonnés et de gérer les définitions de messages générées par IDL.
**Comment ça marche :** Fournit des classes wrapper Python auto-générées ({robot}_pub, {robot}_sub) à partir de spécifications IDL avec des valeurs par défaut pré-remplies, réduisant les frictions d'intégration. Construit au-dessus du middleware DDS (probablement CycloneDDS ou similaire) ; dépend de Pinocchio pour la cinématique/dynamique. Installable via pip ; cible les environnements Python 3.x sur les systèmes compatibles avec le SDK robot d'Unitree.
**Spécificité chinoise :** Hébergé sur GitHub par unitreerobotics (Unitree Robotics, un fabricant chinois de robots quadrupèdes) ; aucune spécificité chinoise particulière au-delà de l'origine de l'auteur et de la concentration sur les plateformes robots propriétaires d'Unitree.
**Équivalent occidental :** Couche d'abstraction ROS 2 DDS, liaisons Python Cyclone DDS
**Maturité :** Expérimental (★ 33, 6 forks, mis à jour 2024-10)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree_dds_wrapper
---
