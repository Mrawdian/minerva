---
## sophgo/cvi_mpi
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 66/100
**Problème résolu :** Fournir des bibliothèques de codecs multimédias et de traitement d'images (encodage, décodage, pipeline ISP) pour la série SoC CV18xx, qui est une famille de processeurs de vision basse consommation utilisés dans les applications d'IA en périphérie et d'IoT.
**Comment ça marche :** Le projet expose une couche Media Processing Interface (MPI) écrite en C, encapsulant les codecs matériels et les blocs ISP sur les puces CV18xx. Il inclut l'encodage/décodage vidéo (H.264, H.265, JPEG), la mise à l'échelle d'images, la conversion d'espace colorimétrique et les pilotes d'interface capteur. Les dépendances incluent le micrologiciel propriétaire du SoC et le chargeur d'amorçage ; la bibliothèque est généralement liée aux applications s'exécutant sur le noyau Linux embarqué ou RTOS fourni par le fournisseur.
**Spécificité chinoise :** Sophgo est une entreprise chinoise de semi-conducteurs sans usine spécialisée dans les SoC d'IA en périphérie et de traitement vidéo. La série CV18xx est leur architecture propriétaire ; cette bibliothèque MPI est la couche d'abstraction multimédia officielle pour leurs puces, étroitement couplée à la conception matérielle et à l'écosystème micrologiciel de Sophgo.
**Équivalent occidental :** Qualcomm Snapdragon Heterogeneous Compute SDK (pour vidéo/ISP sur SoC mobiles), NVIDIA Tegra Multimedia API (pour encodage vidéo sur GPU embarqué), MediaTek NeuroPilot (pour SoC d'IA en périphérie avec support vidéo)
**Maturité :** Actif (★ 2, 7 forks, mis à jour 2026-06)
**Langue :** Anglais
**GitHub :** https://github.com/sophgo/cvi_mpi
---
