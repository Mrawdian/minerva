---
## alibaba/iot_remote_access
**Type :** Application
**Domaine :** IoT
**Score de pertinence :** 71/100
**Problème résolu :** Fournit un accès à distance sécurisé aux appareils IoT sans adresse IP publique, permettant le SSH, le shell web, l'accès aux fichiers et le tunneling réseau à travers Internet.
**Comment ça marche :** Le daemon côté appareil établit une connexion WebSocket persistante vers les serveurs Alibaba Cloud IoT pour créer un canal de communication bidirectionnel. L'architecture supporte le SSH distant, un shell web basé navigateur, la navigation de fichiers avec upload/download, et le tunneling RDP Windows via ce canal chiffré. Le système compile en binaires statiques ou dynamiques pour multiples architectures (x86_64, ARM v7, macOS) avec support de contrôle cloud pour activer/désactiver les canaux de maintenance.
**Spécificité chinoise :** Intégration native avec l'écosystème Alibaba Cloud IoT et Link IoT Edge, plateforme propriétaire chinoise de gestion IoT. Conçu pour les appareils déployés en Chine sans accès direct à Internet public, utilisant l'infrastructure cloud d'Alibaba comme point de relais central.
**Équivalent occidental :** Aucun équivalent direct connu - combine les fonctionnalités de ngrok/Cloudflare Tunnel avec un daemon IoT propriétaire, mais sans équivalent open-source occidental offrant cette intégration cloud complète pour IoT
**Maturité :** Expérimental (mis à jour 2024-11)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/alibaba/iot_remote_access
---
