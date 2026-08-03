---
## paddlepaddle/PaddleOCR [MODIFIÉ]
**Type :** Library
**Domaine :** Embarqué
**Score de pertinence :** 71/100
**Problème résolu :** Convertir des documents PDF et des images en données structurées prêtes pour les LLM (JSON/Markdown) avec une haute précision. Fournir une reconnaissance optique de caractères multilingue (100+ langues) et une analyse de la mise en page des documents pour les applications RAG et IA agentive sans dépendre de solutions commerciales propriétaires.
**Comment ça marche :** PaddleOCR comprend trois composants principaux : PP-OCRv6 (moteur de détection et reconnaissance de texte supportant 50 langues dans un modèle unifié), PaddleOCR-VL-1.6 (modèle vision-langage léger de 0,9B pour l'analyse de documents atteignant 96,3% de précision sur OmniDocBench), et PP-StructureV3 (convertisseur PDF/image-vers-Markdown/JSON conscient de la structure avec extraction de coordonnées fine). Construit sur le framework d'apprentissage profond PaddlePaddle (Python/C++), il supporte l'inférence sur GPU NVIDIA, CPU Intel, XPU Kunlunxin et autres accélérateurs IA. Les formats de sortie incluent Markdown et JSON avec coordonnées des cellules de tableau et du texte.
**Spécificité chinoise :** Développé par l'équipe PaddlePaddle de Baidu ; PaddlePaddle est le framework d'apprentissage profond open-source de Baidu largement adopté dans l'écosystème IA chinois. L'intégration avec XPU Kunlunxin (accélérateur IA chinois) est explicitement supportée. Aucune conformité obligatoire aux normes chinoises citée.
**Équivalent occidental :** Tesseract (moteur OCR open-source), EasyOCR (bibliothèque Python), Docling (IBM, analyse de documents), PyMuPDF (extraction PDF)
**Maturité :** Stable (★ 4335, 1094 forks, mis à jour 2026-06)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/paddlepaddle/PaddleOCR
---
