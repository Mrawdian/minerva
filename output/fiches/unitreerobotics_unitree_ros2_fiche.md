---
## unitreerobotics/unitree_ros2
**Type:** Framework
**Domain:** Robotics
**Relevance score:** 71/100
**Problem solved:** Enable ROS2-native communication with Unitree quadruped robots (Go2, B2, H1) by exposing their CycloneDDS-based SDK as standard ROS2 message types, eliminating the need to wrap proprietary SDK interfaces.
**How it works:** The project bridges Unitree SDK2 (built on CycloneDDS 0.10.2) with ROS2 by providing ROS2 message definitions and example packages. It requires Ubuntu 20.04/22.04, ROS2 foxy/humble, CycloneDDS middleware (compiled separately for foxy), libyaml-cpp-dev, and rmw-cyclonedds-cpp. The workspace contains cyclonedds_ws with unitree_go and unitree_api message packages, plus example applications demonstrating robot control and communication.
**Chinese specificity:** Hosted on GitHub by unitreerobotics (Unitree Robotics, a Chinese quadruped robot manufacturer); no particular Chinese standard or chipset vendor tie beyond the author's commercial robotics platform.
**Western equivalent:** MoveIt2 (ROS2 motion planning), Clearpath Robotics ROS2 packages (commercial robot ROS2 integration)
**Maturity:** Stable (★ 779, 229 forks, updated 2026-07)
**Language:** English
**GitHub:** https://github.com/unitreerobotics/unitree_ros2
---
