---
## unitreerobotics/televuer
**Type:** Library
**Domain:** Robotics
**Relevance score:** 67/100
**Problem solved:** Enable teleoperation of Unitree robots from XR headsets (Apple Vision Pro, Meta Quest 3, Pico 4) by providing hand/controller tracking input and first-person view streaming with multiple display modes (immersive, pass-through, ego).
**How it works:** TeleVuer is a Python wrapper around the Vuer library that abstracts XR device APIs and robot state/command interfaces. It handles image transport via ZMQ or WebRTC, exposes hand/controller pose data through a unified TeleData structure, and manages three display modes by controlling image plane rendering. Dependencies include Vuer (core XR framework), teleimager (image capture), and optional WebRTC/ZMQ backends; it integrates with the xr_teleoperate library for full teleoperation workflows.
**Chinese specificity:** Hosted on GitHub by unitreerobotics (Unitree Robotics, a Chinese quadruped/humanoid robot manufacturer); no particular Chinese chipset or standard specificity beyond the author's commercial robotics platform.
**Western equivalent:** No known direct equivalent — specific combination of XR device abstraction layer (Vuer) with robot teleoperation middleware for hand/controller tracking and streaming video.
**Maturity:** Active (★ 46, 33 forks, updated 2026-05)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/televuer
---
