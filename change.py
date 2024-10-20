import serial
import time

# Function to calculate CRC16 for modbus communication
def calculate_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

# Function to send a command to change the PZEM address
def change_pzem_address(serial_port, new_address):
    if new_address < 1 or new_address > 247:
        raise ValueError("Address must be between 1 and 247")
    
    # Command structure to change PZEM address (modbus frame)
    # Format: [Slave Address, Function Code, Address to Change, CRC16]
    command = [0xF8, 0x06, 0x00, 0x02, 0x00, new_address]
    
    # Calculate CRC for the command
    crc = calculate_crc(command)
    
    # Append CRC to the command (little-endian)
    command.append(crc & 0xFF)
    command.append((crc >> 8) & 0xFF)
    
    # Send the command to the PZEM
    serial_port.write(bytearray(command))
    time.sleep(0.1)  # Wait for the PZEM to process the command
    
    # Read the response (if necessary)
    response = serial_port.read(8)  # Reading the expected response (8 bytes)
    print(f"Response: {response.hex()}")

# Main script to change the address
def main():
    # Open serial connection
    serial_port = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)  # Adjust the port name if necessary
    
    try:
        # Change the address of the PZEM to a new address, e.g., 5
        change_pzem_address(serial_port, new_address=2)
        print("Address change successful.")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Close the serial port
        serial_port.close()

if __name__ == '__main__':
    main()
