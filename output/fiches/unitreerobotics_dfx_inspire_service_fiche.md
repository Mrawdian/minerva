---
## unitreerobotics/dfx_inspire_service
**Type:** Application
**Domain:** Edge AI
**Relevance score:** 57/100
**Problem solved:** Provides a controller interface for the Unitree RH56DFX Inspire dexterous hand (12 motors across both hands) over serial connection, translating high-level motor command messages (MotorCmds_) into low-level hardware control and exposing motor state feedback (MotorStates_) via DDS middleware.
**How it works:** C++ application built on top of unitree_sdk2, using Cyclone DDS for inter-process communication over topics (rt/inspire/cmd for commands, rt/inspire/state for telemetry). Depends on Boost and spdlog libraries. Communicates with H1 or G1 robot platforms via serial port (/dev/ttyUSB*), serializing/deserializing IDL-defined message structures (MotorCmds_, MotorStates_) using xcdr_v2 encoding from Eclipse Cyclone DDS.
**Chinese specificity:** Hosted on GitHub by unitreerobotics; no particular Chinese specificity beyond the author. Unitree Robotics is a Chinese robotics company, but this project is a standard controller interface without ties to Chinese chipset vendors, standards, or cloud platforms.
**Western equivalent:** No known direct equivalent — specific combination of Unitree SDK integration, DDS-based middleware, and dexterous hand motor control.
**Maturity:** Experimental (★ 50, 15 forks, updated 2025-09)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/dfx_inspire_service
---
