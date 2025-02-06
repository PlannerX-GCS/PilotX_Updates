from ROBOT_ACTIONS import *
from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from lcd_api import *

i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)

lcd = I2cLcd(i2c, 39, 2, 16)

i = 0.5
while i >= 0:
    lcd.backlight_off()
    sleep(i)
    lcd.backlight_on()
    sleep(i)
    i -= 0.05

lcd.putstr("  Initialising       Sensor")
sleep(2)
lcd.clear()

count = 0

while True:
    val = read_right_ir()
    val2 = read_left_ir()
    
    if val == 0 or val2 == 0:
        count = count + 1
    else:
        count = count
        
    lcd.putstr(" Objects Passed" + "        " + str(count))
    sleep(0.2)
    lcd.clear()
    


