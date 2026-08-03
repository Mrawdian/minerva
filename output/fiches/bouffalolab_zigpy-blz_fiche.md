---
## bouffalolab/zigpy-blz
**Type:** Library
**Domain:** IoT
**Relevance score:** 51/100
**Problem solved:** Enable Bouffalo Lab Zigbee (BLZ) radio hardware to integrate with zigpy, the open-source Python Zigbee stack, allowing users to control Zigbee devices through Home Assistant ZHA without proprietary vendor software.
**How it works:** zigpy-blz is a Python library that implements the Bouffalo Zigbee Serial Protocol (BZSP) to communicate with BLZ radio modules. It acts as a radio driver layer within the zigpy framework, translating zigpy's generic Zigbee commands into BZSP messages over serial. The library depends on zigpy (core stack), pyserial (serial communication), and asyncio for asynchronous I/O. It supports Bouffalo Lab's BLZ radio hardware and integrates with Home Assistant's ZHA component via a custom integration wrapper.
**Chinese specificity:** Hosted on GitHub by bouffalolab (Bouffalo Lab, a Chinese semiconductor company). The project provides driver support for Bouffalo Lab's proprietary BLZ Zigbee radio chipsets, which are manufactured and sold by the parent organization as part of their IoT connectivity portfolio.
**Western equivalent:** zigpy-xbee (Digi XBee radio support), zigpy-deconz (ConBee/RaspBee radio support), zigpy-znp (Texas Instruments Z-Stack radio support)
**Maturity:** Active (★ 9, 5 forks, updated 2026-06)
**Language:** English
**GitHub:** https://github.com/bouffalolab/zigpy-blz
---
