import numpy as np

def generate_data_stream():
    t = 0
    while True:
        # Regular pattern: simulate a seasonal sine wave pattern
        seasonal = 10 * np.sin(2 * np.pi * t / 50)  # Seasonal element (50-period cycle)
        
        # Noise: add random Gaussian noise
        noise = np.random.normal(0, 2)  # Gaussian noise with mean 0 and standard deviation 2
        
        # Anomalies: Occasionally add an anomaly (a sudden large spike)
        anomaly = 50 if np.random.rand() > 0.98 else 0  # 2% chance of an anomaly
        
        # Combine the regular pattern, noise, and possible anomaly
        value = seasonal + noise + anomaly
        
        t += 1
        yield value  # Yield each value as part of the data stream

