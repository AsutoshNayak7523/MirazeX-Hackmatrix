from flask import Flask, render_template, request, session, jsonify
import random
import smtplib
import serial
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize Serial Communication with Arduino (Change the port accordingly)
ser = serial.Serial('/dev/ttyACM4', 9600, timeout=1)
time.sleep(2)  # Allow time for connection

# Email Configuration (Use your email credentials)
EMAIL_ADDRESS = "ambulancebuzzer@gmail.com"
EMAIL_PASSWORD = "mnjn wiyj qyvg pdhg"

def send_otp(email):
    otp = str(random.randint(1000, 9999))
    session['otp'] = otp  # Store OTP in session

    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, f"Subject: {subject}\n\n{message}")

    return otp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_otp', methods=['POST'])
def send_otp_request():
    email = request.form.get("email")
    if email:
        send_otp(email)
        return jsonify({"status": "OTP Sent"})
    return jsonify({"status": "Error", "message": "Invalid Email"})

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_otp = request.form.get("otp")
    if 'otp' in session and session['otp'] == user_otp:
        ser.write(b"ON\n")  # Send command to turn on buzzer
        return jsonify({"status": "success", "message": "OTP Verified. Buzzer ON!"})
    return jsonify({"status": "error", "message": "Incorrect OTP"})

@app.route('/trip_complete', methods=['POST'])
def trip_complete():
    ser.write(b"OFF\n")  # Send command to turn off buzzer
    return jsonify({"status": "success", "message": "Trip Completed. Buzzer OFF!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5015, debug=True)
