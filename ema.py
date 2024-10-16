import numpy as np

# Online algorithm for standard deviation (to avoid recalculating the full window)
def update_stats(mean, M2, n, new_value):
    """
    Update the mean, variance incrementally using Welford's algorithm.
    
    This method computes the mean and variance for a stream of data in an online fashion
    without needing to store the entire dataset. The variance is updated with each new data point.
    
    Parameters:
    mean (float): Current mean of the data stream.
    M2 (float): Sum of squares of differences from the current mean.
    n (int): Number of data points processed so far.
    new_value (float): New data point to be included in the statistics.

    Returns:
    mean (float): Updated mean.
    M2 (float): Updated sum of squares of differences from the mean.
    variance (float): Updated variance.
    n (int): Updated number of data points processed.
    """
    n += 1
    delta = new_value - mean
    mean += delta / n
    delta2 = new_value - mean
    M2 += delta * delta2
    variance = M2 / n if n > 1 else 0
    return mean, M2, variance, n

def exponential_moving_average(data, initial_alpha=0.1, k=2, sensitivity=0.2, window_size=100, warmup_period=5):
    """
    Calculate the Exponential Moving Average (EMA) while adapting the smoothing factor (alpha)
    to handle concept drift and detect anomalies in the data.

    Parameters:
    data (list): Time series data to process.
    initial_alpha (float): Initial smoothing factor for EMA.
    k (float): Factor for setting dynamic thresholds (multiplies standard deviation of residuals).
    sensitivity (float): Minimum change in data needed to consider it as a potential spike (concept drift).
    window_size (int): Maximum number of residuals to store for analysis (unused here, but could be extended).
    warmup_period (int): Number of initial data points to ignore for anomaly detection (to stabilize EMA).

    Returns:
    Yields:
    tuple: (t, value, ema, residual, dynamic_threshold, is_anomaly)
        t (int): Time step.
        value (float): Current data value.
        ema (float): Current EMA value.
        residual (float): Difference between the actual value and EMA (residual).
        dynamic_threshold (float): Calculated dynamic threshold based on the residual variance.
        is_anomaly (bool): Flag indicating if the current data point is an anomaly (spike or dip).
    """
    ema = None  # Initialize EMA as None to indicate the first value hasn't been processed
    residuals = []  # List to store residuals (unused in current implementation)
    dynamic_threshold = None  # Initial dynamic threshold
    alpha = initial_alpha  # Set initial alpha (smoothing factor)
    recovery_mode = False  # Flag for recovery mode after detecting a spike
    cooldown = 0  # Cooldown period to prevent detecting consecutive spikes too quickly

    # Variables for online mean/variance calculation of residuals
    mean_residual = 0  # Running mean of residuals
    M2 = 0  # Running sum of squares of residuals
    n_residuals = 0  # Number of residuals processed
    cooldown_duration = 4  # Cooldown duration in time steps after a spike

    # Iterate over the time series data
    for t, value in enumerate(data):
        # Initialize EMA with the first data point
        if ema is None:
            ema = value
        else:
            # Calculate drift (absolute difference between value and EMA)
            drift = abs(value - ema)
            
            # Adjust alpha based on the drift or recovery mode (adaptive EMA)
            if drift > sensitivity:
                # Increase alpha (make EMA more responsive) during a spike
                alpha = min(0.5, alpha + 0.05)
                recovery_mode = True  # Enter recovery mode after spike
            elif recovery_mode and value < ema:
                # Speed up EMA recovery when values drop after a spike
                alpha = min(0.5, alpha + 0.1)
            else:
                # Slowly decrease alpha (make EMA less sensitive) after spike
                alpha = max(0.01, alpha - 0.02)
                recovery_mode = False  # Exit recovery mode once values stabilize

            # Update EMA using the adaptive alpha
            ema = alpha * value + (1 - alpha) * ema

        # Calculate residual (difference between actual value and EMA)
        residual = value - ema

        # Update online statistics for the residuals (mean and variance)
        mean_residual, M2, variance_residual, n_residuals = update_stats(mean_residual, M2, n_residuals, residual)

        # Calculate the dynamic threshold as a multiple of the standard deviation of residuals
        std_residual = np.sqrt(variance_residual)
        dynamic_threshold = k * std_residual

        # Warm-up period: Skip anomaly detection during the first few time steps
        if t < warmup_period:
            continue

        # Cooldown period: Skip anomaly detection if still within cooldown period after detecting a spike
        if cooldown > 0:
            cooldown -= 1
            continue

        # Check if the current residual exceeds the dynamic threshold (spike or dip detection)
        is_spike = residual > dynamic_threshold  # Spike: residual is greater than positive threshold
        is_dip = residual < -dynamic_threshold  # Dip: residual is less than negative threshold
        is_anomaly = is_dip or is_spike  # Anomaly is either a spike or dip

        # Trigger cooldown if a spike is detected
        if is_spike:
            cooldown = cooldown_duration  # Set cooldown period to prevent consecutive spikes

        # Yield the current time step, value, EMA, residual, threshold, and anomaly flag
        yield t, value, ema, residual, dynamic_threshold, is_anomaly
