---
## bouffalolab/toolchain_riscv_sifive_linux64
**Type :** Tool
**Domaine :** Embarqué
**Score de pertinence :** 32/100
**Problème résolu :** Fournir une chaîne d'outils GCC RISC-V ciblant Linux 64 bits sur les plateformes SiFive, permettant la compilation croisée pour les systèmes RISC-V sans dépendre de l'infrastructure de compilation propriétaire de SiFive.
**Comment ça marche :** Il s'agit d'une distribution de chaîne d'outils GCC RISC-V pré-compilée ou basée sur les sources, ciblant l'espace utilisateur Linux sur les systèmes 64 bits. Elle inclut binutils, GCC et probablement glibc ou musl pour la bibliothèque C. La chaîne d'outils s'exécute sur des hôtes Linux x86_64 et produit des binaires ELF RISC-V. Aucun composant d'exécution ou de noyau spécifique n'est fourni ; il s'agit uniquement d'une boîte à outils de compilation croisée.
**Spécificité chinoise :** Hébergé sur Gitee par Bouffalo Lab, une filiale de Nanjing Xiaoxin Semiconductor spécialisée dans les SoC RISC-V et sans fil. Cependant, ce dépôt particulier est une distribution générique de chaîne d'outils RISC-V/SiFive sans intégration de chipset spécifique à Bouffalo ni conformité aux normes chinoises évidente.
**Équivalent occidental :** SiFive Freedom Tools (distribution GCC officielle de SiFive), RISC-V GNU Toolchain (upstream RISC-V International)
**Maturité :** Expérimental (mis à jour 2025-08)
**Langue :** Anglais
**GitHub :** https://github.com/bouffalolab/toolchain_riscv_sifive_linux64
---
