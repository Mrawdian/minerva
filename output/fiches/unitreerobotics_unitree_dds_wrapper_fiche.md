---
## unitreerobotics/unitree_dds_wrapper
**Type:** Library
**Domain:** Edge AI
**Relevance score:** 49/100
**Problem solved:** Abstracts the DDS (Data Distribution Service) middleware layer for Unitree quadruped robots, eliminating the need to manually write boilerplate publisher/subscriber code and handle IDL-generated message definitions.
**How it works:** Provides auto-generated Python wrapper classes ({robot}_pub, {robot}_sub) from IDL specifications with pre-populated default values, reducing integration friction. Built on top of DDS middleware (likely CycloneDDS or similar); depends on Pinocchio for kinematics/dynamics. Installable via pip; targets Python 3.x environments on systems compatible with Unitree's robot SDK.
**Chinese specificity:** Hosted on GitHub by unitreerobotics (Unitree Robotics, a Chinese quadruped robot manufacturer); no particular Chinese specificity beyond the author's origin and focus on Unitree's proprietary robot platforms.
**Western equivalent:** ROS 2 DDS abstraction layer, Cyclone DDS Python bindings
**Maturity:** Experimental (★ 33, 6 forks, updated 2024-10)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree_dds_wrapper
---
