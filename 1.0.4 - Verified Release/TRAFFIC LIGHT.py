from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from ROBOT_ACTIONS import read_left_ir, read_right_ir
from lcd_api import *

# Initialize I2C and LCD
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 39, 2, 16)

# Display initialization message
lcd.putstr("  Initialising   Traffic Light")
sleep(2)
lcd.clear()
lcd.putstr("VAC SYSTEM READY")
sleep(2)
lcd.clear()
lcd.putstr("VAC")

# Variable to store the last displayed message
last_message = ""

while True:
    left_value = int(read_left_ir())
    right_value = int(read_right_ir())
    
    new_message = ""

    if left_value == 1 and right_value == 1:
        new_message = "STOP"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
        
    elif left_value == 1 and right_value == 0:
        sleep(15)
        new_message = "GO < ^ >"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
        
        sleep(5)
        new_message = "STOP"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message    
        
    elif left_value == 0 and right_value == 1:
        new_message = "STOP"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
    
    
    elif left_value == 0 and right_value == 0:
        sleep(5)
        new_message = "GO < ^ >"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message

        sleep(15)
        new_message = "STOP"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
        
