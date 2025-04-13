import serial
import numpy as np
import matplotlib.pyplot as plt

# Set the Arduino serial port and baud rate (e.g., COM3)
ser = serial.Serial('COM3', 115200)
num_rows = 8
num_cols = 8

plt.ion()
fig, ax = plt.subplots()
im = ax.imshow(np.zeros((num_rows, num_cols)), cmap='hot', vmin=0, vmax=510)
plt.title("8x8 Velostat Pressure Sensor Array (with Offset)")

# Collect the first 10 frames to calculate the offset
print("Offset calibration: Collecting first 10 frames (please do not disturb the sensor).")
calibration_frames = []
while len(calibration_frames) < 10:
    try:
        matrix = []
        for _ in range(num_rows):
            line = ser.readline().decode().strip()
            # Convert comma-separated string into a list of integers
            values = list(map(int, line.split(',')))
            if len(values) == num_cols:
                matrix.append(values)
        if len(matrix) == num_rows:
            calibration_frames.append(np.array(matrix, dtype=np.float32))
    except Exception as e:
        print("Calibration error:", e)

# Compute the offset for each sensor in the array
offset = np.mean(np.array(calibration_frames), axis=0)
print("Calibration complete. Offset array:")
print(offset)

# Main loop: Read sensor data and update the plot after applying the offset correction
while True:
    try:
        matrix = []
        for _ in range(num_rows):
            line = ser.readline().decode().strip()
            values = list(map(int, line.split(',')))
            if len(values) == num_cols:
                matrix.append(values)
        if len(matrix) == num_rows:
            frame = np.array(matrix, dtype=np.float32)
            corrected_frame = frame - offset
            # Clip negative values to 0 (if desired)
            corrected_frame = np.clip(corrected_frame, 0, None)
            im.set_data(corrected_frame)
            plt.draw()
            plt.pause(0.01)
    except Exception as e:
        print("Error:", e)