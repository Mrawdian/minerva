---
## alibaba/alibaba-rsocket-broker
**Type :** Framework
**Domaine :** Embarqué
**Score de pertinence :** 62/100
**Problème résolu :** Fournir un système de communication réactive pair-à-pair basé sur RSocket pour les architectures distribuées (RPC, Pub/Sub, Streaming) sans gestion explicite de threads et avec support du backpressure.
**Comment ça marche :** Le broker implémente le protocole RSocket pour établir des connexions bidirectionnelles asynchrones entre clients et serveurs. Il utilise un plan de contrôle (Control Plane) pour orchestrer les communications, supporter la découverte de services et gérer les métriques Prometheus. L'architecture réactive élimine les modèles de threads bloquants et adapte les flux de données aux capacités du récepteur via le backpressure.
**Spécificité chinoise :** Projet Alibaba intégrant les besoins d'infrastructure cloud chinoise (environnements multi-cloud et cross-cloud). Le projet est archivé depuis juillet 2024 au profit du fork communautaire reactive-rsocket-broker.
**Équivalent occidental :** Spring Cloud Stream, Vert.x, Akka, gRPC avec streaming bidirectionnel
**Maturité :** Expérimental (mis à jour 2024-10)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/alibaba/alibaba-rsocket-broker
---
