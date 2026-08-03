---
## alibaba/sionnx
**Type :** Tool
**Domaine :** Edge AI
**Score de pertinence :** 64/100
**Problème résolu :** Automatiser la génération de tests de conformité ONNX pour valider l'implémentation des opérateurs dans les runtimes hétérogènes.
**Comment ça marche :** SIONNX utilise un DSL (Domain Specific Language) décrivant les instructions ONNX, traité par une chaîne LLVM TableGen personnalisée pour générer des tests unitaires en Python. Les tests générés peuvent être exportés au format protobuf pour compatibilité avec plusieurs frameworks ONNX runtime. Le système supporte des niveaux de profiling configurables (smoke tests vs tests complets) et permet l'ajout d'opérateurs via fichiers .td et algorithmes numpy.
**Spécificité chinoise :** Originaire de la plateforme Sinian d'Alibaba, une infrastructure d'accélération matérielle hétérogène optimisée pour l'inférence ML sur cloud, edge computing et appareils IoT chinois. Intégration directe avec l'écosystème d'optimisation de performance d'Alibaba pour applications d'IA et big data.
**Équivalent occidental :** ONNX Model Zoo test generation, ONNX Runtime test suite, mais sans approche DSL/TableGen équivalente
**Maturité :** Expérimental (★ 7, mis à jour 2024-11)
**Langue :** EN
**Gitee :** https://gitee.com/alibaba/sionnx
---
