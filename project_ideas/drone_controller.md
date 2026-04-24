
## Data Flow (Telemetry)
1. Flight controller sends MAVLink messages (ATTITUDE, GLOBAL_POSITION_INT, BATTERY_STATUS, etc.) at 10–50 Hz.
2. Ground station receives via serial, parses, pushes to WebSocket clients.
3. Dashboard renders real‑time instruments and map.
4. All messages are logged to SQLite with timestamps.
5. Optionally, ground station publishes to MQTT topics; a cloud mirror stores them.

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
- WebSocket endpoint for live telemetry; basic dashboard with attitude indicator.
- Mission planning UI: waypoint list, map picker.
- Flight log viewer: replay stored missions with slider.

### Phase 4: First Flight & Iteration (Weeks 9‑12)
- Mount on a reliable frame, constrained hover tests.
- Failsafe behaviors: loss‑of‑signal, low battery landing.
- Tune PIDs aggressively based on real flight logs.
- Flight log post‑analysis: power spectral density of vibrations, motor output balance.

### Phase 5: Cloud Mirror & Polish (Weeks 13‑16)
- Set up MQTT bridge and AWS IoT Core via Terraform.
- Auto‑upload logs to S3 after each flight.
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