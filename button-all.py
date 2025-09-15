# import RPi.GPIO as GPIO
# import subprocess
# import time
# import psutil
# from RPLCD.i2c import CharLCD

# # GPIO configuration
# BUTTON1_PIN = 23  # Button 1 on pin 23
# BUTTON2_PIN = 18  # Button 2 on pin 18
# BUTTON3_PIN = 22  # Button 3 on pin 22
# BUTTON4_PIN = 17  # Button 4 on pin 17
# LED1_PIN = 6  # GPIO pin for LED1
# LED2_PIN = 13  # GPIO pin for LED2

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(BUTTON3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(BUTTON4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(LED1_PIN, GPIO.OUT)
# GPIO.setup(LED2_PIN, GPIO.OUT)

# # Store the processes for QR and LED scripts
# current_qr_process = None
# current_led_process = None
# current_qr_process_pay = None

# # Define LCD parameters
# lcd1 = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, charmap='A02')
# lcd2 = CharLCD(i2c_expander='PCF8574', address=0x26, port=1, cols=16, rows=2, charmap='A02')
# lcd3 = CharLCD(i2c_expander='PCF8574', address=0x25, port=1, cols=16, rows=2, charmap='A02')
# lcd4 = CharLCD(i2c_expander='PCF8574', address=0x23, port=1, cols=16, rows=2, charmap='A02')
# lcd1.backlight_enabled = False
# lcd2.backlight_enabled = False
# lcd3.backlight_enabled = False
# lcd4.backlight_enabled = False

# def kill_old_process(script_name):
#     """Kill old process if running."""
#     for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
#         try:
#             if proc.info['cmdline'] and script_name in proc.info['cmdline']:
#                 print(f"Terminating old {script_name} process with PID: {proc.info['pid']}")
#                 proc.terminate()  # Send SIGTERM
#                 proc.wait()  # Ensure it has terminated
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue

# def start_firebase_monitor(script_name):
#     """Kill old process and start read-firebase-plug-all.py."""
#     # script_name = "read-firebase-plug2.py"
    
#     # Kill any existing process
#     kill_old_process(script_name)
    
#     # Start new process
#     subprocess.Popen(["python3", script_name])
#     print(f"Started new {script_name} process.")

# def call_qr_script(url, text):
#     """Call qr.py with specified URL and text."""
#     global current_qr_process

#     # If a QR code is already being displayed, terminate it
#     if current_qr_process and current_qr_process.poll() is None:
#         current_qr_process.terminate()
#         current_qr_process.wait()
#         print("Closed existing QR code window.")

#     # Start a new QR code process
#     current_qr_process = subprocess.Popen(["python3", "qr.py", "--url", url, "--text", text])
#     time.sleep(1)  # Wait for the new QR code to load
#     print(f"Displayed QR code for {text}.")

# def run_display_pay(parameter):
#     """Run display-pay.py with a specific parameter."""
#     global current_qr_process_pay

#     # Terminate the current process if it's running
#     if current_qr_process_pay and current_qr_process_pay.poll() is None:
#         current_qr_process_pay.terminate()
#         current_qr_process_pay.wait()

#     # Start display-pay.py with the specified parameter
#     current_qr_process_pay = subprocess.Popen(["python3", "display-pay-update.py", parameter])
#     time.sleep(1)  # Wait for the new process to start
#     print(f"Running display-pay-update.py with parameter: {parameter}")

# def start_led_script(script_name):
#     """Start the specified LED blinking script."""
#     global current_led_process

#     if current_led_process and current_led_process.poll() is None:
#         print("An LED script is already running.")
#         return

#     current_led_process = subprocess.Popen(["python3", script_name])
#     print(f"Started {script_name} script.")

# def stop_led_script():
#     """Stop the currently running LED script and turn off LEDs."""
#     global current_led_process

#     if current_led_process and current_led_process.poll() is None:
#         current_led_process.terminate()
#         current_led_process.wait()
#         print("Stopped LED script.")

#     # Ensure both LEDs are turned off
#     GPIO.output(LED1_PIN, GPIO.LOW)
#     GPIO.output(LED2_PIN, GPIO.LOW)
#     print("All LEDs turned off.")
    
# def start_blackdisplay_script(script_name):

#     current_led_process = subprocess.Popen(["python3", script_name])
#     print(f"Started {script_name} script.")

# try:
#     start_blackdisplay_script("display35.py")
#     print("Waiting for button presses...")
#     while True:
#         if GPIO.input(BUTTON1_PIN) == GPIO.LOW:  # Button 1 pressed
#             print("Button 1 pressed!")
#             stop_led_script()
#             call_qr_script("https://pupa.pea.co.th/pupapay/easyplug/EZP000101", "Plug 1")
#             start_led_script("led1.py")
#             run_display_pay("EZP000101")
#             start_firebase_monitor("read-firebase-plug1.py")  # Kill old and start new instance
#             time.sleep(0.5)  # Debounce delay

#         elif GPIO.input(BUTTON2_PIN) == GPIO.LOW:  # Button 2 pressed
#             print("Button 2 pressed!")
#             stop_led_script()
#             call_qr_script("https://pupa.pea.co.th/pupapay/easyplug/EZP000102", "Plug 2")
#             start_led_script("led2.py")
#             run_display_pay("EZP000102")
#             start_firebase_monitor("read-firebase-plug2.py")  # Kill old and start new instance
#             time.sleep(0.5)  # Debounce delay

#         elif GPIO.input(BUTTON3_PIN) == GPIO.LOW:  # Button 2 pressed
#             print("Button 3 pressed!")
#             stop_led_script()
#             call_qr_script("https://pupa.pea.co.th/pupapay/easyplug/EZP000103", "Plug 3")
#             start_led_script("led3.py")
#             run_display_pay("EZP000103")
#             start_firebase_monitor("read-firebase-plug3.py")  # Kill old and start new instance
#             time.sleep(0.5)  # Debounce delay

#         elif GPIO.input(BUTTON4_PIN) == GPIO.LOW:  # Button 2 pressed
#             print("Button 4 pressed!")
#             stop_led_script()
#             call_qr_script("https://pupa.pea.co.th/pupapay/easyplug/EZP000104", "Plug 4")
#             start_led_script("led4.py")
#             run_display_pay("EZP000104")
#             start_firebase_monitor("read-firebase-plug4.py")  # Kill old and start new instance
#             time.sleep(0.5)  # Debounce delay

# except KeyboardInterrupt:
#     print("Exiting program...")

# finally:
#     # Cleanup
#     GPIO.cleanup()
#     if current_qr_process and current_qr_process.poll() is None:
#         current_qr_process.terminate()
#         current_qr_process.wait()
#     if current_led_process and current_led_process.poll() is None:
#         current_led_process.terminate()
#         current_led_process.wait()
#     stop_led_script()  # Ensure LEDs are turned off


# import RPi.GPIO as GPIO
# import subprocess
# import time
# import psutil
# import json
# import os
# from RPLCD.i2c import CharLCD

# # GPIO configuration
# BUTTON1_PIN = 23  # Button 1 on pin 23
# BUTTON2_PIN = 18  # Button 2 on pin 18
# BUTTON3_PIN = 22  # Button 3 on pin 22
# BUTTON4_PIN = 17  # Button 4 on pin 17
# LED1_PIN = 6  # GPIO pin for LED1
# LED2_PIN = 13  # GPIO pin for LED2

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(BUTTON3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(BUTTON4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(LED1_PIN, GPIO.OUT)
# GPIO.setup(LED2_PIN, GPIO.OUT)

# # Store the processes for QR and LED scripts
# current_qr_process = None
# current_led_process = None
# current_qr_process_pay = None

# # Define LCD parameters
# lcd1 = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, charmap='A02')
# lcd2 = CharLCD(i2c_expander='PCF8574', address=0x26, port=1, cols=16, rows=2, charmap='A02')
# lcd3 = CharLCD(i2c_expander='PCF8574', address=0x25, port=1, cols=16, rows=2, charmap='A02')
# lcd4 = CharLCD(i2c_expander='PCF8574', address=0x23, port=1, cols=16, rows=2, charmap='A02')
# lcd1.backlight_enabled = False
# lcd2.backlight_enabled = False
# lcd3.backlight_enabled = False
# lcd4.backlight_enabled = False

# # JSON file paths for each plug
# BALANCE_FILES = {
#     1: "balance-plug1.json",
#     2: "balance-plug2.json", 
#     3: "balance-plug3.json",
#     4: "balance-plug4.json"
# }

# def check_plug_status(plug_number):
#     """Check if plug is active by reading JSON file"""
#     try:
#         file_path = BALANCE_FILES.get(plug_number)
#         if not file_path or not os.path.exists(file_path):
#             print(f"Status file {file_path} not found - assuming inactive")
#             return ""
        
#         with open(file_path, 'r') as f:
#             data = json.load(f)
        
#         last_stop_reason = data.get('last_stop_reason', '')
#         print(f"Plug {plug_number} last_stop_reason: {last_stop_reason}")
#         return last_stop_reason
        
#     except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
#         print(f"Error reading status for plug {plug_number}: {e}")
#         return "inactive"  # Default to inactive if error

# def kill_old_process(script_name):
#     """Kill old process if running."""
#     for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
#         try:
#             if proc.info['cmdline'] and script_name in proc.info['cmdline']:
#                 print(f"Terminating old {script_name} process with PID: {proc.info['pid']}")
#                 proc.terminate()  # Send SIGTERM
#                 proc.wait()  # Ensure it has terminated
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue

# def start_firebase_monitor(script_name):
#     """Kill old process and start read-firebase-plug-all.py."""
#     # Kill any existing process
#     kill_old_process(script_name)
    
#     # Start new process
#     subprocess.Popen(["python3", script_name])
#     print(f"Started new {script_name} process.")

# def call_qr_script(url, text):
#     """Call qr.py with specified URL and text."""
#     global current_qr_process

#     # If a QR code is already being displayed, terminate it
#     if current_qr_process and current_qr_process.poll() is None:
#         current_qr_process.terminate()
#         current_qr_process.wait()
#         print("Closed existing QR code window.")

#     # Start a new QR code process
#     current_qr_process = subprocess.Popen(["python3", "qr.py", "--url", url, "--text", text])
#     time.sleep(1)  # Wait for the new QR code to load
#     print(f"Displayed QR code for {text}.")

# def run_display_pay(parameter):
#     """Run display-pay.py with a specific parameter."""
#     global current_qr_process_pay

#     # Terminate the current process if it's running
#     if current_qr_process_pay and current_qr_process_pay.poll() is None:
#         current_qr_process_pay.terminate()
#         current_qr_process_pay.wait()

#     # Start display-pay.py with the specified parameter
#     current_qr_process_pay = subprocess.Popen(["python3", "display-pay-update.py", parameter])
#     time.sleep(1)  # Wait for the new process to start
#     print(f"Running display-pay-update.py with parameter: {parameter}")

# def start_led_script(script_name):
#     """Start the specified LED blinking script."""
#     global current_led_process

#     if current_led_process and current_led_process.poll() is None:
#         print("An LED script is already running.")
#         return

#     current_led_process = subprocess.Popen(["python3", script_name])
#     print(f"Started {script_name} script.")

# def stop_led_script():
#     """Stop the currently running LED script and turn off LEDs."""
#     global current_led_process

#     if current_led_process and current_led_process.poll() is None:
#         current_led_process.terminate()
#         current_led_process.wait()
#         print("Stopped LED script.")

#     # Ensure both LEDs are turned off
#     GPIO.output(LED1_PIN, GPIO.LOW)
#     GPIO.output(LED2_PIN, GPIO.LOW)
#     print("All LEDs turned off.")
    
# def start_blackdisplay_script(script_name):
#     current_led_process = subprocess.Popen(["python3", script_name])
#     print(f"Started {script_name} script.")

# def handle_button_press(plug_number, plug_id, url, led_script, firebase_script):
#     """Handle button press with status checking"""
#     print(f"Button {plug_number} pressed!")
    
#     # Check if plug is already active
#     last_stop_reason = check_plug_status(plug_number)
    
#     if last_stop_reason == "Emergency Button Pressed":
#         set last_stop_reason value in json file to "normal"
#         return
    
#     # Plug is inactive - proceed with normal button action
#     print(f"✅ Plug {plug_number} is inactive - processing button press")
#     stop_led_script()
#     call_qr_script(url, f"Plug {plug_number}")
#     start_led_script(led_script)
#     run_display_pay(plug_id)
#     start_firebase_monitor(firebase_script)

# try:
#     start_blackdisplay_script("display35.py")
#     print("Waiting for button presses...")
#     print("System ready - all plugs available")
    
#     while True:
#         if GPIO.input(BUTTON1_PIN) == GPIO.LOW:  # Button 1 pressed
#             handle_button_press(
#                 plug_number=1,
#                 plug_id="EZP000101", 
#                 url="https://pupa.pea.co.th/pupapay/easyplug/EZP000101",
#                 led_script="led1.py",
#                 firebase_script="read-firebase-plug1.py"
#             )
#             time.sleep(0.5)  # Debounce delay

#         elif GPIO.input(BUTTON2_PIN) == GPIO.LOW:  # Button 2 pressed
#             handle_button_press(
#                 plug_number=2,
#                 plug_id="EZP000102",
#                 url="https://pupa.pea.co.th/pupapay/easyplug/EZP000102", 
#                 led_script="led2.py",
#                 firebase_script="read-firebase-plug2.py"
#             )
#             time.sleep(0.5)  # Debounce delay

#         elif GPIO.input(BUTTON3_PIN) == GPIO.LOW:  # Button 3 pressed
#             handle_button_press(
#                 plug_number=3,
#                 plug_id="EZP000103",
#                 url="https://pupa.pea.co.th/pupapay/easyplug/EZP000103",
#                 led_script="led3.py", 
#                 firebase_script="read-firebase-plug3.py"
#             )
#             time.sleep(0.5)  # Debounce delay

#         elif GPIO.input(BUTTON4_PIN) == GPIO.LOW:  # Button 4 pressed
#             handle_button_press(
#                 plug_number=4,
#                 plug_id="EZP000104",
#                 url="https://pupa.pea.co.th/pupapay/easyplug/EZP000104",
#                 led_script="led4.py",
#                 firebase_script="read-firebase-plug4.py"
#             )
#             time.sleep(0.5)  # Debounce delay

# except KeyboardInterrupt:
#     print("Exiting program...")

# finally:
#     # Cleanup
#     GPIO.cleanup()
#     if current_qr_process and current_qr_process.poll() is None:
#         current_qr_process.terminate()
#         current_qr_process.wait()
#     if current_led_process and current_led_process.poll() is None:
#         current_led_process.terminate()
#         current_led_process.wait()
#     stop_led_script()  # Ensure LEDs are turned off
#     print("System cleanup completed")

import RPi.GPIO as GPIO
import subprocess
import time
import psutil
from RPLCD.i2c import CharLCD

# GPIO configuration
BUTTON1_PIN = 23  # Button 1 on pin 23
BUTTON2_PIN = 18  # Button 2 on pin 18
BUTTON3_PIN = 22  # Button 3 on pin 22
BUTTON4_PIN = 17  # Button 4 on pin 17
LED1_PIN = 6  # GPIO pin for LED1
LED2_PIN = 13  # GPIO pin for LED2

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)

# Store the processes for QR and LED scripts
current_qr_process = None
current_led_process = None
current_qr_process_pay = None

# Define LCD parameters
lcd1 = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, charmap='A02')
lcd2 = CharLCD(i2c_expander='PCF8574', address=0x26, port=1, cols=16, rows=2, charmap='A02')
lcd3 = CharLCD(i2c_expander='PCF8574', address=0x25, port=1, cols=16, rows=2, charmap='A02')
lcd4 = CharLCD(i2c_expander='PCF8574', address=0x23, port=1, cols=16, rows=2, charmap='A02')
lcd1.backlight_enabled = False
lcd2.backlight_enabled = False
lcd3.backlight_enabled = False
lcd4.backlight_enabled = False

def check_internet_connection():
    """Check if internet connection is available using multiple methods."""
    
    # # Method 1: Try to reach Google DNS
    # try:
    #     socket.create_connection(("8.8.8.8", 53), timeout=3)
    #     return True
    # except OSError:
    #     pass
    
    # # Method 2: Try HTTP request to Google
    # try:
    #     response = requests.get("http://www.google.com", timeout=5)
    #     if response.status_code == 200:
    #         return True
    # except (requests.ConnectionError, requests.Timeout):
    #     pass
    
    # Method 3: Try ping to Google DNS
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '3', '8.8.8.8'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return True
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass
    
    return False

def kill_old_process(script_name):
    """Kill old process if running."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and script_name in proc.info['cmdline']:
                print(f"Terminating old {script_name} process with PID: {proc.info['pid']}")
                proc.terminate()  # Send SIGTERM
                proc.wait()  # Ensure it has terminated
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def start_firebase_monitor(script_name):
    """Kill old process and start read-firebase-plug-all.py."""
    # script_name = "read-firebase-plug2.py"
    
    # Kill any existing process
    kill_old_process(script_name)
    
    # Start new process
    subprocess.Popen(["python3", script_name])
    print(f"Started new {script_name} process.")

def call_qr_script(url, text):
    """Call qr.py with specified URL and text."""
    global current_qr_process

    # If a QR code is already being displayed, terminate it
    if current_qr_process and current_qr_process.poll() is None:
        current_qr_process.terminate()
        current_qr_process.wait()
        print("Closed existing QR code window.")

    # Start a new QR code process
    current_qr_process = subprocess.Popen(["python3", "qr.py", "--url", url, "--text", text])
    time.sleep(1)  # Wait for the new QR code to load
    print(f"Displayed QR code for {text}.")

def run_display_pay(parameter):
    """Run display-pay.py with a specific parameter."""
    global current_qr_process_pay

    # Terminate the current process if it's running
    if current_qr_process_pay and current_qr_process_pay.poll() is None:
        current_qr_process_pay.terminate()
        current_qr_process_pay.wait()

    # Start display-pay.py with the specified parameter
    current_qr_process_pay = subprocess.Popen(["python3", "display-pay-update.py", parameter])
    time.sleep(1)  # Wait for the new process to start
    print(f"Running display-pay-update.py with parameter: {parameter}")

def start_led_script(script_name):
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
    
def start_blackdisplay_script(script_name):

    current_led_process = subprocess.Popen(["python3", script_name])
    print(f"Started {script_name} script.")

try:
    start_blackdisplay_script("display35.py")
    # print("Waiting for button presses...")
    while True:
        if check_internet_connection():
            print("Internet connection OK. Waiting for button presses...")
            pass
        else:
            print("No internet connection. Buttons disabled until connection restored.")
            time.sleep(1)
            continue
                
        if GPIO.input(BUTTON1_PIN) == GPIO.LOW:  # Button 1 pressed
            print("Button 1 pressed!")
            subprocess.run(['xset', 'dpms', 'force', 'on'])
            stop_led_script()
            call_qr_script("https://pupa.pea.co.th/pupapay/easyplug/EZP000101", "Plug 1")
            # start_led_script("led1.py")
            run_display_pay("EZP000101")
            start_firebase_monitor("read-firebase-plug1.py")  # Kill old and start new instance
            time.sleep(0.5)  # Debounce delay

        elif GPIO.input(BUTTON2_PIN) == GPIO.LOW:  # Button 2 pressed
            print("Button 2 pressed!")
            subprocess.run(['xset', 'dpms', 'force', 'on'])
            stop_led_script()
            call_qr_script("https://pupa.pea.co.th/pupapay/easyplug/EZP000102", "Plug 2")
            # start_led_script("led2.py")
            run_display_pay("EZP000102")
            start_firebase_monitor("read-firebase-plug2.py")  # Kill old and start new instance
            time.sleep(0.5)  # Debounce delay

        elif GPIO.input(BUTTON3_PIN) == GPIO.LOW:  # Button 2 pressed
            print("Button 3 pressed!")
            subprocess.run(['xset', 'dpms', 'force', 'on'])
            stop_led_script()
            call_qr_script("https://pupa.pea.co.th/pupapay/easyplug/EZP000103", "Plug 3")
            # start_led_script("led3.py")
            run_display_pay("EZP000103")
            start_firebase_monitor("read-firebase-plug3.py")  # Kill old and start new instance
            time.sleep(0.5)  # Debounce delay

        elif GPIO.input(BUTTON4_PIN) == GPIO.LOW:  # Button 2 pressed
            print("Button 4 pressed!")
            subprocess.run(['xset', 'dpms', 'force', 'on'])
            stop_led_script()
            call_qr_script("https://pupa.pea.co.th/pupapay/easyplug/EZP000104", "Plug 4")
            # start_led_script("led4.py")
            run_display_pay("EZP000104")
            start_firebase_monitor("read-firebase-plug4.py")  # Kill old and start new instance
            time.sleep(0.5)  # Debounce delay

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    # Cleanup
    GPIO.cleanup()
    if current_qr_process and current_qr_process.poll() is None:
        current_qr_process.terminate()
        current_qr_process.wait()
    if current_led_process and current_led_process.poll() is None:
        current_led_process.terminate()
        current_led_process.wait()
    stop_led_script()  # Ensure LEDs are turned off

