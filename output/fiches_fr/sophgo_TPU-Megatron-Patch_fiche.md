---
## sophgo/TPU-Megatron-Patch
**Type :** Framework
**Domaine :** Embarqué
**Score de pertinence :** 54/100
**Problème résolu :** Adapter le framework d'entraînement distribué Megatron pour s'exécuter sur les accélérateurs TPU SOPHGO pour l'entraînement de modèles de langage volumineux (LLM) et de modèles de langage visuel (VLM), en remplaçant les pipelines d'entraînement centrés sur GPU par un entraînement distribué optimisé pour TPU.
**Comment ça marche :** TPU-Megatron-Patch étend le framework Megatron-LM (conçu à l'origine pour les GPU NVIDIA) pour supporter le matériel TPU SOPHGO via la couche de liaison torch_tpu. La boîte à outils est écrite en Python et s'intègre avec PyTorch, fournissant des utilitaires d'entraînement distribué pour le parallélisme de modèle et le parallélisme de données. Le support actuellement documenté inclut le fine-tuning de Qwen2-7B ; la base de code est dérivée de Pai-Megatron-Patch d'Alibaba et ajoute des optimisations spécifiques à TPU et l'intégration du pilote de périphérique.
**Spécificité chinoise :** Maintenu par SOPHGO, une entreprise chinoise de semi-conducteurs spécialisée dans les accélérateurs d'IA et la conception de TPU. Le projet cible directement la gamme de produits TPU de SOPHGO et s'intègre à l'écosystème d'entraînement d'IA chinois, bien qu'il ne fasse référence à aucune norme chinoise spécifique ni à des plateformes cloud.
**Équivalent occidental :** Megatron-LM (NVIDIA), DeepSpeed (Microsoft), Hugging Face Transformers avec des backends d'entraînement distribué
**Maturité :** Expérimental (mis à jour 2024-12)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/TPU-Megatron-Patch
---
