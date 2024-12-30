# import RPi.GPIO as GPIO
# import time

# # Pin configuration
# LED1_PIN = 6  # GPIO pin where the LED is connected

# # GPIO setup
# GPIO.setwarnings(False)  # Disable GPIO warnings
# GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
# GPIO.setup(LED1_PIN, GPIO.OUT)  # Set the pin as an output

# # Blink function
# try:
#     while True:
#         GPIO.output(LED1_PIN, GPIO.HIGH)  # Turn the LED on
#         print("LED ON")
#         time.sleep(0.2)  # Wait 1 second
#         GPIO.output(LED1_PIN, GPIO.LOW)  # Turn the LED off
#         print("LED OFF")
#         time.sleep(0.2)  # Wait 1 second
# except KeyboardInterrupt:
#     print("Program stopped by user")
# finally:
#     GPIO.cleanup()  # Clean up the GPIO configuration

import RPi.GPIO as GPIO
import time
import sys
from threading import Timer

# Pin configuration
LED1_PIN = 6  # GPIO pin where the LED is connected

# GPIO setup
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(LED1_PIN, GPIO.OUT)  # Set the pin as an output

# Exit function after 5 minutes
def exit_program():
    print("Exiting program after 5 minutes.")
    GPIO.cleanup()  # Clean up the GPIO configuration
    sys.exit()

# Set a timer to exit the program after 5 minutes (300 seconds)
exit_timer = Timer(60, exit_program)
exit_timer.start()

# Blink function
try:
    while True:
        GPIO.output(LED1_PIN, GPIO.HIGH)  # Turn the LED on
        print("LED ON")
        time.sleep(0.2)  # Wait 0.2 seconds
        GPIO.output(LED1_PIN, GPIO.LOW)  # Turn the LED off
        print("LED OFF")
        time.sleep(0.2)  # Wait 0.2 seconds
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    exit_timer.cancel()  # Cancel the timer if the program is interrupted
    GPIO.cleanup()  # Clean up the GPIO configuration

