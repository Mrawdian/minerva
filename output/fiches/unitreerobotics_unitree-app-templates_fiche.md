---
## unitreerobotics/unitree-app-templates
**Type:** Application
**Domain:** Robotics
**Relevance score:** 59/100
**Problem solved:** Provide a standardized template and packaging framework for developers to build and deploy applications on Unitree quadruped robots (G1, etc.) without reimplementing deployment infrastructure. Abstracts robot control APIs and Docker-based app distribution.
**How it works:** Monorepo structure with example projects (G1 Mimic Learning Demo) written in C++ for control logic and Python for service layers. Applications are containerized via Docker and must expose an HTTP service on port 80, with metadata defined in YAML. Developers package binaries/scripts into an `app/` folder and upload to UniStore. The G1 example demonstrates imitation learning policies for motion control using Unitree's proprietary SDK.
**Chinese specificity:** Unitree Robotics is a Chinese quadruped robot manufacturer; this repository serves as the official app distribution template for their robot platform. No integration with Chinese cloud services (Baidu, Aliyun, WeChat) is documented; the specificity is primarily the parent organization's role in the Chinese robotics industry.
**Western equivalent:** Boston Dynamics Spot SDK (proprietary), ANYmal ROS2 integration (ANYbotics), Clearpath Robotics Warthog/Husky app frameworks
**Maturity:** Active (★ 16, 5 forks, updated 2026-06)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree-app-templates
---
