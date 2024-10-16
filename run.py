import matplotlib.pyplot as plt
from data_stream import generate_data_stream
from ema import exponential_moving_average
import numpy as np

def main():
    """
    Main function to run real-time data stream processing and EMA-based anomaly detection.
    
    The function sets up the environment to plot a live data stream, computes the Exponential 
    Moving Average (EMA) for the incoming data, and highlights any anomalies detected based on 
    residual thresholds. The plot updates in real-time using Matplotlib.
    """
    
    # Step 1: Get the data stream (infinite generator)
    data_stream = generate_data_stream()

    # Step 2: Set parameters for EMA and anomaly detection
    alpha = 0.1  # Initial smoothing factor for EMA (controls how responsive EMA is to changes)
    k = 2  # Multiplier for anomaly detection threshold (how many standard deviations away is considered an anomaly)
    window_size = 100  # Window size for maintaining the dynamic threshold based on recent data

    # Initialize real-time plot
    plt.ion()  # Interactive mode on for real-time plotting
    fig, ax = plt.subplots(figsize=(10, 6))  # Create figure and axis for plotting

    # Initialize lists to store data for plotting purposes
    time_points = []  # List to store the time steps
    values = []  # List to store the actual values from the data stream
    emas = []  # List to store the computed EMA values
    anomalies = []  # List to store detected anomalies (spikes or dips)

    # Initialize the EMA generator (real-time data processing)
    ema_generator = exponential_moving_average(data_stream, initial_alpha=alpha, k=k, window_size=window_size)

    # Step 3: Process and plot the data in real-time
    for t, value, ema, residual, threshold, is_anomaly in ema_generator:
        """
        Iterate over the data stream and compute the EMA, residual, and dynamic threshold in real time.
        If an anomaly is detected, it is flagged and added to the 'anomalies' list.
        Each step updates the plot with the current data and anomalies.
        
        Parameters yielded from ema_generator:
        t (int): Current time step
        value (float): Current data value
        ema (float): Current EMA value
        residual (float): Difference between the actual value and EMA (used to detect anomalies)
        threshold (float): Dynamic threshold for anomaly detection
        is_anomaly (bool): Flag indicating if the current value is an anomaly
        """
        
        # Store the current data point and its corresponding EMA
        time_points.append(t)
        values.append(value)
        emas.append(ema)

        # If an anomaly is detected, add the anomaly to the list
        if is_anomaly:
            anomalies.append((t, value))

        # Plot the current data stream and EMA
        ax.clear()  # Clear the previous plot to update it with new data
        ax.plot(time_points, values, label="Data Stream", linestyle="--", color="blue")  # Plot the data stream
        # Optionally plot the EMA (commented out, but can be displayed by uncommenting)
        # ax.plot(time_points, emas, label="EMA", color="red")
        
        # Highlight anomalies (if any detected)
        if anomalies:
            # Separate time points and values of detected anomalies
            anomaly_times, anomaly_values = zip(*anomalies)
            # Scatter plot anomalies in red
            ax.scatter(anomaly_times, anomaly_values, color="red", label="Anomalies", zorder=5)

        # Add plot labels, title, and legend
        ax.set_title("Real-Time Data Stream with EMA-Based Anomaly Detection")  # Title for the plot
        ax.set_xlabel("Time")  # Label for the x-axis (time steps)
        ax.set_ylabel("Value")  # Label for the y-axis (data stream values)
        ax.legend()  # Add legend to distinguish between data stream, EMA, and anomalies
        ax.grid(True)  # Add grid for better readability of the plot

        # Pause briefly to allow the plot to refresh (control smoothness of plot updates)
        plt.pause(0.01)  # Short pause between updates (in seconds)

        # Stop after processing 200 points (for testing purposes)
        if t > 200:
            break

    plt.ioff()  # Turn off interactive mode when done
    plt.show()  # Display the final plot after real-time processing ends

# Run the main function
if __name__ == "__main__":
    main()
