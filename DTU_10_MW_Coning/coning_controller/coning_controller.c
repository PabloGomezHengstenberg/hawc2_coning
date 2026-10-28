
#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

// Controller parameters
static double gamma_target = 10.0;
static double t_start = 10.0;
static double ramp_duration = 10.0;

// Initialization
EXPORT void __cdecl initialize(
    double *input,
    double *output)
{
    gamma_target = input[0];

    output[0] = 1.0;
}

// Controller update
EXPORT void __cdecl update(
    double *input,
    double *output)
{
    double t = input[0];
    double gamma;

    if (t <= t_start) {
        gamma = 0.0;
    }
    else if (t < t_start + ramp_duration) {
        gamma = gamma_target *
                (t - t_start) / ramp_duration;
    }
    else {
        gamma = gamma_target;
    }

    // Apply collective coning
    output[0] = gamma;  // Cone 1
    output[1] = gamma;  // Cone 2
    output[2] = gamma;  // Cone 3
}
