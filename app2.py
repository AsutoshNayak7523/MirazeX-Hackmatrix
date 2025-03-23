import cv2
import numpy as np
import tflite_runtime.interpreter as tflite
import serial
import time

# Load the TFLite model
model_path = "model.tflite"  # Update with your actual model path
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Serial connection to Arduino (Update the port if needed)
arduino = serial.Serial('/dev/ttyACM2', 9600, timeout=1)
time.sleep(2)  # Allow some time for the connection

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use your webcam index (0 for default)

# Class Labels (Ensure these match your Teachable Machine labels)
class_labels = ["No Results", "Ambulance", "Traffic Jam", "Vehicle 1", "Vehicle 3", "Vehicle 2", "Vehicle 4"]

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        continue

    # Preprocess the image to match the input size of the model
    input_shape = input_details[0]['shape']
    img = cv2.resize(frame, (input_shape[1], input_shape[2]))  # Resize to model input size
    img = np.expand_dims(img, axis=0)  # Add batch dimension

    # Convert image to required data type (uint8 or float32)
    if input_details[0]['dtype'] == np.uint8:
        img = np.array(img, dtype=np.uint8)  # No normalization
    else:
        img = np.array(img, dtype=np.float32) / 255.0  # Normalize for float models

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Get the predicted class
    predicted_class = np.argmax(output_data)
    label = class_labels[predicted_class]

    print(f"Detected: {label}")

    # Send signal to Arduino
    if label == "Ambulance":
        arduino.write(b'G')  # Turn Green Light ON
    else:
        arduino.write(b'R')  # Turn Red Light ON

    # Display the camera feed
    cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Traffic Light AI", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
arduino.close()
