# Artifex Eco-Press — Agent Action Plan

## 0.1 Product Understanding
Based on the prompt, the Blitzy platform understands that the new product is the Artifex Eco-Press Rev 8.3/8.4 FINAL — an open-source, AI-supervised, 100-ton injection-compression manufacturing cell that presses audiophile-grade 12-inch LP records from 100% recycled PET (r-PET). The deliverable for this Agent Action Plan is the complete software, firmware, and documentation artefact set that brings the specified hardware build into a production-ready, safety-certified, ISO 13849-compliant operating system executing a strict 48-second cycle at 75 discs/hour.

### 0.1.1 Core Product Vision
The Artifex Eco-Press is a pre-engineered, pre-costed cyber-physical manufacturing platform targeted at independent artists, small labels, and eco-focused brands. It transitions vinyl production economics from a per-run outsourcing model ($3.99–$7.87/disc) to a marginal-cost manufacturing model ($0.85/disc), with capital recoverable in less than one production day at typical retail pricing.

**Functional Requirements (Technically Restated):**
* **FR-01 — Cycle Orchestration:** The software shall execute a deterministic 48-second production cycle composed of six sequential phases without operator intervention.
* **FR-02 — Hydraulic Control:** The firmware shall drive the 4/3 proportional spool valve through three distinct modes per cycle.
* **FR-03 — Injection Drive Control:** The firmware shall command the 1.5 kW AC Servo (130ST-M10015) to rotate the 35 mm ball-screw at 1680 RPM.
* **FR-04 — Thermal Regulation:** A multi-zone PID controller shall maintain barrel heaters and hold the mold at 60°C.
* **FR-05 — Pre-Production Gating:** Dew-point sensor confirms < -40°C for >= 90 mins AND NIR sensor confirms surface moisture < 55 ppm.
* **FR-06 — AI Quality Audit:** A computer-vision pipeline shall analyze each ejected disc via the ELP 1080p camera for haze and flash using OpenCV.
* **FR-07 — Data Logging:** Every cycle shall log a structured JSON packet.
* **FR-08 — Reject Handling:** Failed audits shall trigger quarantine routing.
* **FR-09 — Extraction Choreography:** 3-axis Cartesian gantry extraction control.

**Non-Functional Requirements:**
* **NFR-01 — Safety (Priority: P0):** ISO 13849-1 Category 3 / Performance Level d.
* **NFR-02 — Latching Fault Semantics:** Interlock trips require physical RESET.
* **NFR-03 — Real-Time Determinism:** Sub-millisecond cycle-timing determinism.
* **NFR-04 — Throughput:** Sustained 48-second cycle time.
* **NFR-05 — Inter-Processor Communication:** Portenta H7 (M7) and Jetson communicate over UART4 at 920 kbps (JSON).
* **NFR-06 — Power Envelope:** Coincident load must not exceed 9,530 W.

### 0.1.2 Technology Stack
* **Microcontroller:** Arduino Portenta H7 (Cortex-M7 + Cortex-M4)
* **Edge AI:** NVIDIA Jetson Orin Nano 4GB module
* **Voice Safety:** Teensy 4.0 + I2S Mic
* **Safety Relay:** Pilz PNOZ X2.1
* **Vision Library:** OpenCV (blob/contour detection)
* **Languages:** C/C++ (Arduino/Mbed, Teensyduino), Python 3.10 (Jetson)

## 0.3 Technical Architecture Design
The Artifex Eco-Press software stack is a hierarchical three-tier distributed control architecture with a hardwired safety substrate.

* **L3 — Supervisor (Jetson Orin Nano):** Python 3.10, OpenCV 4.12, FastAPI, SQLite
* **L2 — Real-Time Controller (Portenta H7 M7):** C++17 on Arduino Mbed Core
* **L2 — PID / SSR / ISRs (Portenta H7 M4):** C++ on Mbed pinned to deterministic tasks
* **L1 — Voice Safety (Teensy 4.0):** C++ on Teensyduino + Audio Library
* **L0 — Hardwired Safety:** Pilz PNOZ X2.1 + 290°C bimetallic cutoffs

## 0.5 Repository Structure Planning
A polyglot monorepo structure separating firmware (Portenta, Teensy) and supervisor software (Jetson), sharing common JSON schemas.

### 0.5.1 Proposed Directory Tree
* `/firmware/portenta_h7/` (Cycle FSM, PID, Safety, Comms)
* `/firmware/teensy_40/` (Voice Keyword Stop)
* `/jetson/` (Python Orchestrator, OpenCV Vision, HMI, SQLite Logger)
* `/schemas/` (Single Source of Truth JSON schemas for code-generation)
* `/config/` (YAML configurations)
* `/hardware/` (BOMs, Schematics, Pinmaps)
* `/docs/` (Architecture, Operator Runbook, Commissioning)
* `/scripts/` (Build and Flash scripts)

## 0.7 Deliverable Mapping & Phases

* **Phase F0 — Foundation:** Repo skeleton, config files, schema codegen, and CI setup.
* **Phase F1 — Core Logic:** Portenta FSM skeleton, Teensy audio capture, Jetson orchestrator skeleton.
* **Phase F2 — Interfaces:** Drivers, OpenCV pipeline, SQLite DB, HMI.
* **Phase F3 — Testing:** Unity/Ceedling tests, Python pytest, commissioning wrappers.
* **Phase F4 — Documentation:** Runbooks, maintenance guides, architecture.
* **Phase F5 — Release Hardening:** SBOMs, signed artefacts.
