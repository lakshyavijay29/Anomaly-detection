import numpy as np

# Online algorithm for standard deviation (to avoid recalculating the full window)
def update_stats(mean, M2, n, new_value):
    """Update the mean and variance incrementally (Welford's algorithm)."""
    n += 1
    delta = new_value - mean
    mean += delta / n
    delta2 = new_value - mean
    M2 += delta * delta2
    variance = M2 / n if n > 1 else 0
    return mean, M2, variance, n

def exponential_moving_average(data, initial_alpha=0.1, k=2, sensitivity=0.2, window_size=100):
    ema = None
    residuals = []
    dynamic_threshold = None
    alpha = initial_alpha

    # Variables for online mean/variance calculation
    mean_residual = 0
    M2 = 0
    n_residuals = 0

    # Calculate EMA for each point in the time series, adapting alpha for concept drift
    for t, value in enumerate(data):
        if ema is None:
            ema = value
        else:
            drift = abs(value - ema)
            
            # Update alpha more aggressively for stronger drift adaptation
            if drift > sensitivity:
                alpha = min(0.5, alpha + 0.05)  # Increase alpha faster when drift is detected
            else:
                alpha = max(0.01, alpha - 0.005)  # Decrease alpha slowly to avoid overreaction

            # Update EMA using adaptive alpha
            ema = alpha * value + (1 - alpha) * ema

        residual = value - ema

        # Update the online statistics for the residuals (mean and variance)
        mean_residual, M2, variance_residual, n_residuals = update_stats(mean_residual, M2, n_residuals, residual)

        # Dynamic threshold based on the standard deviation of residuals
        std_residual = np.sqrt(variance_residual)
        dynamic_threshold = k * std_residual

        # Flag anomaly if residual exceeds the threshold
        is_anomaly = abs(residual) > dynamic_threshold

        # Yield time step, value, EMA, residual, threshold, and anomaly flag
        yield t, value, ema, residual, dynamic_threshold, is_anomaly

