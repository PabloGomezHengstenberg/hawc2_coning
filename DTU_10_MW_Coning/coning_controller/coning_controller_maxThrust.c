
#include <math.h>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#define CALL __cdecl
#else
#define EXPORT
#define CALL
#endif

// Controller parameters
static double gamma_max = 2.0;  // [deg]
static double T_max = 1534.0;     // [kN]
static double T_reset = 900.0;   // [kN]
static double max_rate = 1.0;     // [deg/s]

// Controller state
static double gamma = 0.0;
static double previous_time = 0.0;
static int first_step = 1;
static int coning_active = 0;


// Initialize controller
EXPORT void CALL initialize(
    double *input,
    double *output)
{
    gamma_max = input[0];
    T_max = input[1];
    T_reset = input[2];
    max_rate = input[3];

    // Reset state
    gamma = 0.0;
    previous_time = 0.0;
    first_step = 1;
    coning_active = 0;

    output[0] = 1.0;
}


// Update controller at every time step
EXPORT void CALL update(
    double *input,
    double *output)
{
    // Read HAWC2 signals
    double time = input[0];    // [s]
    double thrust = input[1];  // [kN]

    // Calculate time increment
    double dt = 0.0;

    if (!first_step) {
        dt = time - previous_time;
        if (dt < 0.0) {
            dt = 0.0;
        }
    }

    previous_time = time;
    first_step = 0;

    // 1. Determine controller state
    if (!coning_active && thrust > T_max) {
        coning_active = 1;
    }
    else if (coning_active && thrust < T_reset) {
        coning_active = 0;
    }

    // 2. Determine target coning angle
    double gamma_target;

    if (coning_active) {
        gamma_target = gamma_max;
    }
    else {
        gamma_target = 0.0;
    }

    // 3. Apply coning rate limit
    double error = gamma_target - gamma;
    double max_step = max_rate * dt;

    if (error > max_step) {
        error = max_step;
    }
    else if (error < -max_step) {
        error = -max_step;
    }

    gamma += error;

    // 4. Apply collective coning
    output[0] = gamma;  // Cone 1
    output[1] = gamma;  // Cone 2
    output[2] = gamma;  // Cone 3
}
