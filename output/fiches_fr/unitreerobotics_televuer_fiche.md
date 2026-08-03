---
## unitreerobotics/televuer
**Type :** Library
**Domaine :** Robotique
**Score de pertinence :** 67/100
**Problème résolu :** Activer la téléopération des robots Unitree à partir de casques XR (Apple Vision Pro, Meta Quest 3, Pico 4) en fournissant un suivi des mains/contrôleurs et un streaming de vue à la première personne avec plusieurs modes d'affichage (immersif, pass-through, ego).
**Comment ça marche :** TeleVuer est un wrapper Python autour de la bibliothèque Vuer qui abstrait les API des appareils XR et les interfaces d'état/commande des robots. Il gère le transport d'images via ZMQ ou WebRTC, expose les données de pose des mains/contrôleurs via une structure TeleData unifiée, et gère trois modes d'affichage en contrôlant le rendu du plan d'image. Les dépendances incluent Vuer (framework XR principal), teleimager (capture d'image) et des backends WebRTC/ZMQ optionnels ; il s'intègre avec la bibliothèque xr_teleoperate pour les workflows de téléopération complets.
**Spécificité chinoise :** Hébergé sur GitHub par unitreerobotics (Unitree Robotics, un fabricant chinois de robots quadrupèdes/humanoïdes) ; aucune spécificité particulière de chipset ou de norme chinoise au-delà de la plateforme robotique commerciale de l'auteur.
**Équivalent occidental :** Aucun équivalent direct connu — combinaison spécifique d'une couche d'abstraction d'appareils XR (Vuer) avec un middleware de téléopération de robots pour le suivi des mains/contrôleurs et le streaming vidéo.
**Maturité :** Actif (★ 46, 33 forks, mis à jour 2026-05)
**Langue :** Anglais
**GitHub :** https://github.com/unitreerobotics/televuer
---
