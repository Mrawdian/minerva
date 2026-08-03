---
## rtthread/rt-thread [MODIFIÉ]
**Type :** RTOS
**Domaine :** Embarqué
**Score de pertinence :** 100/100
**Problème résolu :** Fournir un système d'exploitation temps réel scalable qui s'exécute sur des microcontrôleurs à ressources limitées (ARM Cortex-M0 avec 3 KB Flash / 1,2 KB RAM) tout en supportant des appareils IoT plus volumineux (ARM Cortex-A, MIPS32/64 multicœur). Unifie le noyau, la BSP, les pilotes de périphériques et un écosystème de composants modulaires (VFS, CLI FinSH, pile réseau) sous un seul RTOS basé sur C.
**Comment ça marche :** RT-Thread est un noyau RTOS monolithique écrit en C, avec une architecture en couches : couche noyau (threading, ordonnancement, sémaphores, boîte aux lettres, file de messages, gestion mémoire, minuteurs), couche libcpu/BSP (portage CPU et pilotes périphériques) et couche composants/services (VFS, interface de ligne de commande FinSH, frameworks réseau, framework de périphériques). Supporte les chaînes d'outils GCC, Keil et IAR. Inclut un gestionnaire de paquets (450+ paquets) pour la composition modulaire de logiciels. Porté sur STM32F103 et autres MCU courants.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par rtthread ; aucune spécificité chinoise particulière au-delà de l'auteur. Fondé en 2006 en tant que projet open-source piloté par la communauté ; aucune affiliation documentée avec HiSilicon, Rockchip, Espressif ou d'autres fournisseurs de puces chinoises.
**Équivalent occidental :** FreeRTOS (Amazon), Zephyr (Linux Foundation), RIOT OS
**Maturité :** Stable (★ 5527, 2264 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/rtthread/rt-thread
---
