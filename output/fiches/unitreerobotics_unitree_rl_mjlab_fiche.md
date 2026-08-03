---
## unitreerobotics/unitree_rl_mjlab
**Type:** Framework
**Domain:** Robotics
**Relevance score:** 74/100
**Problem solved:** Provide a lightweight, modular reinforcement learning framework for training and deploying locomotion policies on Unitree quadruped and humanoid robots using MuJoCo physics simulation, with direct sim-to-real transfer via ONNX export.
**How it works:** Built on mjlab (which combines Isaac Lab's API with MuJoCo physics), the framework implements RL training loops in Python using reward-based policy optimization. Supports multi-GPU training via PyTorch, exports trained policies as ONNX models for deployment. Targets Unitree Go2, A2, As2, G1, R1, H1_2, and H2 robots. Deployment requires cyclonedds and unitree_sdk2 for robot communication.
**Chinese specificity:** Hosted by unitreerobotics (Unitree Robotics, a Chinese quadruped/humanoid robot manufacturer); no particular Chinese chipset vendor or standard integration beyond the author's commercial robot platform.
**Western equivalent:** Isaac Lab (NVIDIA), Legged Gym (ETH Zurich), rsl_rl (ETH Zurich)
**Maturity:** Stable (★ 558, 157 forks, updated 2026-04)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree_rl_mjlab
---
