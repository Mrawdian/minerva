---
## EspressifSystems/esp-iot-bridge [MODIFIÉ]
**Type :** Framework
**Domaine :** IoT
**Score de pertinence :** 79/100
**Problème résolu :** Permettre aux ESP32 et aux SoCs Espressif similaires de créer un pont entre plusieurs interfaces réseau (Wi-Fi, Ethernet, USB, SPI, SDIO) et d'agir comme passerelles réseau ou adaptateurs réseau sans fil/filaires, en supportant des cas d'usage tels que les routeurs Wi-Fi, les points d'accès cellulaires et l'émulation d'interface réseau pour PC et MCU.
**Comment ça marche :** La solution fournit un framework basé sur des composants (iot_bridge) qui abstrait la traduction de protocoles et le transfert de paquets entre des interfaces réseau hétérogènes. Elle inclut des implémentations de référence en C pour les scénarios courants : routeur Wi-Fi (pontage SoftAP), carte réseau sans fil (USB/ETH/SPI/SDIO vers carte réseau), carte réseau filaire (entrée Ethernet avec plusieurs interfaces de sortie), point d'accès 4G (module cellulaire vers Wi-Fi) et carte réseau 4G (cellulaire vers filaire/sans fil). Construite sur ESP-IDF (Espressif IoT Development Framework) et intégrée avec des composants optionnels comme Wi-Fi Mesh Lite et Rainmaker.
**Spécificité chinoise :** Hébergé sur Gitee/GitHub par EspressifSystems ; aucune spécificité chinoise particulière au-delà de l'auteur. Espressif Systems est un fournisseur de SoC basé à Shanghai ; ce projet est une implémentation de référence pour leur famille ESP32.
**Équivalent occidental :** OpenWrt (Linux Foundation, orientation routeur/passerelle), Home Assistant (pont réseau pour IoT), Tasmota (firmware ESP8266/ESP32 avec pontage réseau)
**Maturité :** Actif (★ 10, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**Gitee :** https://gitee.com/EspressifSystems/esp-iot-bridge
---
