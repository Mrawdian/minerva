---
## Tencent/ncnn [MODIFIÉ]
**Type :** Library
**Domaine :** Edge AI
**Score de pertinence :** 90/100
**Problème résolu :** Déployer des modèles d'apprentissage profond (PyTorch, ONNX) sur des appareils mobiles, embarqués et périphériques avec une surcharge d'exécution minimale et une latence d'inférence optimisée. Élimine la dépendance envers les frameworks lourds comme TensorFlow Lite ou CoreML en fournissant un moteur d'inférence C++ autonome avec accélération GPU ARM NEON et Vulkan.
**Comment ça marche :** ncnn est un framework d'inférence C++ avec une liaison Python et une API C. Les composants principaux incluent un chargeur de modèle pour les fichiers au format `.param` et `.bin`, un moteur d'exécution CPU avec optimisations ARM NEON et planification multi-cœur, un backend GPU Vulkan optionnel, et l'outil pnnx pour convertir les modèles PyTorch et ONNX. Supporte le stockage fp16, la quantification int8 et l'enregistrement de couches personnalisées. Aucune dépendance externe BLAS, NNPACK ou runtime ; chargement de modèle avec mappage mémoire direct.
**Spécificité chinoise :** Développé par le Youtu Lab de Tencent et déployé en production dans les applications Tencent (WeChat, QQ, Qzone, Pitu). Aucune intégration documentée avec les plateformes cloud chinoises ou les fournisseurs de chipsets ; la spécificité est principalement organisationnelle plutôt que basée sur l'écosystème.
**Équivalent occidental :** TensorFlow Lite (Google), ONNX Runtime (Microsoft/Linux Foundation), CoreML (Apple)
**Maturité :** Actif (★ 303, 3 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/Tencent/ncnn
---
