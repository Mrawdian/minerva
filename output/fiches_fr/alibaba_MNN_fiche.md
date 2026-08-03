---
## alibaba/MNN [MODIFIÉ]
**Type :** Framework
**Domaine :** Edge AI
**Score de pertinence :** 76/100
**Problème résolu :** Déployer des modèles d'apprentissage profond (LLM, modèles de diffusion, modèles de vision) pour l'inférence sur appareil sur mobile, IoT et systèmes embarqués avec latence minimale et empreinte mémoire réduite, en évitant la dépendance au cloud.
**Comment ça marche :** MNN est un moteur d'inférence C++ avec architecture de backend modulaire supportant CPU (ARM, x86), GPU (Metal, OpenGL, Vulkan) et accélérateurs spécialisés (Qualcomm Hexagon DSP à partir de v3.6.1). Les composants principaux incluent un convertisseur de modèle (supportant les formats ONNX, TensorFlow, PyTorch), des outils de quantification (INT8, FP16) et des couches d'exécution pour Android, iOS, Linux et Windows. MNN-LLM encapsule le moteur pour le déploiement de modèles transformateurs ; MNN-Diffusion gère l'inférence de diffusion stable. Les dépendances incluent des bibliothèques ML standard ; aucun verrouillage propriétaire de fournisseur n'est signalé.
**Spécificité chinoise :** Développé et maintenu par Alibaba ; intégré dans 30+ applications Alibaba (Taobao, Tmall, Youku, DingTalk) couvrant 70+ scénarios de production. Supporte Qwen (série LLM d'Alibaba) et autres modèles LLM chinois (Baichuan, Zhipu). Le système Walle (OSDI'22) utilise MNN comme module d'inférence principal pour l'apprentissage automatique collaboratif appareil-cloud dans l'infrastructure de production d'Alibaba.
**Équivalent occidental :** TensorFlow Lite (Google), PyTorch Mobile (Meta), NCNN (Tencent, également chinois mais projet distinct), TVM (Apache)
**Maturité :** Actif (★ 7, 4 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/alibaba/MNN
---
