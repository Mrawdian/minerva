---
## unitreerobotics/unitree_rl_lab
**Type:** Framework
**Domain:** Robotics / Edge AI
**Relevance score:** 75/100
**Problem solved:** Provide reinforcement learning training environments for Unitree quadruped and humanoid robots (Go2, H1, G1-29dof) integrated with NVIDIA's IsaacLab simulator, enabling sim-to-sim and sim-to-real policy transfer without proprietary training frameworks.
**How it works:** Built on IsaacLab (NVIDIA's physics simulation framework) and MuJoCo for environment definition; Python-based RL training with support for policy deployment via C++ robot controllers compiled against unitree_sdk2. Includes standalone IsaacLab environments installable via pip, MuJoCo simulation for validation, and C++ deployment binaries (g1_ctrl, etc.) that communicate with robots over Ethernet using Unitree's proprietary protocol. Dependencies: YAML-cpp, Boost, Eigen3, spdlog, fmt for the control layer.
**Chinese specificity:** Hosted by Unitree Robotics, a Chinese manufacturer of quadruped and humanoid robots; no integration with Chinese cloud platforms or chipset vendors (uses NVIDIA GPUs for training, standard x86/ARM for deployment). The project is specific to Unitree hardware but otherwise follows Western open-source conventions.
**Western equivalent:** NVIDIA IsaacGym (proprietary baseline), OpenAI Gym with MuJoCo backend, Gazebo with ROS 2 for robot simulation and RL training
**Maturity:** Stable (★ 1245, 301 forks, updated 2026-05)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree_rl_lab
---
