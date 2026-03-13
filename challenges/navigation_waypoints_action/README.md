# 🤖 Autonomous Navigation Challenge

Welcome to the Autonomous Navigation Challenge! In this repository, you will find the base workspace required to complete the integration of an Action Server with the Nav2 stack. 

Your mission is to act as the systems integrator: build the "brain" of the robot to bridge high-level command requests with low-level navigation and mapping, utilizing a provided path-optimization algorithm.



## 📑 Table of Contents
- [Overview](#-overview)
- [System Architecture & Rules](#-system-architecture--rules)
- [Your Mission](#-your-mission)
- [Provided Tools](#-provided-tools)
- [Getting Started](#-getting-started)
- [How to Run](#-how-to-run)

---

## 📋 Overview

You are provided with a complete base ROS 2 workspace. This includes an Action Client, predefined Action Interfaces, a base SLAM/Nav2 stack, and a custom waypoint optimization function. 

Your goal is to implement the **Action Server**, integrate the waypoint optimizer, and tune the **SLAM/Nav2 stack** so the robot can smoothly and efficiently execute the optimized route without violating physical constraints.

---

## 🏗️ System Architecture & Rules

To ensure a level playing field, certain parts of the system are strictly locked. Focus your engineering efforts entirely on the Action Server logic and navigation tuning.

### Modifiability Matrix

| Component | Status | Description |
| :--- | :---: | :--- |
| **Action Client** | 🔒 **LOCKED** | Initiates the task and sends the goal. Do not modify. |
| **Action Interfaces** | 🔒 **LOCKED** | The `.action` files defining the structure of the goal, feedback, and result. |
| **Robot Physics/Kinematics** | 🔒 **LOCKED** | Start point, max/min velocity, acceleration, mass, and inertia. |
| **Action Server** | 🛠️ **MODIFIABLE** | **Your core deliverable.** Implement your state machine and logic here. |
| **SLAM & Nav2 Stack** | 🛠️ **MODIFIABLE** | Tune parameters (costmaps, planners, inflation radii) to ensure efficient movement. |

> **⚠️ STRICT RULE:** You may not "cheat" the physics. Altering the robot's physical constraints (e.g., cranking up max velocity, modifying inertia) or manually changing the starting pose is strictly prohibited and will result in a failed evaluation. Your performance relies purely on efficient software integration and parameter tuning.

---

## 🚀 Your Mission

Your primary task is to write the Action Server node (`action_server_node.py` or `.cpp`) and tune the navigation stack configurations. 

Your Action Server must successfully:
1. **Receive the Goal:** Accept the high-level task from the fixed Action Client.
2. **Optimize the Route:** Pass the necessary target data into the provided **Waypoint Optimizer Function** to calculate the best sequence of waypoints.
3. **Execute the Sequence:** Communicate the optimized waypoints sequentially to the Nav2 stack.
4. **Manage State:** Monitor the robot's progress and handle potential navigation failures via SLAM/Nav2 feedback.
5. **Return Feedback & Result:** Pipe standard progress feedback and the final completion result back to the Action Client using the locked Action Interfaces.

---

## 🧰 Provided Tools

* `waypoint_optimizer`: A library/function that calculates the most efficient sequence of waypoints to reach the destination. You must call this from your Action Server.
* `nav_base_pkg`: The foundational SLAM and Nav2 configurations to get you started. (You are expected to tune the `.yaml` files in this package!)

---

## 💻 Getting Started

### Prerequisites
* Ubuntu 22.04
* ROS 2 Humble
* Nav2 Stack (`sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup`)

### Installation

1. Create a workspace and clone the repository:
   ```bash
   mkdir -p ~/nav_challenge_ws/src
   cd ~/nav_challenge_ws/src
   git clone <YOUR_REPO_URL_HERE> .
