from INTERNAL_SENSOR_STREAM import internal_sensor_datas
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

lcd.putstr("  Initialising    Inclinometer")
sleep(2)
lcd.clear()

count = 0

while True:
    data = internal_sensor_datas()
    pitch, roll = data[7], data[8]
    lcd.putstr(" X_Tilt: " + str(round(pitch,1)) + "     Y_Tilt: " + str(round(roll,1)))
    sleep(0.2)
    lcd.clear()
    



