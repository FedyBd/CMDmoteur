# Import the required libraries
from flask import Flask
import RPi.GPIO as GPIO

# Create the Flask app
app = Flask(__name__)

# Set up GPIO mode and motor pins
GPIO.setmode(GPIO.BCM)
motor_pin = 17
GPIO.setup(motor_pin, GPIO.OUT)

# Define routes to control the motor
@app.route('/forward')
def forward():
    GPIO.output(motor_pin, GPIO.HIGH)  # Turn the motor forward
    return 'Motor moving forward'

@app.route('/stop')
def stop():
    GPIO.output(motor_pin, GPIO.LOW)  # Stop the motor
    return 'Motor stopped'

# Run the app on port 5000 (you can choose a different port if needed)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
