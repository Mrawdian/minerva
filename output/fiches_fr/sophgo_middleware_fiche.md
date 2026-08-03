---
## sophgo/middleware
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 62/100
**Problème résolu :** Fournir des bibliothèques de codecs multimédias et de traitement d'images pour le SoC série CV18xx (processeurs CVITEK/SOPHGO), permettant l'encodage/décodage vidéo, la mise à l'échelle d'images et la conversion d'espace colorimétrique sans dépendre uniquement des implémentations propriétaires fermées du fournisseur.
**Comment ça marche :** La pile middleware inclut des bibliothèques de codecs vidéo (H.264, H.265, JPEG), des modules de traitement d'images (ISP, scaler, conversion colorimétrique) et la prise en charge des codecs audio. Écrite principalement en C avec des couches d'abstraction matérielle pour la famille de SoC CV18xx. Les dépendances incluent les pilotes noyau et les composants de bootloader spécifiques à la plateforme CVITEK/SOPHGO. Cible les déploiements Linux embarqué sur CV1800, CV1812 et variantes connexes.
**Spécificité chinoise :** SOPHGO (anciennement CVITEK) est une fabless chinoise spécialisée dans les SoC d'IA embarquée et multimédias. Ce middleware est la bibliothèque de support officielle pour la famille de processeurs CV18xx, largement utilisée dans les applications chinoises d'IoT, de surveillance et de robotique.
**Équivalent occidental :** FFmpeg (codecs multimédias), GStreamer (framework multimédia), libx264/libx265 (encodage vidéo) — bien que ceux-ci soient génériques ; aucun équivalent direct pour l'accélération matérielle spécifique à CV18xx.
**Maturité :** Actif (★ 6, 13 forks, mis à jour 2026-04)
**Langue :** Anglais
**GitHub :** https://github.com/sophgo/middleware
---
