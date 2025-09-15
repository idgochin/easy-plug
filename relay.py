import RPi.GPIO as GPIO
import time

# Pin Definitions
LED1_PIN = 6    # LED 1 connected to GPIO 6
LED2_PIN = 13   # LED 2 connected to GPIO 13
RELAY1_PIN = 12 # Relay 1 connected to GPIO 12
RELAY2_PIN = 16 # Relay 2 connected to GPIO 16
RELAY3_PIN = 20 # Relay 3 connected to GPIO 20
RELAY4_PIN = 21 # Relay 4 connected to GPIO 21

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(LED1_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED2_PIN, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(RELAY1_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RELAY2_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RELAY3_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RELAY4_PIN, GPIO.OUT, initial=GPIO.HIGH)

try:
    while True:
        # Activate LED 1
        GPIO.output(LED1_PIN, GPIO.HIGH)
        print("LED 1 ON")
        time.sleep(1)
        
        # Deactivate LED 1 and activate LED 2
        GPIO.output(LED1_PIN, GPIO.LOW)
        GPIO.output(LED2_PIN, GPIO.HIGH)
        print("LED 2 ON")
        time.sleep(1)

        # Activate Relay 1
        GPIO.output(RELAY1_PIN, GPIO.LOW)
        print("Relay 1 ON")
        time.sleep(1)

        # Activate Relay 2
        GPIO.output(RELAY2_PIN, GPIO.LOW)
        print("Relay 2 ON")
        time.sleep(1)

        GPIO.output(RELAY3_PIN, GPIO.LOW)
        print("Relay 3 ON")
        time.sleep(1)

        GPIO.output(RELAY4_PIN, GPIO.LOW)
        print("Relay 4 ON")
        time.sleep(1)

        # Turn off all
        GPIO.output(LED1_PIN, GPIO.LOW)
        GPIO.output(LED2_PIN, GPIO.LOW)
        GPIO.output(RELAY1_PIN, GPIO.HIGH)
        GPIO.output(RELAY2_PIN, GPIO.HIGH)
        GPIO.output(RELAY3_PIN, GPIO.HIGH)
        GPIO.output(RELAY4_PIN, GPIO.HIGH)
        print("All OFF")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    GPIO.cleanup()  # Reset GPIO pins
