---
## unitreerobotics/unitree_mujoco
**Type:** Tool
**Domain:** Robotics / Edge AI
**Relevance score:** 70/100
**Problem solved:** Enable seamless sim-to-real transfer of control programs written for Unitree quadruped robots (Go2, B2, H1, G1, etc.) by providing a MuJoCo-based simulator that natively speaks the Unitree SDK2 message protocol (LowCmd, LowState, SportModeState, IMUState) without requiring code rewrites.
**How it works:** The simulator wraps MuJoCo physics engine with Unitree SDK2 bindings in C++ (primary) and Python variants. It accepts low-level motor commands (LowCmd) and returns motor state (LowState) and IMU/odometry data (SportModeState, IMUState) via DDS-based message types (unitree_go IDL for Go2/B2/H1, unitree_hg IDL for G1/H1-2). Robot morphologies are defined in MJCF format; a terrain generation tool is included. Dependencies: libyaml-cpp, libspdlog, libboost, libglfw3, MuJoCo 3.3.6+, unitree_sdk2.
**Chinese specificity:** Hosted on Gitee/GitHub by unitreerobotics; no particular Chinese specificity beyond the author. Unitree Robotics is a Chinese quadruped robotics manufacturer, but the simulator uses open-source Western tools (MuJoCo by DeepMind, standard DDS) with no vendor-specific chipset or compliance tie.
**Western equivalent:** Gazebo (Open Robotics) with custom Unitree plugin, Isaac Sim (NVIDIA) with robot-specific adapters, CoppeliaSim with Unitree SDK bindings — but none offer native, out-of-box Unitree SDK2 message compatibility.
**Maturity:** Stable (★ 1111, 378 forks, updated 2026-06)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree_mujoco
---
