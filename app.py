import numpy as np
import pyaudio
import serial
import tensorflow.lite as tflite
import wave

# Set up the serial connection (update the port accordingly)
arduino = serial.Serial("COM11", 9600)  # Change COM3 to the correct port

# Load Teachable Machine model
interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 1  # Duration of each sample
p = pyaudio.PyAudio()

def get_audio_features():
    """Captures real-time audio and returns it as a feature array."""
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []
    
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()

    # Convert to numpy array
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    audio_data = np.array(audio_data, dtype=np.float32) / np.iinfo(np.int16).max  # Normalize

    return np.expand_dims(audio_data, axis=0)  # Reshape to match model input

def classify_audio():
    """Runs the Teachable Machine model on the recorded audio."""
    features = get_audio_features()
    interpreter.set_tensor(input_details[0]['index'], features)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]

    class_index = np.argmax(predictions)
    return class_index

while True:
    class_id = classify_audio()

    if class_id == 0:  # Background Noise
        print("Ambulance Buzzer detected - Green Light ON")
        arduino.write(b'R')
    elif class_id == 1:  # Ambulance Buzzer
        print("Background Noise detected - Red Light ON")
        arduino.write(b'G')
