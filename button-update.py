import RPi.GPIO as GPIO
import subprocess
import time

# GPIO configuration
BUTTON1_PIN = 17  # Button 1 on pin 17
BUTTON2_PIN = 18  # Button 2 on pin 18
LED1_PIN = 6  # GPIO pin for LED1
LED2_PIN = 13  # GPIO pin for LED2

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)

# Store the process for display-pay.py
current_display_process = None

def turn_display_off():
    """Turn the display off."""
    subprocess.run(["vcgencmd", "display_power", "0"])
    print("Display turned off.")

def turn_display_on():
    """Turn the display on."""
    subprocess.run(["vcgencmd", "display_power", "1"])
    print("Display turned on.")

def run_display_pay(parameter):
    """Run display-pay.py with a specific parameter."""
    global current_display_process

    # Turn off the display for a smooth transition
    turn_display_off()
    time.sleep(0.5)

    # Terminate the current process if it's running
    if current_display_process and current_display_process.poll() is None:
        current_display_process.terminate()
        current_display_process.wait()
        print("Closed existing display-pay.py process.")

    # Start display-pay.py with the specified parameter
    current_display_process = subprocess.Popen(["python3", "display-pay-update.py", parameter])
    time.sleep(1)  # Wait for the new process to start

    # Turn the display back on
    turn_display_on()
    print(f"Running display-pay.py with parameter: {parameter}")

try:
    print("Waiting for button presses...")
    while True:
        if GPIO.input(BUTTON1_PIN) == GPIO.LOW:  # Button 1 pressed
            print("Button 1 pressed!")
            run_display_pay("EZP000101")
            time.sleep(0.5)  # Debounce delay
        elif GPIO.input(BUTTON2_PIN) == GPIO.LOW:  # Button 2 pressed
            print("Button 2 pressed!")
            run_display_pay("EZP000102")
            time.sleep(0.5)  # Debounce delay
except KeyboardInterrupt:
    print("Exiting program...")
finally:
    # Ensure cleanup of GPIO and subprocess
    GPIO.cleanup()
    if current_display_process and current_display_process.poll() is None:
        current_display_process.terminate()
        current_display_process.wait()
    turn_display_on()  # Ensure the display is on when the program exits
