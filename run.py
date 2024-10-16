import matplotlib.pyplot as plt
from data_stream import generate_data_stream
from ema import exponential_moving_average

def main():
    # Step 1: Get the data stream (infinite generator)
    data_stream = generate_data_stream()

    # Step 2: Run EMA-based anomaly detection on the data stream
    alpha = 0.1  # Smoothing factor for EMA
    k = 2  # Threshold for anomaly detection (number of std deviations)
    results = exponential_moving_average(data_stream, alpha, k)

    # Step 3: Visualize the first 200 points of the stream
    time_points = []
    values = []
    emas = []
    anomalies = []

    for i, (t, value, ema, residual, threshold, is_anomaly) in enumerate(results):
        if i > 200:  # Limit visualization to first 200 points
            break
        time_points.append(t)
        values.append(value)
        emas.append(ema)

        if is_anomaly:
            anomalies.append((t, value))

    # Step 4: Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, values, label="Data Stream", linestyle="--", color="blue")
    plt.plot(time_points, emas, label="EMA", color="red")
    
    # Highlight anomalies
    if anomalies:
        anomaly_times, anomaly_values = zip(*anomalies)
        plt.scatter(anomaly_times, anomaly_values, color="red", label="Anomalies", zorder=5)

    plt.title("Data Stream with EMA-Based Anomaly Detection")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()
