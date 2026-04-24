#include "fsm.h"
#include <Arduino.h>

// Artifex Eco-Press - Portenta H7 M7 Core
// Deterministic 48-Second Cycle FSM

void CycleFSM::initialize() {
    currentState = State::IDLE;
    Serial.println("FSM Initialized: Waiting for Dew Point & NIR preconditions.");
}

void CycleFSM::update() {
    switch(currentState) {
        case State::IDLE:
            if (checkPreconditions()) {
                transitionTo(State::MOLD_CLOSE);
            }
            break;

        case State::MOLD_CLOSE:
            // Regenerative extension 4.4s, standard extension 0.1s
            if (timer.elapsed() >= 4500) {
                transitionTo(State::INJECTION);
            }
            break;

        case State::INJECTION:
            // 35mm AC Servo plunge at 1680 RPM
            if (checkVPSwitchover() || timer.elapsed() >= 3000) {
                transitionTo(State::COMPRESSION);
            }
            break;

        case State::COMPRESSION:
            // 13.8 MPa hold for 5s
            if (timer.elapsed() >= 5000) {
                transitionTo(State::ACTIVE_COOLING);
            }
            break;

        case State::ACTIVE_COOLING:
            // Chiller hold and Accumulator charge 12s
            if (timer.elapsed() >= 12000) {
                transitionTo(State::MOLD_OPEN);
            }
            break;

        case State::MOLD_OPEN:
            // Accumulator dump 0.58s
            if (timer.elapsed() >= 580) {
                transitionTo(State::EXTRACTION_AUDIT);
            }
            break;

        case State::EXTRACTION_AUDIT:
            // Robot extraction and AI Audit 11.5s
            if (timer.elapsed() >= 11500) {
                transitionTo(State::IDLE);
            }
            break;

        case State::FAULT_LATCHED:
            // System halted. Requires hardware RESET button.
            break;
    }
}
