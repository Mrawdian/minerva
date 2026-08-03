---
## unitreerobotics/unitree-motor-debugging-assistant
**Type :** Tool
**Domaine :** Embarqué
**Score de pertinence :** 63/100
**Problème résolu :** Fournir une interface graphique Windows pour le débogage en temps réel, l'ajustement des paramètres et la gestion du micrologiciel des moteurs sans balais Unitree GO-M8010-6 via communication série, éliminant le besoin d'outils en ligne de commande ou d'utilitaires propriétaires fermés.
**Comment ça marche :** Un frontal basé sur Electron (HTML/CSS/JavaScript) communique via HTTP et WebSocket avec un serveur backend local Node.js/C++ (server.exe) s'exécutant sur localhost:26565. Le backend gère l'énumération des ports série, l'analyse du protocole moteur (ID moteur, mode, couple, vitesse, position, température, drapeaux d'erreur), la distribution des commandes et le téléchargement du binaire du micrologiciel. Les opérations de configuration incluent la requête/modification d'ID, la récupération de mode, le contrôle d'auto-calibrage, l'effacement d'erreurs et le flashage du micrologiciel .bin. Les journaux sont écrits dans %APPDATA%\unitree-motor-debugging-assistant\logs\.
**Spécificité chinoise :** Unitree Robotics (宇树科技, HangZhou YuShu TECHNOLOGY CO.,LTD.) est un fabricant chinois de robots quadrupèdes et humanoïdes ; cet outil est leur utilitaire officiel de débogage moteur pour leur gamme d'actionneurs GO-M8010-6. Aucune intégration avec les plateformes cloud chinoises ou les fournisseurs de puces n'est documentée.
**Équivalent occidental :** Aucun équivalent direct connu — spécifique au protocole moteur propriétaire et à l'écosystème matériel d'Unitree ; comparable aux interfaces graphiques d'ajustement moteur fournies par les fabricants (par exemple, Maxon EPOS Studio, Elmo Studio) mais fermées et spécifiques au moteur.
**Maturité :** Actif (mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/unitreerobotics/unitree-motor-debugging-assistant
---
