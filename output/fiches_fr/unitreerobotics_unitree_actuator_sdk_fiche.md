---
## unitreerobotics/unitree_actuator_sdk
**Type :** Library
**Domaine :** Edge AI
**Score de pertinence :** 64/100
**Problème résolu :** Fournir un SDK C++/Python pour contrôler les actionneurs Unitree (moteurs GO-M8010-6, A1, B1) via communication série, en gérant les transformations de coordonnées côté moteur par rapport au côté sortie et les conversions de rapport de réduction qui ne sont pas triviales pour les applications de robotique.
**Comment ça marche :** Le SDK expose le contrôle moteur via des classes C++ et des liaisons Python, supportant la communication série avec les moteurs Unitree. Les composants principaux incluent les énumérations de type moteur (MotorType::A1, MotorType::B1), les modes de contrôle (FOC), et les structures de commande (cmd, data) avec des champs pour les gains proportionnel/dérivé (kp, kd), la position (q), la vitesse (dq), et le couple (tau). Le système de construction utilise CMake ; nécessite gcc ≥5.4.0 (x86) ou ≥7.5.0 (ARM). Les exemples démontrent la conversion de coordonnées rotor-vers-sortie en utilisant des formules de mise à l'échelle du rapport de réduction.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par unitreerobotics ; aucune spécificité chinoise particulière au-delà de l'auteur. Unitree Robotics est une entreprise chinoise de robotique, mais le SDK cible leur matériel moteur propriétaire plutôt qu'un fournisseur de chipset chinois ou une norme.
**Équivalent occidental :** Aucun équivalent direct connu — combinaison spécifique d'un SDK de contrôle moteur basé sur série avec transformation de coordonnées côté rotor/sortie pour les actionneurs de robots quadrupèdes/à pattes.
**Maturité :** Expérimental (★ 132, 39 forks, mis à jour 2025-01)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/unitree_actuator_sdk
---
