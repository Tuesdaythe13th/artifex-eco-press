#include "pid.h"
#include <Arduino.h>

// Artifex Eco-Press - Portenta H7 M4 Core (Safety/Real-Time)
// 270°C PID SSR Control Loop

ThermalController::ThermalController(float kp, float ki, float kd, float setpoint)
    : kp(kp), ki(ki), kd(kd), setpoint(setpoint) {
    integral = 0.0f;
    previousError = 0.0f;
}

void ThermalController::update(float currentTemp, float dt) {
    // 1. Hardware Safety Interlock (Redundant to Pilz Relay)
    if (currentTemp > 290.0f) {
        Serial.println("THERMAL RUNAWAY! M4 CORE KILLING SSRs.");
        digitalWrite(SSR_PIN, LOW);
        return;
    }

    // 2. Compute PID
    float error = setpoint - currentTemp;
    integral += error * dt;
    float derivative = (error - previousError) / dt;

    float output = (kp * error) + (ki * integral) + (kd * derivative);
    previousError = error;

    // 3. Modulate SSR Duty Cycle (0-100%)
    output = constrain(output, 0.0f, 100.0f);
    applyPWM(output);
}

void ThermalController::applyPWM(float dutyCycle) {
    // Hardware specific PWM mapping
    int pwmValue = map(dutyCycle, 0, 100, 0, 255);
    analogWrite(SSR_PIN, pwmValue);
}
