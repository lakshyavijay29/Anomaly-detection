import matplotlib.pyplot as plt
from data_stream import generate_data_stream
from ema import exponential_moving_average
import numpy as np

def main():
    # Step 1: Get the data stream (infinite generator)
    data_stream = generate_data_stream()

    # Step 2: Set parameters for EMA and anomaly detection
    alpha = 0.1  # Smoothing factor for EMA
    k = 2  # Threshold for anomaly detection (number of std deviations)
    window_size = 100  # Window size for the dynamic threshold

    # Initialize real-time plot
    plt.ion()  # Turn on interactive mode for real-time plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Initialize lists to store points for plotting
    time_points = []
    values = []
    emas = []
    anomalies = []

    # Initialize the EMA generator for real-time processing
    ema_generator = exponential_moving_average(data_stream, initial_alpha=alpha, k=k, window_size=window_size)

    # Step 3: Process and plot the data in real-time
    for t, value, ema, residual, threshold, is_anomaly in ema_generator:
        # Store the current data point and EMA
        time_points.append(t)
        values.append(value)
        emas.append(ema)

        # If an anomaly is detected, store the anomaly
        if is_anomaly:
            anomalies.append((t, value))

        # Plot the current data stream and EMA
        ax.clear()  # Clear the previous plot
        ax.plot(time_points, values, label="Data Stream", linestyle="--", color="blue")
        ax.plot(time_points, emas, label="EMA", color="red")
        
        # Highlight anomalies
        if anomalies:
            anomaly_times, anomaly_values = zip(*anomalies)
            ax.scatter(anomaly_times, anomaly_values, color="red", label="Anomalies", zorder=5)

        # Add plot details
        ax.set_title("Real-Time Data Stream with EMA-Based Anomaly Detection")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True)

        # Pause briefly to allow the plot to update
        plt.pause(0.01)  # Adjust the pause interval for smoothness of updates

        # Stop after plotting the first 200 points (for testing purposes)
        if t > 200:
            break

    plt.ioff()  # Turn off interactive mode when done
    plt.show()  # Show the final plot

# Run the main function
if __name__ == "__main__":
    main()
