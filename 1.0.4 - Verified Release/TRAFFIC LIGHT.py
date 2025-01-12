from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from ROBOT_ACTIONS import read_left_ir, read_right_ir
from lcd_api import *

# Initialize I2C and LCD
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 39, 2, 16)

# Initialize LEDs and IR sensors
led_red = Pin(7, Pin.OUT)
led_green = Pin(8, Pin.OUT)
led_blue = Pin(9, Pin.OUT)
ir_left = Pin(13, Pin.IN)
ir_right = Pin(2, Pin.IN)

# LED initialization sequence
led_red.on()
led_green.on()
led_blue.on()

led_red.off()
led_green.on()
led_blue.on()
sleep(1)

led_red.on()
led_green.off()
led_blue.on()
sleep(1)

led_red.on()
led_green.on()
led_blue.off()
sleep(1)

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
    ir_one = ir_right.value()
    ir_two = ir_left.value()
    new_message = ""

    if ir_two == 1 and ir_one == 1:
        new_message = "STOP"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
        led_red.off()
        led_green.on()
        led_blue.on()
        
    elif ir_two == 1 and ir_one == 0:
        sleep(15)
        new_message = "GO < ^ >"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
        led_red.on()
        led_green.off()
        led_blue.on()
        sleep(5)
        new_message = "STOP"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
        led_red.off()
        led_green.on()
        led_blue.on()
    
        
    elif ir_two == 0 and ir_one == 1:
        new_message = "STOP"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
        led_red.off()
        led_green.on()
        led_blue.on()
    
    elif ir_two == 0 and ir_one == 0:
        sleep(5)
        new_message = "GO < ^ >"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
        led_red.on()
        led_green.off()
        led_blue.on()
        sleep(15)
        new_message = "STOP"
        if new_message != last_message:
            lcd.clear()
            lcd.putstr(new_message)
            last_message = new_message
        led_red.off()
        led_green.on()
        led_blue.on()