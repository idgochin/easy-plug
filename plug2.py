import RPi.GPIO as GPIO
import time

# Pin Definitions
LED2_PIN = 13   # LED 2 connected to GPIO 13
RELAY2_PIN = 20 # Relay 2 connected to GPIO 16

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED2_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RELAY2_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    # Activate LED 2 and Relay 2
    GPIO.output(LED2_PIN, GPIO.HIGH)
    GPIO.output(RELAY2_PIN, GPIO.HIGH)
    print("Relay 2 and LED 2 activated")
    time.sleep(5)  # Keep active for 5 seconds

finally:
    GPIO.output(LED2_PIN, GPIO.LOW)
    GPIO.output(RELAY2_PIN, GPIO.LOW)
    GPIO.cleanup()
