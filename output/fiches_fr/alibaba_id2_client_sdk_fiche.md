---
## alibaba/id2_client_sdk
**Type :** Library
**Domaine :** Edge AI
**Score de pertinence :** 67/100
**Problème résolu :** Fournir une identité numérique inviolable et non-contrefaçable pour les appareils IoT, garantissant l'authentification et l'intégrité dans les écosystèmes connectés.
**Comment ça marche :** Le SDK client ID² implémente une couche d'abstraction matérielle (HAL) pour l'intégration cryptographique et supporte quatre types de porteurs de sécurité : Demo (démonstration), SE (puce de sécurité externe), PUF (fonction physiquement non-clonnable) et MDU (module de sécurité). L'architecture modulaire sépare les interfaces de chiffrement/déchiffrement, les spécifications de protocole, et les modules dépendants pour permettre l'adaptation à différentes plateformes matérielles. La compilation croisée est configurée via des fichiers make.rules et make.settings pour supporter plusieurs chaînes d'outils et environnements cibles.
**Spécificité chinoise :** ID² est une infrastructure de confiance développée par Alibaba pour l'écosystème IoT chinois fragmenté, intégrant des standards de sécurité adaptés aux contraintes de coût et de consommation énergétique des appareils connectés. Le projet s'aligne avec les initiatives chinoises de souveraineté technologique en matière d'identité numérique pour l'Internet des Objets.
**Équivalent occidental :** Aucun équivalent direct connu - les solutions occidentales (TPM, DICE de Microsoft, ARM TrustZone) ne proposent pas d'infrastructure d'identité unifiée comparable
**Maturité :** Expérimental (mis à jour 2024-10)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/alibaba/id2_client_sdk
---
