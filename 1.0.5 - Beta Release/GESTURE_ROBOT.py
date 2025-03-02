from time import ticks_ms, ticks_diff, sleep
from ROBOT_ACTIONS import *
from pico_i2c_lcd import I2cLcd
from lcd_api import *
from machine import I2C, Pin

start_time_left = None
start_time_right = None
obstacle_trigger_time = None

i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)

lcd = I2cLcd(i2c, 39, 2, 16)

i = 0.5
while i >= 0:
    lcd.backlight_off()
    sleep(i)
    lcd.backlight_on()
    sleep(i)
    i -= 0.05
    
lcd.putstr("  Initialising     Gesture Car")
sleep(2)
lcd.clear()

while True:
    ir_left = read_left_ir()    # Read left IR sensor
    ir_right = read_right_ir()  # Read right IR sensor
    distance = obstacle_distance()
    print(distance)
    
    lcd.move_to(0,0)
    lcd.putstr("Awaiting Gesture    Command")
    lcd.move_to(0,0)
    
    robot_stop()

    if distance<15 and obstacle_trigger_time is None:
        obstacle_trigger_time = ticks_ms()  # Start obstacle timer

    if obstacle_trigger_time is not None:
        elapsed_time = ticks_diff(ticks_ms(), obstacle_trigger_time)

        if 25 <= distance <= 40 and elapsed_time <= 1000:
            lcd.move_to(0,0)
            lcd.putstr("Forward Gesture     Dectected")
            robot_forward(1, 1)
            sleep(2)
            obstacle_trigger_time = None
        elif elapsed_time > 1000:
            obstacle_trigger_time = None

    
    if ir_left == 0 and start_time_left is None:
        start_time_left = ticks_ms() 

    if start_time_left is not None:
        elapsed_time = ticks_diff(ticks_ms(), start_time_left)

        if ir_right == 0 and elapsed_time <= 1000:
            lcd.move_to(0,0)
            lcd.putstr("  Left Gesture     Dectected")
            robot_axis_left(1, 1)  # Move robot left
            sleep(2)  # Give time for the action
            start_time_left = None  # Reset timer
        elif elapsed_time > 1000:
            start_time_left = None  # Reset if time exceeded
    
    ir_left = read_left_ir()    # Read left IR sensor
    ir_right = read_right_ir()  # Read right IR sensor

    if ir_right == 0 and start_time_right is None:
        start_time_right = ticks_ms()  # Start the timer for right

    if start_time_right is not None:
        elapsed_time = ticks_diff(ticks_ms(), start_time_right)

        if ir_left == 0 and elapsed_time <= 1000:
            lcd.move_to(0,0)
            lcd.putstr("  Right Gesture    Dectected")
            robot_axis_right(1, 1)  # Move robot right
            sleep(2)  # Give time for the action
            start_time_right = None  # Reset timer
        elif elapsed_time > 1000:
            start_time_right = None  # Reset if time exceeded

    sleep(0.0001)
