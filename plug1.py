import RPi.GPIO as GPIO
import time

# Pin Definitions
LED1_PIN = 6    # LED 1 connected to GPIO 6
RELAY1_PIN = 12 # Relay 1 connected to GPIO 12

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RELAY1_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    # Activate LED 1 and Relay 1
    GPIO.output(LED1_PIN, GPIO.HIGH)
    GPIO.output(RELAY1_PIN, GPIO.HIGH)
    print("Relay 1 and LED 1 activated")
    time.sleep(5)  # Keep active for 5 seconds

finally:
    GPIO.output(LED1_PIN, GPIO.LOW)
    GPIO.output(RELAY1_PIN, GPIO.LOW)
    GPIO.cleanup()
