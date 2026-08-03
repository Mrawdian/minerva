---
## unitreerobotics/unitree_lerobot
**Type:** Framework
**Domain:** Edge AI
**Relevance score:** 77/100
**Problem solved:** Enable training and deployment of imitation learning policies on Unitree G1 dual-arm robots using the LeRobot framework, with data conversion utilities for proprietary Unitree hand formats (Dex1, Dex3, BrainCo, Inspire1) into LeRobot-compatible datasets.
**How it works:** The project wraps the LeRobot training framework (commit 0878c68) with Unitree-specific extensions: a `utils` module for dataset conversion from Unitree robots to LeRobot v3.0 format, an `eval_robot` module for real-world inference validation via unitree_sdk2_python (DDS-based communication), and support for multiple policy architectures (PI05, GROOT). Dependencies include PyTorch, LeRobot core, and unitree_sdk2_python for robot control; primary languages are Python and YAML for configuration.
**Chinese specificity:** Unitree Robotics is a Chinese robotics manufacturer specializing in quadruped and humanoid platforms; this project directly integrates their proprietary G1 robot hardware and dexterous hand variants (Dex1, Dex3) with the open-source LeRobot framework, enabling Chinese roboticists to leverage imitation learning on Unitree platforms.
**Western equivalent:** LeRobot (Hugging Face), Mobile ALOHA (Stanford), Diffusion Policy (UC Berkeley) — all imitation learning frameworks, but unitree_lerobot is a hardware-specific adapter rather than a standalone policy architecture.
**Maturity:** Stable (★ 728, 133 forks, updated 2026-05)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/unitreerobotics/unitree_lerobot
---
