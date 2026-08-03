---
## sophgo/bootloader-arm64
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 61/100
**Problème résolu :** Fournir un bootloader pour les puces accélérateurs Sophon AI (SoC BM1684) qui initialise le matériel ARM64, charge le noyau Linux et établit un pont entre le firmware propriétaire Sophon et le flux de démarrage du système d'exploitation open-source.
**Comment ça marche :** Le projet est un bootloader basé sur U-Boot (architecture ARM64) qui s'intègre avec un port de noyau Linux personnalisé (linux-arm64) et la pile middleware Sophon. Le processus de compilation utilise la chaîne d'outils GCC Linaro 6.3.1, device-tree-compiler et u-boot-tools ; il génère des paquets Debian (sophon-soc-libsophon, sophon-mw-soc-sophon-ffmpeg, sophon-mw-soc-sophon-opencv) qui sont intégrés dans un rootfs via debootstrap. Le bootloader dépend de libsophon (référentiel séparé) pour l'abstraction matérielle et se lie aux bibliothèques middleware propriétaires de Sophon.
**Spécificité chinoise :** Hébergé par Sophgo (算能), une entreprise chinoise de conception de puces IA qui fabrique l'accélérateur TPU Sophon BM1684. Le bootloader est spécifique à l'écosystème SoC de Sophgo et s'intègre avec leur firmware propriétaire et leur pile middleware, qui ne sont pas disponibles dans les projets open-source occidentaux.
**Équivalent occidental :** U-Boot (DENX), Arm Trusted Firmware (Arm), Barebox — mais aucun ne cible les puces Sophon ; il s'agit d'un BSP spécifique au fournisseur pour un SoC accélérateur chinois.
**Maturité :** Actif (★ 12, 26 forks, mis à jour 2026-06)
**Langue :** Anglais
**GitHub :** https://github.com/sophgo/bootloader-arm64
---
