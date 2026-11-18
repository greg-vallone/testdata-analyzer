
import numpy as np
import pandas as pd

# -----------------------------------------
# Configuration
# -----------------------------------------
np.random.seed(42)

sample_rate = 1                 # Hz
duration = 600                  # seconds
num_samples = sample_rate * duration

time = np.arange(num_samples)

# -----------------------------------------
# Generate simulated sensor signals
# -----------------------------------------
data = {
    "Time_s": time
}

sensor_config = [
    # Name, baseline, amplitude, noise, drift, decimals
    ("Temperature_C", 25.0, 2.5, 0.15, 0.002, 2),
    ("Pressure_bar", 5.2, 0.4, 0.025, 0.0005, 3),
    ("Flow_L_min", 120.0, 15.0, 1.2, 0.01, 2),
    ("Vibration_mm_s", 3.5, 1.0, 0.12, 0.001, 3),
    ("Voltage_V", 230.0, 2.0, 0.25, 0.001, 2),
    ("Current_A", 12.0, 1.5, 0.10, 0.0005, 3),
    ("Humidity_pct", 45.0, 5.0, 0.4, 0.003, 1),
    ("Speed_RPM", 1500.0, 80.0, 5.0, 0.05, 1),
    ("Torque_Nm", 85.0, 12.0, 1.0, 0.01, 2),
    ("Acceleration_m_s2", 0.0, 2.0, 0.2, 0.0001, 4),
    ("Displacement_mm", 10.0, 1.5, 0.08, 0.001, 3),
    ("Power_kW", 18.0, 3.0, 0.3, 0.005, 2),
    ("Conductivity_mS", 1.8, 0.3, 0.025, 0.0002, 4),
    ("Level_pct", 65.0, 8.0, 0.5, -0.005, 2)
]

for name, baseline, amplitude, noise, drift, decimals in sensor_config:

    # Different frequency for each sensor
    frequency = np.random.uniform(0.002, 0.03)

    # Periodic signal
    periodic = amplitude * np.sin(
        2 * np.pi * frequency * time
    )

    # Additional low-frequency variation
    secondary = (amplitude * 0.2) * np.sin(
        2 * np.pi * frequency * 0.3 * time
        + np.random.uniform(0, 2 * np.pi)
    )

    # Random measurement noise
    random_noise = np.random.normal(
        0, noise, num_samples
    )

    # Gradual linear drift
    sensor_drift = drift * time

    # Occasional transient events
    transient = np.zeros(num_samples)

    for _ in range(3):
        event_time = np.random.randint(50, num_samples - 50)
        event_duration = np.random.randint(5, 20)
        event_magnitude = np.random.uniform(
            -amplitude * 0.5,
            amplitude * 0.5
        )

        end_time = min(
            event_time + event_duration,
            num_samples
        )

        transient[event_time:end_time] += event_magnitude

    # Combine all signal components
    signal = (
        baseline
        + periodic
        + secondary
        + random_noise
        + sensor_drift
        + transient
    )

    # Apply sensor-specific decimal precision
    data[name] = np.round(signal, decimals)

# -----------------------------------------
# Create DataFrame
# -----------------------------------------
df = pd.DataFrame(data)

# -----------------------------------------
# Export to CSV
# -----------------------------------------
filename = "simulated_sensor_data.csv"

df.to_csv(filename, index=False)

# -----------------------------------------
# Display dataset information
# -----------------------------------------
print("CSV file successfully generated!")
print(f"Filename: {filename}")
print(f"Number of samples: {len(df)}")
print(f"Number of columns: {len(df.columns)}")
print(f"Sampling frequency: {sample_rate} Hz")
print(f"Recording duration: {duration} seconds")

print("\nFirst 10 rows:")
print(df.head(10))

print("\nDataset statistics:")
print(df.describe())
