
#include <math.h>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#define CALL __cdecl
#else
#define EXPORT
#define CALL
#endif

// =====================================================
// CONTROLLER PARAMETERS
// =====================================================

static double gamma_max = 2.0;  // [deg]
static double T_max = 1500.0;   // [kN]
static double T_reset = 900.0;  // [kN]
static double max_rate = 0.5;   // [deg/s]

// =====================================================
// CONTROLLER STATES
// =====================================================

enum ControllerState {
    UNCONED,
    CONING,
    CONED,
    RETURNING
};

static enum ControllerState state = UNCONED;

// Current commanded coning angle
static double gamma = 0.0;

// S-curve trajectory parameters
static double gamma_start = 0.0;
static double gamma_end = 0.0;
static double t_start = 0.0;
static double ramp_duration = 0.0;


// =====================================================
// S-CURVE FUNCTION
// =====================================================

static double smoothstep(double s)
{
    // Limit normalized time to [0, 1]
    if (s < 0.0) s = 0.0;
    if (s > 1.0) s = 1.0;

    // Quintic S-curve
    return 10.0*s*s*s
         - 15.0*s*s*s*s
         + 6.0*s*s*s*s*s;
}


// =====================================================
// START A NEW CONING MOVEMENT
// =====================================================

static void start_movement(
    double time,
    double target_angle,
    enum ControllerState new_state)
{
    gamma_start = gamma;
    gamma_end = target_angle;
    t_start = time;

    // Duration based on peak angular velocity
    ramp_duration = 1.875 *
        fabs(gamma_end - gamma_start) / max_rate;

    state = new_state;
}


// =====================================================
// INITIALIZATION
// =====================================================

EXPORT void CALL initialize(
    double *input,
    double *output)
{
    // Read HTC initialization parameters
    gamma_max = input[0];
    T_max = input[1];
    T_reset = input[2];
    max_rate = input[3];

    // Validate parameters
    if (!isfinite(gamma_max) || gamma_max <= 0.0 ||
        !isfinite(T_max) || !isfinite(T_reset) ||
        T_reset >= T_max ||
        !isfinite(max_rate) || max_rate <= 0.0)
    {
        output[0] = 0.0;
        return;
    }

    // Reset controller state
    gamma = 0.0;
    gamma_start = 0.0;
    gamma_end = 0.0;
    t_start = 0.0;
    ramp_duration = 0.0;

    state = UNCONED;

    output[0] = 1.0;
}


// =====================================================
// CONTROLLER UPDATE
// =====================================================

EXPORT void CALL update(
    double *input,
    double *output)
{
    // Read HAWC2 signals
    double time = input[0];    // [s]
    double thrust = input[1];  // [kN]

    // -------------------------------------------------
    // 1. CHECK THRUST AND START MOVEMENT
    // -------------------------------------------------

    if (state == UNCONED && thrust > T_max)
    {
        start_movement(time, gamma_max, CONING);
    }

    else if (state == CONED && thrust < T_reset)
    {
        start_movement(time, 0.0, RETURNING);
    }

    // -------------------------------------------------
    // 2. COMPUTE S-CURVE TRAJECTORY
    // -------------------------------------------------

    if (state == CONING || state == RETURNING)
    {
        double s = (time - t_start) / ramp_duration;

        if (s >= 1.0)
        {
            // Movement complete
            gamma = gamma_end;

            if (state == CONING)
            {
                state = CONED;
            }
            else
            {
                state = UNCONED;
            }
        }
        else
        {
            // Calculate smooth coning angle
            gamma = gamma_start +
                (gamma_end - gamma_start) * smoothstep(s);
        }
    }

    // -------------------------------------------------
    // 3. APPLY COLLECTIVE CONING
    // -------------------------------------------------

    output[0] = gamma;  // Cone 1
    output[1] = gamma;  // Cone 2
    output[2] = gamma;  // Cone 3
}
