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

# Store the processes for QR and LED scripts
current_qr_process = None
current_led_process = None
current_qr_process_pay = None

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
    global current_qr_process

    # Turn off the display for a smooth transition
    turn_display_off()
    time.sleep(0.5)  # Wait for the display to power off

    # If a QR code is already being displayed, terminate it
    if current_qr_process and current_qr_process.poll() is None:
        current_qr_process.terminate()
        current_qr_process.wait()
        print("Closed existing QR code window.")

    # Start a new QR code process
    current_qr_process = subprocess.Popen(["python3", "qr.py", "--url", url, "--text", text])
    time.sleep(1)  # Wait for the new QR code to load

    # Turn the display back on
    turn_display_on()
    print(f"Displayed QR code for {text}.")

def run_display_pay(parameter):
    """Run display-pay.py with a specific parameter."""
    global current_qr_process_pay

    # Turn off the display for a smooth transition
    # turn_display_off()
    # time.sleep(0.5)

    # Terminate the current process if it's running
    if current_qr_process_pay and current_qr_process_pay.poll() is None:
        current_qr_process_pay.terminate()
        current_qr_process_pay.wait()
    #     print("Closed existing display-pay.py process.")

    # Start display-pay.py with the specified parameter
    current_qr_process_pay = subprocess.Popen(["python3", "display-pay-update.py", parameter])
    time.sleep(1)  # Wait for the new process to start

    # Turn the display back on
    # turn_display_on()
    print(f"Running display-pay.py with parameter: {parameter}")

def start_led_script(script_name, led_pin):
    """Start the specified LED blinking script."""
    global current_led_process

    if current_led_process and current_led_process.poll() is None:
        print("An LED script is already running.")
        return

    current_led_process = subprocess.Popen(["python3", script_name])
    print(f"Started {script_name} script.")

def stop_led_script():
    """Stop the currently running LED script and turn off LEDs."""
    global current_led_process

    if current_led_process and current_led_process.poll() is None:
        current_led_process.terminate()
        current_led_process.wait()
        print("Stopped LED script.")

    # Ensure both LEDs are turned off
    GPIO.output(LED1_PIN, GPIO.LOW)
    GPIO.output(LED2_PIN, GPIO.LOW)
    print("All LEDs turned off.")

try:
    print("Waiting for button presses...")
    while True:
        if GPIO.input(BUTTON1_PIN) == GPIO.LOW:  # Button 1 pressed
            print("Button 1 pressed!")
            stop_led_script()
            call_qr_script(
                "https://pupa-dev.pea.co.th/pupapay/easyplug/EZP000101", "1"
            )
            start_led_script("led1.py", LED1_PIN)
            run_display_pay("EZP000101")
            time.sleep(0.5)  # Debounce delay
        elif GPIO.input(BUTTON2_PIN) == GPIO.LOW:  # Button 2 pressed
            print("Button 2 pressed!")
            stop_led_script()
            call_qr_script(
                "https://pupa-dev.pea.co.th/pupapay/easyplug/EZP000102", "2"
            )
            start_led_script("led2.py", LED2_PIN)
            time.sleep(0.5)  # Debounce delay
except KeyboardInterrupt:
    print("Exiting program...")

finally:
    # Ensure cleanup of GPIO and subprocess
    GPIO.cleanup()
    if current_qr_process and current_qr_process.poll() is None:
        current_qr_process.terminate()
        current_qr_process.wait()
    if current_led_process and current_led_process.poll() is None:
        current_led_process.terminate()
        current_led_process.wait()
    stop_led_script()  # Ensure LEDs are turned off
    turn_display_on()  # Ensure the display is on when the program exits
