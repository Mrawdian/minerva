---
## ByteDance/coap
**Type:** Framework
**Domain:** Edge AI
**Relevance score:** 54/100
**Problem solved:** Reduce memory consumption during training of large deep learning models without degrading final performance.
**How it works:** COAP uses correlation-based gradient projection to identify and eliminate redundant gradients during backpropagation. The method projects gradients into a low-rank subspace while accounting for correlations between parameters, thereby reducing computational overhead. The approach is validated on computer vision tasks, natural language processing, and multimodal models, demonstrating training acceleration with improved convergence.
**Chinese specificity:** Developed by ByteDance, a Chinese leader in mobile applications and AI, in collaboration with Rutgers University. Represents ByteDance's effort to optimize large-scale model training in a context of computational constraints.
**Western equivalent:** LoRA (Low-Rank Adaptation), QLoRA, and other memory-efficient fine-tuning methods (Hugging Face, Meta)
**Maturity:** Experimental (updated 2025-03)
**Language:** EN
**Gitee:** https://gitee.com/ByteDance/coap
---
