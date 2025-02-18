# import RPi.GPIO as GPIO
# import time

# # Pin Definitions
# LED2_PIN = 13   # LED 2 connected to GPIO 13
# RELAY2_PIN = 20 # Relay 2 connected to GPIO 16

# # GPIO setup
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(LED2_PIN, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(RELAY2_PIN, GPIO.OUT, initial=GPIO.LOW)

# try:
#     # Activate LED 2 and Relay 2
#     GPIO.output(LED2_PIN, GPIO.HIGH)
#     GPIO.output(RELAY2_PIN, GPIO.HIGH)
#     print("Relay 2 and LED 2 activated")
#     time.sleep(5)  # Keep active for 5 seconds

# finally:
#     GPIO.output(LED2_PIN, GPIO.LOW)
#     GPIO.output(RELAY2_PIN, GPIO.LOW)
#     GPIO.cleanup()

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

# Pin Definitions
LED1_PIN = 13    # LED 1 connected to GPIO 6
RELAY1_PIN = 20 # Relay 1 connected to GPIO 12

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED1_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RELAY1_PIN, GPIO.OUT, initial=GPIO.LOW)

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
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, charmap='A02')

# Configure the Modbus client for the USB to TTL connection
client = ModbusSerialClient(port='/dev/ttyUSB0', baudrate=9600, timeout=1, stopbits=1, bytesize=8, parity='N')

# Balance file paths
BALANCE_FILES = {
    "EZP000101": "balance-plug1.json",
    "EZP000102": "balance-plug2.json",
}

# Specify the Modbus unit ID (slave address)
UNIT_ID = 2

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
#lcd.create_char(8, name0x15)
#lcd.create_char(9, name1x4)

# Function to read balance from the JSON file
def read_balance_from_file(plug_id):
    file_path = BALANCE_FILES.get(plug_id, "balance-plug2.json")  # Default to plug1.json if unknown
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return float(data.get("balance", 0.0))
    except (FileNotFoundError, json.JSONDecodeError):
        # If file not found or corrupted, create a default balance
        write_balance_to_file(plug_id, 0.0)
        return 0.0

# Function to write balance to the JSON file
def write_balance_to_file(plug_id, balance):
    file_path = BALANCE_FILES.get(plug_id, "balance-plug1.json")  # Default to plug1.json if unknown
    with open(file_path, "w") as file:
        json.dump({"balance": balance}, file)

# Read data and take action
def monitor_plugs():
    try:
        plug_id = "EZP000102"  # Set the plug ID for this script
        balance = read_balance_from_file(plug_id)
        time_no_energy = 0
        use = 0

        last_check_time = time.time()

        while balance - use > 0:
            # Fetch data every 5 seconds without sleep
            if time.time() - last_check_time >= 5:
                last_check_time = time.time()
                
                data = ref.get()
                print("Data from Realtime Database:", data)
                
                if data:
                    plug_data = data.get(plug_id, {})
                    if plug_data.get('status') == 'active':
                        balance = float(plug_data.get('balance', balance))
                        write_balance_to_file(plug_id, balance)

            read_pzem_data()
            lcd.cursor_pos = (0, 0)
            lcd.write_string(f"\x00\x01\x02 {balance} \x05\x06\x07")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"\x03\x04 {balance} \x05\x06\x07")
            print(voltage)
            print(current)
            print(balance)
            print(use)

            # Activate LED 1 and Relay 1
            GPIO.output(LED1_PIN, GPIO.HIGH)
            GPIO.output(RELAY1_PIN, GPIO.HIGH)
            print("Relay 2 and LED 2 activated")

            if current > 0.068:
                time.sleep(1)
                use += 1
                time_no_energy = 0
            else:
                time.sleep(1)
                time_no_energy += 1
                if time_no_energy >= 300:  # 5 minutes
                    print("Energy too low for 5 minutes, stopping device.")
                    break

        lcd.backlight_enabled = False
        print("Balance expired or conditions not met, stopping device.")
        write_balance_to_file(plug_id, 0.0)
        GPIO.output(LED1_PIN, GPIO.LOW)
        GPIO.output(RELAY1_PIN, GPIO.LOW)
        return
    except Exception as e:
        print("Error monitoring plugs:", e)

# Function to read and parse all data
def read_pzem_data():
    global voltage, energy, current  # Update the global voltage variable
    if client.connect():
        try:
            result = client.read_input_registers(address=0x0000, count=10, slave=UNIT_ID)
            
            if isinstance(result, ModbusIOException) or result.isError():
                print(f"Failed to read from the device, result: {result}")
            else:
                # Extract data from registers (assuming common register map)
                voltage = result.registers[0] / 10.0
                current = (result.registers[1] + (result.registers[2] << 16)) / 1000.0
                power = (result.registers[3] + (result.registers[4] << 16)) / 10.0
                energy = result.registers[5] + (result.registers[6] << 16)
                frequency = result.registers[7] / 10.0
                power_factor = result.registers[8] / 100.0
                alarm_status = result.registers[9]

        except Exception as e:
            print(f"Error: {e}")
        finally:
            client.close()
    else:
        print("Unable to connect to the device")

if __name__ == "__main__":
    monitor_plugs()
