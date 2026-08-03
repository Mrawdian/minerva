---
## sophgo/vllm-tpu
**Type :** Framework
**Domaine :** Embarqué
**Score de pertinence :** 57/100
**Problème résolu :** Activer l'inférence de grands modèles de langage (LLaMa, Qwen, DeepSeek) sur les accélérateurs Sophon TPU SG2260 en portant vLLM v0.11.0 pour supporter les chemins d'exécution spécifiques aux TPU, les formats de quantification (w4a16, FP8, BF16) et les topologies multi-puces.
**Comment ça marche :** Fork de vLLM v0.11.0 avec intégration du backend TPU pour le matériel Sophon SG2260. Supporte l'inférence de modèles en modes Cmodel (émulé CPU) et Device (TPU natif) via conteneurs Docker. Inclut le paquet wheel Torch-TPU pour les opérations tensorielles, la pile runtime/driver tpuv7 (v1.1.3) et le cache de réorganisation des poids pour les modèles quantifiés. Testé sur les familles de modèles Llama2/3.1, Qwen2/2.5, QwQ, LLaVa et DeepSeek avec quantification FP16, BF16, FP8 et w4a16.
**Spécificité chinoise :** Sophgo est une entreprise chinoise de semi-conducteurs spécialisée dans les accélérateurs IA ; le SG2260 est leur gamme de produits TPU. Le projet s'intègre à l'écosystème propriétaire runtime tpuv7 et driver de Sophgo. Les poids de modèles proviennent de plateformes chinoises (ModelScope, Gitee AI) ainsi que de HuggingFace.
**Équivalent occidental :** vLLM (Meta/communauté LLM), TensorRT-LLM (NVIDIA), Ollama (inférence locale), MLX (Apple Silicon)
**Maturité :** Expérimental (★ 6, 1 forks, mis à jour 2025-12)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/vllm-tpu
---
