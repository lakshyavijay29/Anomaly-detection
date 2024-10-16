import numpy as np

def generate_data_stream():
    """
    Infinite generator function that simulates a real-time data stream. 
    The data stream consists of a seasonal sine wave pattern with added noise and occasional anomalies.

    The generator produces values indefinitely, making it suitable for use in real-time processing systems.
    
    Data stream components:
    - Seasonal Pattern: A repeating sine wave simulates periodic behavior over a 50-time-step cycle.
    - Noise: Random Gaussian noise simulates random fluctuations around the pattern.
    - Anomalies: Occasional large spikes occur with a small probability (2%), simulating sudden unusual events.
    
    Yields:
        float: The current value in the data stream, combining the regular pattern, noise, and possible anomaly.
    """
    
    t = 0  # Initialize time step
    
    while True:
        # Regular pattern: simulate a seasonal sine wave pattern
        # This sine wave has an amplitude of 10 and a period of 50 time steps
        seasonal = 10 * np.sin(2 * np.pi * t / 100)  
        
        # Noise: add random Gaussian noise
        # Gaussian noise with mean 0 and standard deviation 1 to simulate small random variations
        noise = np.random.normal(0, 2)  
        
        # Anomalies: Occasionally add an anomaly (a sudden large spike)
        # There is a 2% chance of generating a large anomaly with a value of 50
        anomaly = 50 if np.random.rand() > 0.98 else 0  
        
        # Combine the regular pattern, noise, and possible anomaly
        value = seasonal + noise + anomaly  # Final value is the sum of the three components
        
        t += 1  # Increment the time step for the next iteration
        
        # Yield each generated value as part of the data stream
        yield value  # Returns the current value and suspends execution until the next value is requested
