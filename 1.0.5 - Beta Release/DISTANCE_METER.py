from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from ROBOT_ACTIONS import obstacle_distance
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

prev_distance = 0

while True:
    distance = obstacle_distance()
    if distance == -1:
        lcd.putstr(" Distance To Obj" + "   " + str(prev_distance) + " cm")
    else:
        prev_distance = distance
        lcd.putstr(" Distance To Obj" + "   " + str(distance) + " cm")
    sleep(0.2)
    lcd.clear()
    


