#pragma once

#include <stdint.h>

class Timer {
public:
    void start();
    uint32_t elapsed();
private:
    uint32_t startTime = 0;
};

enum class State {
    IDLE,
    MOLD_CLOSE,
    INJECTION,
    COMPRESSION,
    ACTIVE_COOLING,
    MOLD_OPEN,
    EXTRACTION_AUDIT,
    FAULT_LATCHED
};

class CycleFSM {
public:
    void initialize();
    void update();

private:
    State currentState;
    Timer timer;

    void transitionTo(State nextState);
    bool checkPreconditions();
    bool checkVPSwitchover();
};
