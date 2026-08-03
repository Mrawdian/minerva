---
## bouffalolab/bouffalo_isp
**Type :** Tool
**Domaine :** Embarqué
**Score de pertinence :** 65/100
**Problème résolu :** Fournir un outil ISP (In-System Programming) hébergé sous Linux pour flasher le firmware dans les MCU RISC-V et ARM de BouffaloLab (séries BL602, BL702, BL616) via interface série, remplaçant les utilitaires de flashage propriétaires Windows uniquement du fournisseur.
**Comment ça marche :** Utilitaire en ligne de commande basé sur C qui communique avec les puces BouffaloLab via UART à des débits configurables (par exemple, 2 Mbps). Accepte les images de firmware binaires pré-compilées (bootloader combiné + application + binaires auxiliaires) et les écrit via le protocole ISP intégré de la puce. Nécessite une compilation croisée pour la plateforme Linux cible (x86, ARM) via CMake ; la configuration des broches de démarrage et de réinitialisation est modifiable par l'utilisateur dans user_config.h. Aucune dépendance externe au-delà de la bibliothèque C standard et des E/S série.
**Spécificité chinoise :** BouffaloLab est une filiale de Nantong Bouffalo Technology, une fabless chinoise spécialisée dans les MCU IoT/edge basés sur RISC-V et ARM. Le projet supporte directement les familles de puces propriétaires de BouffaloLab (BL602, BL702, BL616, BL808), largement utilisées dans les applications IoT et d'IA edge chinoises.
**Équivalent occidental :** esptool.py (Espressif, pour le flashage ESP32), openocd (débogage et flashage ARM/RISC-V), pyocd (flashage ARM Cortex-M)
**Maturité :** Expérimental (★ 4, 1 forks, mis à jour 2025-03)
**Langue :** Anglais
**GitHub :** https://github.com/bouffalolab/bouffalo_isp
---
