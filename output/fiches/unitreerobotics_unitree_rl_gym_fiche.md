---
## unitreerobotics/unitree_rl_gym
**Type:** Framework
**Domain:** Robotics
**Relevance score:** 73/100
**Problem solved:** Provides a reinforcement learning training pipeline and sim-to-real deployment framework for legged robot locomotion control, bridging the gap between policy training in Isaac Gym simulation and execution on physical Unitree quadruped and humanoid robots (Go2, G1, H1).
**How it works:** Built on legged_gym (ETH Zurich) for RL training environment, rsl_rl for policy optimization, and MuJoCo for physics simulation. Python-based training scripts generate control policies; deployment modules target MuJoCo sim-to-sim transfer and real hardware via unitree_sdk2_python (UDP-based communication). Includes C++ deployment binaries for G1 robot compiled with CMake. Supports headless training mode and checkpoint-based model loading.
**Chinese specificity:** Hosted on Gitee/GitHub by unitreerobotics; no particular Chinese specificity beyond the author. Unitree Robotics is a Chinese manufacturer of legged robots, but the framework itself is built on Western open-source foundations (ETH Zurich's legged_gym, Google DeepMind's MuJoCo) without integration of Chinese cloud platforms or chipset vendors.
**Western equivalent:** legged_gym (ETH Zurich), Isaac Gym (NVIDIA), Gazebo with ROS (Open Robotics)
**Maturity:** Experimental (★ 3461, 570 forks, updated 2025-07)
**Language:** Bilingual CN-EN
**GitHub:** https://github.com/unitreerobotics/unitree_rl_gym
---
