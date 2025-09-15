import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess
import time
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import json
import os
import math
import threading

# Pin Definitions
# LED1_PIN = 6    # LED 1 connected to GPIO 6
RELAY1_PIN = 21 # Relay 1 connected to GPIO 12
BUTTON1_PIN = 17  # Emergency stop button (same as main script)

# GPIO setup
GPIO.setmode(GPIO.BCM)
# GPIO.setup(LED1_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RELAY1_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Emergency stop button

# Global flags for safety systems
emergency_stop = False
overcurrent_stop = False
overcurrent_start_time = None

# Path to your service account key
service_account_key_path = "firebase/serviceAccountKey.json"

# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://easy-plug-bc6ca-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Define the database reference
ref = db.reference('plugs')

# Define LCD parameters
lcd = CharLCD(i2c_expander='PCF8574', address=0x23, port=1, cols=16, rows=2, charmap='A02')

# Configure the Modbus client for the USB to TTL connection
client = ModbusSerialClient(port='/dev/ttyUSB0', baudrate=9600, timeout=1, stopbits=1, bytesize=8, parity='N')

# Balance file paths
BALANCE_FILES = {
    "EZP000101": "balance-plug1.json",
    "EZP000102": "balance-plug2.json",
    "EZP000104": "balance-plug4.json",
}

# Specify the Modbus unit ID (slave address)
UNIT_ID = 4

voltage = 0
energy = 0
current = 0

# Custom characters for Thai text
name0x0 = [0b00000, 0b00000, 0b00000, 0b01111, 0b10001, 0b11101, 0b11001, 0b11001]
name0x1 = [0b00000, 0b00000, 0b00000, 0b00011, 0b00001, 0b01101, 0b00111, 0b00011]
name0x2 = [0b00000, 0b00000, 0b00000, 0b00100, 0b00100, 0b00100, 0b00100, 0b00110]
name0x3 = [0b00000, 0b00000, 0b00000, 0b11011, 0b01001, 0b01011, 0b01101, 0b01001]
name0x4 = [0b00101, 0b11111, 0b00000, 0b01111, 0b10001, 0b00101, 0b01011, 0b01001]
name0x5 = [0b00000, 0b00000, 0b00000, 0b01111, 0b00001, 0b01101, 0b01001, 0b01111]
name0x13 = [0b00000, 0b00000, 0b00000, 0b11010, 0b01010, 0b01010, 0b01111, 0b01011]
name0x14 = [0b00000, 0b00000, 0b00000, 0b01100, 0b00010, 0b00010, 0b00010, 0b00010]
name0x15 = [0b00001, 0b11111, 0b00000, 0b11011, 0b01101, 0b01001, 0b01001, 0b01001]
name1x0 = [0b00000, 0b00000, 0b00000, 0b00100, 0b00100, 0b00100, 0b00110, 0b00110]
name1x1 = [0b01110, 0b11111, 0b00000, 0b01010, 0b10101, 0b10001, 0b10101, 0b11101]
name1x2 = [0b00000, 0b00000, 0b00000, 0b11001, 0b01001, 0b01001, 0b11101, 0b11011]
name1x3 = [0b11110, 0b10010, 0b11010, 0b00010, 0b00010, 0b00010, 0b00011, 0b00011]
name1x4 = [0b11000, 0b01110, 0b00000, 0b11001, 0b01010, 0b01010, 0b01010, 0b01100]

# Create custom characters in the LCD memory
lcd.create_char(0, name1x0)
lcd.create_char(1, name1x1)
lcd.create_char(2, name1x2)
lcd.create_char(3, name1x3)
lcd.create_char(4, name1x4)
lcd.create_char(5, name0x13)
lcd.create_char(6, name0x14)
lcd.create_char(7, name0x15)


# Emergency stop monitoring function (runs in separate thread)
def monitor_emergency_button():
    global emergency_stop
    last_button_time = 0
    
    while not emergency_stop and not overcurrent_stop:
        if GPIO.input(BUTTON1_PIN) == GPIO.LOW:  # Button pressed
            current_time = time.time()
            # Debounce: ignore if pressed within 0.5 seconds
            if current_time - last_button_time > 0.5:
                print("EMERGENCY STOP: Button 4 pressed!")
                emergency_stop = True
                last_button_time = current_time
                break
        time.sleep(0.1)  # Check every 100ms

# Function to read balance from the JSON file
def read_balance_from_file(plug_id):
    file_path = BALANCE_FILES.get(plug_id, "balance-plug4.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return float(data.get("balance", 0.0))
    except (FileNotFoundError, json.JSONDecodeError):
        write_balance_to_file(plug_id, 0.0)
        return 0.0

# Function to write balance to the JSON file
def write_balance_to_file(plug_id, total_price):
    file_path = BALANCE_FILES.get(plug_id, "balance-plug4.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # If total_price is 0, reset the balance completely
    if total_price == 0.0:
        data["balance"] = 0.0
        data["total_price"] = 0.0
        data["plug_status"] = "inactive"
        data["customer"] = ""
    else:
        data["total_price"] = (total_price/60)*0.2  # 1 minute = 0.2 baht

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Function to convert balance to time
def balance_to_time(balance):
    return balance * 300  # 1 unit = 5 minutes (300sec)

def show_screen_text(text):
    """Display text on 3.5 inch screen using screen.py"""
    subprocess.Popen(["python3", "stop-screen.py", "--text", text])
    
# Function to safely shutdown and cleanup
def safe_shutdown(plug_id, reason):
    global emergency_stop, overcurrent_stop
    
    print(f"SHUTDOWN INITIATED: {reason}")
    
    # Turn off all hardware immediately
    # GPIO.output(LED1_PIN, GPIO.LOW)
    GPIO.output(RELAY1_PIN, GPIO.HIGH)
    
    # Clear LCD and turn off backlight
    try:
        lcd.clear()
        lcd.write_string(f"STOPPED: {reason}")
        time.sleep(2)
        lcd.backlight_enabled = False
    except:
        pass
    
    print(f"Hardware safely turned off due to: {reason}")
    
    pay_plug("pay-plug4.py") 
    
    # IMPORTANT: Reset Firebase status to 'inactive' to prevent auto-restart
    try:
        plug_ref = ref.child(plug_id)
        plug_ref.update({
            'status': 'inactive',
            'last_stop_reason': reason,
            'stopped_at': time.time()
        })
        print(f"Firebase status set to 'inactive' for {plug_id}")
    except Exception as e:
        print(f"Error updating Firebase status: {e}")
    
    # Reset balance to 0 to prevent restart
    # try:
    #     write_balance_to_file(plug_id, 0.0)
    #     print("Local balance reset to 0")
    # except Exception as e:
    #     print(f"Error resetting balance: {e}")
    
    # Call inactive script to reset the system
    try:
        show_screen_text(f"PLUG 4\nSTOP")
        subprocess.Popen(["python3", "inactive-plug4.py"])
        print("inactive-plug4.py started successfully")
    except Exception as e:
        print(f"Error starting inactive-plug4.py: {e}")
        
     # Call pay
    # try:
    #     subprocess.Popen(["python3", "inactive-plug1.py"])
    #     print("inactive-plug1.py started successfully")
    # except Exception as e:
    #     print(f"Error starting inactive-plug1.py: {e}")
        
       
    
    print("System reset - waiting for new payment/activation")
    
def start_blackdisplay_script(script_name):
    current_led_process = subprocess.Popen(["python3", script_name])
    print(f"Started {script_name} script.")
    return current_led_process  # คืนค่า process handle หากต้องการ

# Read data and take action
def monitor_plugs():
    global emergency_stop, overcurrent_stop, overcurrent_start_time
    
    try:
        start_blackdisplay_script("display35-auto-exit.py")
        plug_id = "EZP000104"
        remain_time = balance_to_time(read_balance_from_file(plug_id))
        
        # Start emergency button monitoring in separate thread
        emergency_thread = threading.Thread(target=monitor_emergency_button, daemon=True)
        emergency_thread.start()
        print("Emergency stop monitoring started")
        
        start_time = time.monotonic()
        
        while remain_time - (time.monotonic() - start_time) > 0:
            # Check for emergency stop
            if emergency_stop:
                safe_shutdown(plug_id, "Emergency Button Pressed")
                return
            
            # Check for overcurrent stop
            if overcurrent_stop:
                safe_shutdown(plug_id, "Overcurrent Protection")
                return
            
            read_pzem_data()
            
            # Update LCD display
            try:
                lcd.cursor_pos = (0, 0)
                lcd.write_string(f"\x00\x01\x02 {remain_time/60:.2f} \x05\x06\x07")
                lcd.cursor_pos = (1, 0)
                # lcd.write_string(f"\x03\x04 {(time.monotonic() - start_time)/60:.2f} \x05\x06\x07")
                elapsed_seconds = int(time.monotonic() - start_time)
                minutes = elapsed_seconds // 60
                seconds = elapsed_seconds % 60
                lcd.write_string(f"\x03\x04 {minutes:02d}:{seconds:02d} \x05\x06\x07")
            except:
                pass
            
            print(f"Voltage: {voltage}V, Current: {current}A, Time: {time.monotonic() - start_time:.1f}s")
            
            # ENHANCED FEATURE 2: Check for overcurrent with 5-second delay
            if current >= 2.0:
                if overcurrent_start_time is None:
                    # First time detecting overcurrent
                    overcurrent_start_time = time.time()
                    print(f"WARNING: Overcurrent detected {current:.2f}A - monitoring for 5 seconds...")
                else:
                    # Check if overcurrent has persisted for 5 seconds
                    overcurrent_duration = time.time() - overcurrent_start_time
                    print(f"OVERCURRENT CONTINUING: {current:.2f}A for {overcurrent_duration:.1f} seconds")
                    
                    if overcurrent_duration >= 5.0:
                        print(f"OVERCURRENT CUTOFF: {current:.2f}A for {overcurrent_duration:.1f} seconds >= 5.0s")
                        overcurrent_stop = True
                        safe_shutdown(plug_id, f"Overcurrent {current:.2f}A for 5+ seconds")
                        return
                
                # During overcurrent warning, keep hardware running but show warning
                # GPIO.output(LED1_PIN, GPIO.HIGH)  # Keep LED on but could blink as warning
                GPIO.output(RELAY1_PIN, GPIO.LOW)  # Keep relay on
            else:
                # Current is back to normal - reset overcurrent timer
                if overcurrent_start_time is not None:
                    print(f"Current back to normal: {current:.2f}A - resetting overcurrent timer")
                    overcurrent_start_time = None
                
                # Normal operation - activate relay and LED
                # GPIO.output(LED1_PIN, GPIO.HIGH)
                GPIO.output(RELAY1_PIN, GPIO.LOW)
            
            # Update usage cost
            write_balance_to_file(plug_id, (time.monotonic() - start_time))
            
            time.sleep(1)  # Check every second for accurate timing
        
        # Normal time expiration
        print("Time expired - shutting down normally")
        safe_shutdown(plug_id, "Time Expired")
        
    except Exception as e:
        print(f"Error in monitor_plugs: {e}")
        safe_shutdown(plug_id, f"System Error: {e}")

# Function to inactive plug
def inactive_plug(script_name):
    subprocess.Popen(["python3", script_name])
    
# Function to papa pay
def pay_plug(script_name):
    subprocess.Popen(["python3", script_name])

# Function to read and parse all data
def read_pzem_data():
    global voltage, energy, current
    if client.connect():
        try:
            result = client.read_input_registers(address=0x0000, count=10, slave=UNIT_ID)
            
            if isinstance(result, ModbusIOException) or result.isError():
                print(f"Failed to read from device: {result}")
            else:
                voltage = result.registers[0] / 10.0
                current = (result.registers[1] + (result.registers[2] << 16)) / 1000.0
                power = (result.registers[3] + (result.registers[4] << 16)) / 10.0
                energy = result.registers[5] + (result.registers[6] << 16)
                frequency = result.registers[7] / 10.0
                power_factor = result.registers[8] / 100.0
                alarm_status = result.registers[9]

        except Exception as e:
            print(f"Modbus Error: {e}")
        finally:
            client.close()
    else:
        print("Unable to connect to PZEM device")

if __name__ == "__main__":
    try:
        monitor_plugs()
    except KeyboardInterrupt:
        print("Keyboard interrupt - shutting down")
        safe_shutdown("EZP000104", "Manual Stop")
    finally:
        # Final cleanup
        # GPIO.output(LED1_PIN, GPIO.LOW)
        GPIO.output(RELAY1_PIN, GPIO.HIGH)
        try:
            lcd.backlight_enabled = False
        except:
            pass
        print("Final cleanup completed")