from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
import time
from RPLCD.i2c import CharLCD

# Define LCD parameters
lcd = CharLCD(i2c_expander='PCF8574', address=0x26, port=1, cols=16, rows=2, charmap='A02')

# Configure the Modbus client for the USB to TTL connection
client = ModbusSerialClient(port='/dev/ttyUSB0', baudrate=9600, timeout=1, stopbits=1, bytesize=8, parity='N')

# Specify the Modbus unit ID (slave address)
UNIT_ID = 1

voltage = 0
energy = 0

# Function to read and parse all data
def read_pzem_data():
    global voltage, energy  # Update the global voltage variable
    if client.connect():
        try:
            # Read multiple registers starting from 0x0000 (10 registers for all data)
            # result = client.read_input_registers(0x0000, 10, slave=UNIT_ID)
            result = client.read_input_registers(address=0x0000, count=10, slave=UNIT_ID)
            
            if isinstance(result, ModbusIOException) or result.isError():
                print(f"Failed to read from the device, result: {result}")
            else:
                # Extract data from registers (assuming common register map)
                
                # Voltage (register 0x0000, scale by 10)
                voltage = result.registers[0] / 10.0
                
                # Current (registers 0x0001 and 0x0002 combined, scale by 100)
                current = (result.registers[1] + (result.registers[2] << 16)) / 100.0
                
                # Power (registers 0x0003 and 0x0004 combined, scale by 10)
                power = (result.registers[3] + (result.registers[4] << 16)) / 10.0
                
                # Energy (registers 0x0005 and 0x0006 combined, scale by 1)
                energy = result.registers[5] + (result.registers[6] << 16)
                
                # Frequency (register 0x0007, scale by 10)
                frequency = result.registers[7] / 10.0
                
                # Power factor (register 0x0008, scale by 100)
                power_factor = result.registers[8] / 100.0
                
                # Alarm status (register 0x0009, 0 = no alarm, 1 = alarm)
                alarm_status = result.registers[9]
                
                # Print all values
                # print("pzem1")
                # print(f"Voltage: {voltage} V")
                # print(f"Current: {current} A")
                # print(f"Power: {power} W")
                # print(f"Energy: {energy} Wh")
                # print(f"Frequency: {frequency} Hz")
                # print(f"Power Factor: {power_factor}")
                # print(f"Alarm Status: {alarm_status}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close the connection
            client.close()
    else:
        print("Unable to connect to the device")

# Call the function to read all data
read_pzem_data()
# Print all values
# print("pzem1")
# print(f"Voltage: {voltage} V")
lcd.cursor_pos = (0, 0)
lcd.write_string(f"Voltage: {voltage} V")
lcd.cursor_pos = (1, 0)
lcd.write_string(f"Energy: {energy} Wh")
# time.sleep(5)
