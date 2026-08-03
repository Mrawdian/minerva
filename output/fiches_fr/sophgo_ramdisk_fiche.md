---
## sophgo/ramdisk
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 47/100
**Problème résolu :** Générer des images de système de fichiers racine et des binaires d'arborescence de périphériques (ITB) pour la série de SoC CV18xx, avec support des superpositions de fichiers indépendantes de la plateforme et spécifiques à la plateforme lors de la compilation.
**Comment ça marche :** Le projet organise les composants rootfs en prebuild (en-têtes et bibliothèques de compilation croisée), target (répertoires communs et de superposition fusionnés au moment de la compilation), tools (scripts pour la génération d'ITB) et configs (listes de fichiers txt et fichiers source d'arborescence de périphériques ITS). Le processus de compilation fusionne les fichiers de superposition dans la base commune, puis génère les artefacts finaux rootfs et ITB. Écrit en scripts shell/build ; dépend du compilateur d'arborescence de périphériques et de la chaîne d'outils de compilation croisée.
**Spécificité chinoise :** Sophgo est une entreprise chinoise de semi-conducteurs spécialisée dans les accélérateurs d'IA et les SoC ; CV18xx est leur série propriétaire de processeurs embarqués. Ce projet est la configuration rootfs officielle pour la plateforme CV18xx de Sophgo.
**Équivalent occidental :** Buildroot (Linux Foundation), Yocto Project (Linux Foundation) — tous deux fournissent des mécanismes de génération de rootfs et de superposition pour les systèmes Linux embarqués.
**Maturité :** Actif (★ 1, 12 forks, mis à jour 2026-06)
**Langue :** Anglais
**GitHub :** https://github.com/sophgo/ramdisk
---
