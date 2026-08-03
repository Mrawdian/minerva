---
## ByteDance/coap
**Type :** Framework
**Domaine :** Edge AI
**Score de pertinence :** 54/100
**Problème résolu :** Réduire la consommation mémoire lors de l'entraînement de grands modèles de deep learning sans dégrader les performances finales.
**Comment ça marche :** COAP utilise une projection de gradient basée sur la corrélation pour identifier et éliminer les gradients redondants lors de la rétropropagation. La méthode projette les gradients dans un sous-espace de faible rang en tenant compte des corrélations entre les paramètres, réduisant ainsi l'overhead computationnel. L'approche est validée sur des tâches de vision par ordinateur, traitement du langage naturel et modèles multimodaux, démontrant une accélération de l'entraînement avec convergence améliorée.
**Spécificité chinoise :** Développé par ByteDance, leader chinois des applications mobiles et de l'IA, en collaboration avec Rutgers University. Représente l'effort de ByteDance pour optimiser l'entraînement de modèles à grande échelle dans un contexte de contraintes computationnelles.
**Équivalent occidental :** LoRA (Low-Rank Adaptation), QLoRA, et autres méthodes de fine-tuning efficace en mémoire (Hugging Face, Meta)
**Maturité :** Expérimental (mis à jour 2025-03)
**Langue :** EN
**Gitee :** https://gitee.com/ByteDance/coap
---
