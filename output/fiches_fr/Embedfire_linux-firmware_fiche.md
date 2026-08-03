---
## Embedfire/linux-firmware
**Type :** Documentation
**Domaine :** Embarqué
**Score de pertinence :** 67/100
**Problème résolu :** Fournir les blobs de firmware et les binaires d'arborescence de périphériques requis par le noyau Linux pour initialiser et exploiter les périphériques matériels (WiFi, Bluetooth, GPU, modem, etc.) sur diverses SoCs et cartes embarquées.
**Comment ça marche :** Il s'agit d'un miroir/distribution du dépôt linux-firmware en amont de kernel.org, contenant des fichiers de firmware précompilés (généralement aux formats .bin, .fw, .ucode) et des fichiers source d'arborescence de périphériques organisés par fournisseur de matériel (Broadcom, Qualcomm, Intel, AMD, Marvell, etc.). Le dépôt est indépendant du langage ; il sert de magasin d'artefacts binaires indexé par des identifiants matériels. L'installation implique généralement de copier les fichiers de firmware vers /lib/firmware sur un système Linux lors du démarrage du noyau ou du chargement du module.
**Spécificité chinoise :** Hébergé sur Gitee par Embedfire, une marque d'électronique éducative chinoise ; aucune spécificité chinoise particulière au-delà de l'auteur. Le dépôt lui-même est un miroir direct du firmware kernel.org en amont et ne contient aucune modification spécifique à Embedfire ni intégration de fournisseur de chipset chinois.
**Équivalent occidental :** linux-firmware (kernel.org en amont), firmware-nonfree (Debian), linux-firmware-git (Arch Linux)
**Maturité :** Actif (mis à jour 2026-07)
**Langue :** Anglais
**Gitee :** https://gitee.com/Embedfire/linux-firmware
---
