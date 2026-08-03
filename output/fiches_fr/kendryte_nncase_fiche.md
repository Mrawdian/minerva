---
## kendryte/nncase
**Type :** Tool
**Domaine :** Edge AI
**Score de pertinence :** 82/100
**Problème résolu :** Compiler des modèles de réseaux de neurones (TensorFlow, ONNX, etc.) vers du code optimisé pour les accélérateurs IA Kendryte (K210, K510, K230), en gérant la quantification et la planification des opérations sur les unités de calcul spécialisées (KPU).
**Comment ça marche :** nncase est un compilateur neural network écrit en C++ qui prend en entrée des modèles au format ONNX ou TensorFlow, applique des passes d'optimisation (fusion d'opérateurs, quantification post-training), et génère du bytecode exécutable sur le KPU (Kendryte Processing Unit). Le runtime Python (pip install nncase nncase-kpu) expose une API de compilation et d'inférence. Les cibles supportées sont K210, K510 et K230 ; la compilation s'effectue via CMake (Ninja ou make) sur Linux/Windows, avec intégration au K230_SDK pour le déploiement embarqué.
**Spécificité chinoise :** Développé par Canaan Creative (créateur du chipset Kendryte), ce compilateur est l'outil officiel de déploiement pour la gamme K2xx. L'écosystème inclut des ressources Canaan (modèles pré-entraînés, images SDK, tutoriels Bilibili) et une intégration native avec le K230_SDK et Canmv (MicroPython pour Kendryte).
**Équivalent occidental :** TVM (Apache), ONNX Runtime (Microsoft), TensorFlow Lite Converter (Google) — mais aucun n'est spécialisé pour les accélérateurs Kendryte ; nncase combine compilation + quantification + planification KPU-spécifique.
**Maturité :** Stable (★ 898, 209 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/kendryte/nncase
---
