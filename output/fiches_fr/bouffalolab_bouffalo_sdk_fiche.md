---
## bouffalolab/bouffalo_sdk
**Type :** Board Support Package
**Domaine :** Embarqué
**Score de pertinence :** 76/100
**Problème résolu :** Fournir un SDK unifié supportant l'ensemble de la gamme de microcontrôleurs Bouffalo (BL602, BL702/L, BL616, BL618) avec une API HAL commune (LHAL) pour éviter la fragmentation entre bl_mcu_sdk et bl_iot_sdk antérieurs. Cela permet aux développeurs d'utiliser une seule base de code pour des périphériques variés (ADC, SPI, UART, cryptographie, caméra, Ethernet) sans réécrire les drivers.
**Comment ça marche :** Architecture modulaire en C avec couches : BSP (clock, pinmux, heap, console), drivers LHAL (périphériques génériques supportant tous les chips), drivers SOC (périphériques spécifiques), composants (stacks réseau, sécurité), et exemples. Support de périphériques : UART, SPI, I2C, I2S, GPIO, ADC, DAC, DMA, FLASH, RTC, timers, AES/SHA/TRNG/PKA, caméra (CAM), MJPEG (BL616/618), Ethernet (EMAC). Inclut tests unitaires et outils de build.
**Spécificité chinoise :** Bouffalo Lab est le fabricant des chipsets Bouffalo (BL602, BL702, BL616, BL618) ; ce SDK est le kit de développement officiel pour cette gamme propriétaire chinoise. Pas d'intégration spécifique à des services cloud chinois (WeChat, Alipay, Baidu) détectée dans le README.
**Équivalent occidental :** Zephyr Project (Linux Foundation, multi-vendor), FreeRTOS + HAL vendor-spécifique (Amazon/Texas Instruments), STM32CubeSDK (STMicroelectronics)
**Maturité :** Actif (★ 486, 178 forks, mis à jour 2026-07)
**Langue :** Bilingue CN-EN
**GitHub :** https://github.com/bouffalolab/bouffalo_sdk
---
