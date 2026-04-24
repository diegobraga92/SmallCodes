# DracoFlite – DIY Drone Flight Controller & Ground Station

## Overview
A fully custom flight controller and ground station for a small quadcopter (or fixed‑wing), built from the PCB up. This project extends my Embraer flight simulation experience into the physical world, while serving as the primary learning vehicle for **embedded/real‑time systems (C++20 on FreeRTOS)** , **cyber‑physical Python backends (FastAPI ground station)** , **edge‑to‑cloud telemetry pipelines (MQTT, optional AWS IoT)** , and **reliable communication protocols over lossy links**.

**Core principle:** all firmware is written from scratch with safety and determinism in mind; the ground station is a local‑first Python service that streams telemetry in real time and provides a rich post‑flight analysis dashboard. An optional reliable link protocol will be implemented to ensure telemetry/command integrity over the noisy RF connection.

## Learning Objectives (Gaps Filled)
- **Embedded / Real‑Time (Primary Gap):**
  - Hard real‑time firmware in modern C++20 on a Cortex‑M4/M7 microcontroller (STM32).
  - FreeRTOS for task scheduling, sensor fusion at 1 kHz, PID motor control loop.
  - Watchdog timers, safe state handling, and interrupt‑driven drivers.
  - Communication protocols: MAVLink, serial, I²C, SPI.
- **Python Backend (Solidified in Cyber‑Physical Context):**
  - FastAPI ground station server for telemetry ingestion, live dashboard, and mission planning.
  - WebSocket push for real‑time flight data, async hardware communication.
- **Cloud (Lightweight Touch):**
  - Optional telemetry mirror to the cloud (AWS IoT Core + Timestream / S3) via Terraform.
  - MQTT bridging from local broker to cloud for remote live view.
- **Networking Reliability (New):** Design and implement a reliable transport layer over MAVLink (ack/nack, retransmission) to handle RF dropouts gracefully.
- **System Design:** Edge computing architecture, graceful degradation when cloud is unreachable, fault‑tolerant RF link, over‑the‑air firmware updates (optional).

## Core Features (MVP)
1. **Flight Controller Firmware (C++20 on FreeRTOS)**
   - Sensor fusion (IMU + barometer + compass) for attitude and altitude estimation (complementary filter or EKF).
   - Rate and angle PID controllers for pitch, roll, yaw.
   - Pilot command processing via RC receiver (SBUS/CRSF) or autonomous mission waypoints.
   - Failsafe behaviors: loss of RC signal → land/disarm; low battery → return to home.
   - Hardware watchdog and brown‑out detection.
2. **Ground Station Software (Python FastAPI)**
   - Real‑time telemetry display: attitude, position, battery, link quality, flight mode.
   - Map overlay with live drone position (using Leaflet/Mapbox in web UI).
   - Mission planner: define waypoints, upload to drone via MAVLink.
   - Flight log replay and post‑flight analytics (motor wear, GPS accuracy, vibration levels).
3. **Reliable Communication Link**
   - A lightweight protocol on top of MAVLink serial packets: sequence numbers, acknowledgements, retransmission timers.
   - Graceful fallback to unreliable mode if bandwidth is too low.
   - This demonstrates systems‑level networking design.
4. **Optional Cloud Mirror**
   - Live telemetry proxy via MQTT to AWS IoT Core for remote monitoring (with delay).
   - Automatic log backup to S3 for long‑term storage.
   - Over‑the‑air (OTA) firmware update mechanism via the ground station or cloud.

## Tech Stack
### Flight Controller (Embedded)
- **MCU:** STM32F405/7 or compatible (common in flight controller designs).
- **RTOS:** FreeRTOS, task priorities carefully assigned.
- **Language:** C++20 (no dynamic allocation after boot, compile‑time polymorphism where possible).
- **Libraries:**
  - Sensor drivers: custom or STM HAL, MPU9250/ICM‑20948, BMP280, GPS (U‑blox NEO‑M8N).
  - Math: `Eigen` or `arm_math` for matrix operations.
  - Communication: MAVLink protocol for telemetry and commands.
  - Control: custom PID library, complementary filter / EKF.
- **Build System:** CMake with ARM GCC, unit tests on host with gtest.

### Ground Station (Python)
- **Framework:** FastAPI + Uvicorn.
- **Dashboard:** Vue.js or React (reuse frontend skills) with a map component.
- **Telemetry Ingestion:** Serial connection to RF modem using `pyserial`, MAVLink parsing with `pymavlink`.
- **Reliable Link Layer:** Custom Python module implementing ack/nack and retransmission.
- **Real‑time:** WebSocket endpoints for live data push to dashboard.
- **Database:** SQLite for local logs, optional PostgreSQL for cloud mirror.

### Cloud (Optional, Lightweight)
- **Messaging:** MQTT broker (Mosquitto) on ground station, bridged to AWS IoT Core.
- **Storage:** S3 for log archives, AWS Timestream for time‑series telemetry (or just parquet files).
- **OTA Updates:** Store firmware images in S3, notify drone via MQTT, drone downloads and verifies signature.
- **IaC:** Terraform for IoT Core resources, S3 bucket, and optional EC2 if a remote dashboard is needed.

### Local Development & Simulation
- **Software‑in‑the‑Loop (SITL):** Use a simple physics simulator (e.g., custom Python or Gazebo) to test the ground station and flight control logic before hardware is ready.
- **Hardware‑in‑the‑Loop (HIL):** Run the real firmware on a dev board with simulated sensor inputs from the simulator → ground station connects as if real flight.

## Architecture Diagram (Logical)
[Drone]
│
├─ Sensors (IMU, Baro, GPS)
├─ PID Loops (Attitude, Rate)
├─ MAVLink over Serial → Reliable Link Layer
└─ RC Receiver (SBUS)
│
▼
[Telemetry Radio] ←→ [Ground Station Python App]
│
├─ Serial MAVLink Parser
├─ Reliable Link Handler
├─ WebSocket Server ↔ [Web Dashboard]
├─ SQLite Flight Logs
└─ MQTT Client → [Local Mosquitto] → (optional) AWS IoT

## Implementation Phases
### Phase 1: Toolchain & Firmware Skeleton (Weeks 1‑4)
- Set up STM32CubeIDE or bare metal CMake toolchain.
- Blink LED using FreeRTOS task → hardware watchdog works.
- Implement MAVLink heartbeat over serial, confirm ground station detects it.
- Write IMU driver and read raw data in a sensor task at 1 kHz.

### Phase 2: Attitude Estimation & Control Loops (Weeks 5‑8)
- Implement complementary filter or EKF for pitch/roll.
- Rate PID controller for gyro stabilization (bench test with motors, props off).
- Attitude PID for auto‑level mode.
- Integrate RC receiver (SBUS) to pass pilot commands.
- Work in SITL to tune gains safely.

### Phase 3: Ground Station Core (Weeks 6‑10, parallel)
- FastAPI project with serial reader, MAVLink parser.
- Design and implement the reliable link protocol (sequence numbers, retransmission).
- WebSocket endpoint for live telemetry; basic dashboard with attitude indicator.
- Mission planning UI: waypoint list, map picker.
- Flight log viewer: replay stored missions with slider.

### Phase 4: First Flight & Iteration (Weeks 9‑12)
- Mount on a reliable frame, constrained hover tests.
- Failsafe behaviors: loss‑of‑signal, low battery landing.
- Tune PIDs aggressively based on real flight logs.
- Flight log post‑analysis: power spectral density of vibrations, motor output balance.

### Phase 5: Cloud Mirror & OTA (Weeks 13‑16)
- Set up MQTT bridge and AWS IoT Core via Terraform.
- Auto‑upload logs to S3 after each flight.
- Implement OTA firmware update: drone listens for update commands, downloads new binary, verifies, and reboots.
- (Optional) Remote live view of drone telemetry from a browser anywhere (low‑latency).
- Final documentation, demo video of autonomous mission.

## Gap‑Filling Deep Dives
### Embedded / Real‑Time
- **Deterministic scheduling:** FreeRTOS tasks with hard deadlines; priority assignment to avoid inversion.
- **Memory discipline:** no heap allocations after init; all buffers statically allocated.
- **Watchdog:** MCU resets if a task fails to check in, motors disarm.
- **Sensor fusion:** practical implementation of a Kalman filter for attitude, handling gyro drift and accelerometer noise.

### Python Backend (Cyber‑Physical)
- **Async serial I/O:** using `pyserial-asyncio` for non‑blocking telemetry.
- **WebSocket push:** real‑time broadcast to many clients.
- **Background tasks:** logging, MQTT bridging, and map tile fetching all run concurrently.
- **Testing:** mock MAVLink stream to verify ground station behavior without hardware.

### Networking Reliability (New)
- **Custom protocol:** Lightweight transport with CRC checks, nack‑based retransmission.
- **Performance:** measure throughput and latency over real RF link.
- **Recovery:** test with simulated packet loss.

### Cloud (Lightweight)
- **AWS IoT Core:** device provisioning, MQTT topics, rules to route data to Timestream/S3.
- **Terraform:** manage IoT policies, certificates, and S3 bucket in a repeatable way.

## Non‑Goals (for this project)
- No Golang or Rust backend – those are covered in other projects.
- No complex Kubernetes – cloud is intentionally minimal.
- No machine learning or computer vision (yet – could be an extension).
- Not a consumer product; it’s a research/development platform for my own use.

## Why I’ll Actually Use This
- I can fly a drone I built and programmed myself, merging my simulation past with my maker future.
- It’s the ultimate conversation starter for interviews that proves I understand systems from bare metal to cloud.
- Flight data and analytics let me continuously improve, just like I did with aircraft simulators at Embraer.
- Unlimited customization: add a camera gimbal, autonomous missions, or even a payload drop mechanism later.

---

**Author:** Diego Braga  
**Status:** Planning phase – hardware procurement begins after SafeSync MVP.
