---
## bouffalolab/zigpy-blz
**Type :** Library
**Domaine :** IoT
**Score de pertinence :** 51/100
**Problème résolu :** Permettre au matériel radio Zigbee Bouffalo Lab (BLZ) de s'intégrer à zigpy, la pile Zigbee Python open-source, permettant aux utilisateurs de contrôler les appareils Zigbee via Home Assistant ZHA sans logiciel propriétaire du fournisseur.
**Comment ça marche :** zigpy-blz est une bibliothèque Python qui implémente le protocole série Zigbee Bouffalo (BZSP) pour communiquer avec les modules radio BLZ. Elle agit comme une couche de pilote radio dans le framework zigpy, traduisant les commandes Zigbee génériques de zigpy en messages BZSP sur port série. La bibliothèque dépend de zigpy (pile principale), pyserial (communication série) et asyncio pour les E/S asynchrones. Elle supporte le matériel radio BLZ de Bouffalo Lab et s'intègre au composant ZHA de Home Assistant via un wrapper d'intégration personnalisé.
**Spécificité chinoise :** Hébergé sur GitHub par bouffalolab (Bouffalo Lab, une entreprise chinoise de semi-conducteurs). Le projet fournit un support de pilote pour les chipsets radio Zigbee BLZ propriétaires de Bouffalo Lab, qui sont fabriqués et vendus par l'organisation mère dans le cadre de leur portefeuille de connectivité IoT.
**Équivalent occidental :** zigpy-xbee (support radio Digi XBee), zigpy-deconz (support radio ConBee/RaspBee), zigpy-znp (support radio Texas Instruments Z-Stack)
**Maturité :** Actif (★ 9, 5 forks, mis à jour 2026-06)
**Langue :** Anglais
**GitHub :** https://github.com/bouffalolab/zigpy-blz
---
