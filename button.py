import RPi.GPIO as GPIO
import subprocess
import time

# GPIO configuration
BUTTON1_PIN = 17  # Button 1 on pin 17
BUTTON2_PIN = 18  # Button 2 on pin 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Store the process for the currently running QR code
current_process = None

def turn_display_off():
    """Turn the display off."""
    subprocess.run(["vcgencmd", "display_power", "0"])
    print("Display turned off.")

def turn_display_on():
    """Turn the display on."""
    subprocess.run(["vcgencmd", "display_power", "1"])
    print("Display turned on.")

def call_qr_script(url, text):
    """Call qr.py with specified URL and text."""
    global current_process

    # Turn off the display for a smooth transition
    turn_display_off()
    time.sleep(0.5)  # Wait for the display to power off

    # If a QR code is already being displayed, terminate it
    if current_process and current_process.poll() is None:  # Check if process is running
        current_process.terminate()
        current_process.wait()  # Ensure the process is terminated
        print("Closed existing QR code window.")

    # Start a new QR code process
    current_process = subprocess.Popen(["python3", "qr.py", "--url", url, "--text", text])
    time.sleep(1)  # Wait for the new QR code to load

    # Turn the display back on
    turn_display_on()
    print(f"Displayed QR code for {text}.")

try:
    print("Waiting for button presses...")
    while True:
        if GPIO.input(BUTTON1_PIN) == GPIO.LOW:  # Button 1 pressed
            print("Button 1 pressed!")
            call_qr_script(
                "https://pupa-dev.pea.co.th/pupapay/easyplug/EZP000101", "1"
            )
            time.sleep(0.5)  # Debounce delay
        elif GPIO.input(BUTTON2_PIN) == GPIO.LOW:  # Button 2 pressed
            print("Button 2 pressed!")
            call_qr_script(
                "https://pupa-dev.pea.co.th/pupapay/easyplug/EZP000102", "2"
            )
            time.sleep(0.5)  # Debounce delay
except KeyboardInterrupt:
    print("Exiting program...")

finally:
    # Ensure cleanup of GPIO and subprocess
    GPIO.cleanup()
    if current_process and current_process.poll() is None:
        current_process.terminate()
        current_process.wait()
    turn_display_on()  # Ensure the display is on when the program exits
