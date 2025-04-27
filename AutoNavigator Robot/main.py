from ROBOT_CONFIGURATIONS import *
from ROBOT_ACTIONS import *
from EXTERNAL_SENSOR_STREAM import *
from machine import Pin, PWM, I2C
import time
from pico_i2c_lcd import I2cLcd
from lcd_api import *

base_speed = 0.45
timeToMoveForward = 1
timeToTakeTurn = 0.3

last_turn = "straight"

i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 39, 2, 16)

action_list = ['R', 'L', 'L', 'L', 'R', 'R', 'R', 'L']

action_index = 0 

while action_index < len(action_list): 
    
    left_value = int(read_left_ir())
    right_value = int(read_right_ir())
        
    if left_value and not right_value:
        lcd.clear()
        robot_forward(base_speed, 0)
        last_turn = "left"
        
    elif right_value and not left_value:
        lcd.clear()
        robot_forward(0, base_speed)  
        last_turn = "right"
        
    elif left_value and right_value: 
        
        current_action = action_list[action_index]
        
        robot_stop()
        lcd.putstr("   Thinking...  ")
        time.sleep(1.5)
        lcd.clear()
        
        if current_action == 'R':
            robot_forward(base_speed, base_speed)
            time.sleep(int(timeToMoveForward))
            robot_axis_left(base_speed, base_speed)
            lcd.putstr("R")
            time.sleep(int(timeToTakeTurn))
            last_turn = "right"
        elif current_action == 'L':
            robot_forward(base_speed, base_speed)
            time.sleep(int(timeToMoveForward))
            robot_axis_right(base_speed, base_speed)
            lcd.putstr("L")
            time.sleep(int(timeToTakeTurn))
            last_turn = "left"        
        
        action_index += 1
        
    else:
        lcd.clear()
        if last_turn == "left":
            robot_forward(base_speed, 0)
        elif last_turn == "right":
            robot_forward(0, base_speed)
        else:
            robot_forward(base_speed, base_speed)
    
    time.sleep(0.0000001)

robot_stop()
