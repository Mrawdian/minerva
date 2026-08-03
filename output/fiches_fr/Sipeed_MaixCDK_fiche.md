---
## Sipeed/MaixCDK
**Type :** Framework
**Domaine :** Edge AI
**Score de pertinence :** 63/100
**Problème résolu :** Fournir un SDK C/C++ unifié pour le développement rapide d'applications d'inférence IA, de vision par machine et d'IoT sur les cartes de la série Sipeed Maix et les plateformes Linux, éliminant le besoin d'intégrer des bibliothèques séparées pour l'accélération des réseaux de neurones, OpenCV et les E/S périphériques.
**Comment ça marche :** MaixCDK est une bibliothèque wrapper C/C++ qui abstrait l'exécution IA accélérée par matériel (classification, détection, segmentation), les algorithmes de vision (détection de couleur, reconnaissance QR/AprilTag, suivi de ligne), l'intégration OpenCV et les interfaces périphériques (UART, I2C, SPI, GPIO, PWM, ADC, caméra, affichage). Il cible les cartes Sipeed MaixCAM et MaixCAM-Pro (basées sur des SoC non spécifiés) et Linux générique. Le système de compilation utilise une compilation en un clic ; le débogage en ligne est pris en charge. Un homologue Python (MaixPy) maintient des API synchronisées.
**Spécificité chinoise :** Sipeed est un fournisseur chinois de systèmes embarqués spécialisé dans les cartes RISC-V et accélérateurs IA ; MaixCDK est leur framework de développement C/C++ principal pour la ligne de produits Maix. Le projet s'intègre avec MaixVision (IDE) et MaixHub (marketplace d'applications), formant un écosystème fermé autour du matériel Sipeed.
**Équivalent occidental :** OpenCV (vision par ordinateur), TensorFlow Lite (inférence), Arduino/mbed (abstraction périphérique), mais aucun projet occidental unique ne combine les trois avec l'accélération matérielle pour une famille de cartes spécifique.
**Maturité :** Actif (★ 1, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/Sipeed/MaixCDK
---
