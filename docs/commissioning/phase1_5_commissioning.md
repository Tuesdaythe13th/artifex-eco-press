# Artifex Eco-Press: Commissioning Checklist & Validation Plan

## 1. Risk & Compliance Checklist
| ID | Subsystem | Critical Item to Verify | Commissioning Standard | Status |
|----|-----------|--------------------------|------------------------|--------|
| R-01 | Safety | Voice-Interrupt Relay | Drop KM1 instantly (<100ms) | [ ] |
| R-02 | Safety | Hardware Reset Loop | System remains locked until physical button press | [ ] |
| R-03 | Safety | Dual-Channel E-Stop | Both channels break power to pump/heaters | [ ] |
| R-04 | Thermal | Hardware Cutoffs | Verified trip at exactly 280°C (test with heat gun) | [ ] |
| R-05 | Electrical | Load Sequencing | Firmware prevents concurrent pump and MTC heater start | [ ] |
| R-06 | Hydraulic | Overpressure Relief | Relief valve opens precisely at 13.8 MPa | [ ] |
| R-07 | Clearances | Mold-Open Stroke | Robot end-effector clears both platens cleanly at required stroke | [ ] |

## 2. Validation Test Plan

### Test A: Thermal Cut-Off Grounding
1. **Setup:** Isolate the thermal cutoffs (e.g., Omega TCALN-K) from the mains power but monitor continuity.
2. **Action:** Apply external heat via a calibrated industrial heat gun to the cutoff sensor.
3. **Observation:** Monitor continuity via multimeter.
4. **Pass Criteria:** Continuity breaks at exactly 280°C (±2°C). Cutoff does not auto-reset upon cooling (requires manual reset).

### Test B: Hydraulic Regenerative Close
1. **Setup:** Machine powered, no melt loaded, mold empty. Set limit switches.
2. **Action:** Trigger the "Mold Close" command.
3. **Observation:** Measure the time from solenoid actuation to final 2mm gap.
4. **Pass Criteria:** Platen completes the 12-inch traverse in ~4.5 seconds. Pump does not cavitate (listen for harsh rattling).

### Test C: Power-Sequencing Interlock
1. **Setup:** Clamp ammeter on the primary 240V/40A feed.
2. **Action:** Attempt to issue a simultaneous "Pump Start" and "Heaters On" command.
3. **Observation:** Observe the firmware logic execution and the ammeter reading.
4. **Pass Criteria:** Firmware forces the pump to spin up completely before energizing the 4x400W mold heaters. Peak inrush current never exceeds 40A.
