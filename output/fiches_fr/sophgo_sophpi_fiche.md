---
## sophgo/sophpi
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 64/100
**Problème résolu :** Fournir un SDK open-source et un BSP pour les SoCs des séries CV18xx et SG200x (processeurs de vision par ordinateur de SOPHGO), permettant le développement de firmware, le portage du noyau, l'intégration de pilotes capteurs/panneaux et l'inférence IA en périphérie sans dépendre de chaînes d'outils propriétaires.
**Comment ça marche :** Le projet est un SDK de style monorepo combinant le noyau Linux (5.10), le chargeur d'amorçage U-Boot, l'option RTOS RT-Thread, les pilotes de périphériques (capteurs : GC2053, GC2093, GC4683, SC535HAI, etc. ; panneaux : MS7024, GC9307, ST7789P3 ; stockage : SPI-NOR, SPI-NAND, eMMC), le système de compilation (basé sur defconfig) et le SDK TDL (framework d'inférence de SOPHGO avec support YOLO v8/v11, détection de visages, support LLM). Langages : C, scripts shell. Les dépendances incluent les chaînes d'outils musl/glibc, OpenSBI et le firmware DDR/FSBL spécifique au fournisseur. Cible les variantes CV180x, CV181x, CV1812, CV1815, CV1842, SG200x avec différentes configurations de stockage et de mémoire.
**Spécificité chinoise :** SOPHGO est une fabless chinoise spécialisée dans les SoCs IA en périphérie et vision par ordinateur ; ce SDK est la plateforme de développement open-source officielle pour leur gamme de produits CV18xx/SG200x. Le projet intègre le SDK TDL (Tensor Deep Learning) propriétaire de SOPHGO et supporte les composants de l'écosystème chinois (chipset WiFi AIC8800, pilotes écran tactile GT9xx, DNSMASQ pour les passerelles IoT).
**Équivalent occidental :** Yocto/OpenEmbedded (framework BSP Linux générique), Buildroot (système de compilation Linux embarqué), Zephyr (alternative RTOS), NXP i.MX SDK (BSP SoC spécifique au fournisseur)
**Maturité :** Actif (★ 59, 35 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/sophgo/sophpi
---
