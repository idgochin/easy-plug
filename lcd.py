import smbus2
import time
from RPLCD.i2c import CharLCD

# Define LCD parameters
lcd = CharLCD(i2c_expander='PCF8574', address=0x23, port=1, cols=16, rows=2, charmap='A02')

# Initialize and display text
lcd.write_string('Hello, World!')
time.sleep(5)
lcd.clear()
lcd.write_string('Raspberry Pi 4')

time.sleep(2)
