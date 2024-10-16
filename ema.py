import numpy as np

def exponential_moving_average(data, initial_alpha=0.1, k=2, sensitivity=0.2, stability=0.1, window_size=100):
    ema = None
    residuals = []
    dynamic_threshold = None
    alpha = initial_alpha

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

        residual = abs(value - ema)
        residuals.append(residual)

        # Calculate dynamic threshold based on residuals (use sliding window)
        if len(residuals) > window_size:
            std_residuals = np.std(residuals[-window_size:])
        else:
            std_residuals = np.std(residuals) if len(residuals) > 1 else 1
        
        dynamic_threshold = k * std_residuals
        
        # Flag anomaly if residual exceeds the threshold
        is_anomaly = residual > dynamic_threshold
        
        # Yield time step, value, EMA, residual, threshold, and anomaly flag
        yield t, value, ema, residual, dynamic_threshold, is_anomaly

    
