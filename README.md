# Real-Time Anomaly Detection with Exponential Moving Average (EMA)

This project implements an **adaptive Exponential Moving Average (EMA)**-based algorithm to detect anomalies in a time series data stream in real time. It dynamically adjusts the smoothing factor (**alpha**) based on the data, detects spikes and dips, and flags anomalies using an online standard deviation calculation for setting thresholds.

## Overview

The script is designed for real-time anomaly detection, especially in scenarios where data may be subject to **concept drift** (i.e., the data distribution changes over time). The key is to adapt the EMA to react quickly to sudden changes (spikes or dips) while maintaining stability in the face of noise.

### Key Features:

- **Exponential Moving Average (EMA):** The EMA is a widely used technique for smoothing time series data. The script adapts the EMA's smoothing factor (**alpha**) based on the magnitude of changes in the data. When a spike is detected, **alpha** increases, allowing the EMA to react quickly. In contrast, when data stabilizes, **alpha** decreases to smooth out noise.
  
- **Online Mean and Variance Calculation:** The script uses **Welford's algorithm** to incrementally calculate the mean and variance of the residuals (the difference between actual data points and the EMA). This avoids the need to store the entire data history.

- **Dynamic Threshold:** The detection threshold is dynamically calculated as a multiple of the standard deviation of residuals. This threshold is used to identify anomalies, such as spikes (positive anomalies) and dips (negative anomalies).

- **Cool-down Mechanism:** To prevent the detection of consecutive spikes or false positives, a **cool-down period** is introduced after a spike detection.

## How It Works

The algorithm operates in the following steps:

1. **EMA Calculation:** For each new data point, the EMA is updated. If a spike is detected (a significant deviation from the EMA), the algorithm increases the smoothing factor **alpha** to allow the EMA to react more quickly to the change.

2. **Residual Calculation:** The residual is calculated as the difference between the actual data point and the EMA. This residual is used to track deviations from the expected behavior.

3. **Dynamic Threshold Calculation:** The variance of the residuals is calculated in real-time, and the standard deviation is used to set the anomaly detection threshold. This threshold adapts based on the variability of the data.

4. **Anomaly Detection:** If the residual exceeds the threshold (either positively or negatively), an anomaly (spike or dip) is flagged.

5. **Cool-Down Period:** After detecting a spike, the algorithm enters a cool-down period to avoid detecting multiple consecutive spikes as anomalies.

## Code Files

1. **`ema.py`**  
   This file contains the core algorithm for the Exponential Moving Average (EMA) and online mean/variance calculation. It also handles the logic for detecting anomalies based on dynamic thresholds.

2. **`data_stream.py`**  
   This script generates a synthetic data stream that simulates real-world scenarios with a **seasonal pattern**, **random noise**, and occasional **anomalies** (sudden spikes).

## Algorithm Effectiveness

### 1. Responsiveness to Concept Drift
The algorithm's adaptive alpha ensures that the EMA can quickly respond to sudden shifts in the data (e.g., spikes), making it effective in **real-time environments** where the data characteristics may change over time.

### 2. Anomaly Detection
By setting a dynamic threshold based on the variance of residuals, the algorithm can detect **spikes** and **dips** with high sensitivity while avoiding false positives during periods of noise or small fluctuations.

### 3. Scalability
The use of **Welford's algorithm** for online mean and variance calculation ensures the algorithm scales efficiently with large datasets or continuous data streams without needing excessive memory.

## Requirements

- Python 3.x
- `numpy`
- `matplotlib`

You can install the dependencies by running:

```bash
pip install numpy matplotlib
```

## Running the Project

To run the real-time anomaly detection and plot the results:

```bash
python run.py
