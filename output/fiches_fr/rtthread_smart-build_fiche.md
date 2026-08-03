---
## rtthread/smart-build
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 71/100
**Problème résolu :** Automatiser la compilation croisée du noyau RT-Thread, du rootfs (busybox) et du bootloader pour cibles ARM (qemuarm64, etc.) via une chaîne Bitbake/OpenEmbedded, en évitant la configuration manuelle répétitive des toolchains et des étapes de build.
**Comment ça marche :** Smart-build est une couche (layer) OpenEmbedded/Bitbake qui orchestre la compilation via des recettes Bitbake. Le flux télécharge smart-gcc (toolchain croisé), compile busybox en rootfs ext4, puis compile le noyau RT-Thread en rtthread.bin. Les dépendances incluent openembedded-core, bitbake, Python 3 (scons, kconfiglib, tqdm), et des outils hôte (bison, flex, cpio, qemu-system-arm). Les cibles supportées incluent qemuarm64 et d'autres architectures ARM via la variable MACHINE.
**Spécificité chinoise :** Hébergé sur Gitee par rtthread (RT-Thread Microsystems, éditeur chinois du RTOS RT-Thread) ; pas de spécificité chinoise particulière au-delà de l'auteur — aucun chipset vendor chinois cité, aucune intégration d'écosystème local détectée.
**Équivalent occidental :** Yocto Project (Linux Foundation), Buildroot, OpenWrt (pour systèmes embarqués Linux)
**Maturité :** Expérimental (mis à jour 2025-08)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/rtthread/smart-build
---
