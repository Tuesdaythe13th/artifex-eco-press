# Artifex Eco-Press

> **100‑Ton Injection‑Compression | AI‑Supervised | Open‑Source | Modular Hardening**

The Artifex Eco-Press is a pre-engineered, pre-costed cyber-physical manufacturing platform targeted at independent artists, small labels, and eco-focused brands. It transitions vinyl production economics from a per-run outsourcing model to a marginal-cost manufacturing model, pressing audiophile-grade 12-inch LP records from 100% recycled PET.

## Architecture

The system employs a hierarchical distributed control architecture:

* **L3 — Supervisor:** NVIDIA Jetson Orin Nano (OpenCV Vision, Orchestration, HMI)
* **L2 — Real-Time Control:** Arduino Portenta H7 M7 (Cycle FSM, Servo/Hydraulic Control)
* **L2 — Fast Safety/PID:** Arduino Portenta H7 M4 (SSR PWM, Thermocouple Polling)
* **L1 — Voice Safety:** Teensy 4.0 + I2S Mic (Keyword Stop)
* **L0 — Hardwired:** Pilz PNOZ X2.1 + 290°C Thermal Cutoffs

## Repository Structure

* `docs/`: Master specification and Agent Action Plan
* `schemas/`: Single Source of Truth JSON schemas
* `config/`: System setpoints and phase budgets
* `jetson/`: Python Supervisor Application
* `firmware/`: Portenta H7 and Teensy 4.0 code
* `hardware/`: BOM, Schematics, Pinmaps
