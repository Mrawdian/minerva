---
## Sipeed/MaixPy
**Type :** Framework
**Domaine :** Edge AI
**Score de pertinence :** 63/100
**Problème résolu :** Fournir un framework de développement basé sur Python pour l'inférence d'IA edge en vision et audio sur des systèmes embarqués à ressources limitées (série MaixCAM), éliminant le besoin d'écrire du C/C++ bas niveau pour les tâches courantes comme la capture caméra, l'inférence de réseau de neurones et les E/S périphériques.
**Comment ça marche :** MaixPy est une couche de liaison Python enveloppant le SDK C/C++ pour le matériel MaixCAM de Sipeed (basé sur SG200 ou SoC similaire). Les modules principaux incluent `maix.camera` (capture vidéo), `maix.nn` (inférence de modèle via NPU embarqué), `maix.display` (sortie framebuffer), `maix.uart` et autres périphériques. Les modèles sont empaquetés au format `.mud`. Le framework inclut également l'IDE MaixVision (station de travail de bureau pour le débogage en direct) et MaixHub (service cloud de formation et conversion de modèles). Supporte à la fois les scripts Python et le SDK C/C++ avec des API identiques.
**Spécificité chinoise :** Sipeed est une entreprise chinoise de conception de semi-conducteurs spécialisée dans les SoC RISC-V et IA edge. Le matériel MaixCAM intègre le processeur SG200 propriétaire de Sipeed ou un silicium propriétaire similaire. La plateforme MaixHub fournit une formation et quantification de modèles IA gratuites basées sur le cloud, réduisant la dépendance aux fournisseurs cloud externes pour la préparation des modèles.
**Équivalent occidental :** OpenMV (STM32H7 + MicroPython), TensorFlow Lite for Microcontrollers, MediaPipe (Google), PyTorch Mobile
**Maturité :** Actif (★ 2, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/Sipeed/MaixPy
---
