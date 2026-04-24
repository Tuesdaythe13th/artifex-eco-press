#pragma once

#define SSR_PIN 5 // Hardware SSR Control Pin

class ThermalController {
public:
    ThermalController(float kp, float ki, float kd, float setpoint);
    void update(float currentTemp, float dt);

private:
    float kp, ki, kd;
    float setpoint;
    float integral;
    float previousError;

    void applyPWM(float dutyCycle);
};
