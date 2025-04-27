from ROBOT_CONFIGURATIONS import * # This is GE Library which understands which devices are connected where
from ROBOT_ACTIONS import * # This is SA Library which has predefined functions to read from sensors and control motors
from EXTERNAL_SENSOR_STREAM import * #Streams the external data from additional connected sensors
from machine import Pin, PWM, I2C
import time
from pico_i2c_lcd import I2cLcd
from lcd_api import *

##### USER CAN CHANGE THESE SETTINGS TO TUNE IN YOUR ROBOT #####
base_speed = 0.45 # Percentage of power being provided to motors, reduce this if the robot slips forward or backward
timeToMoveForward = 1 # This is the amount of time for which robot moves forward when meets a junction (~ 0.8 to 1)
timeToTakeTurn = 0.3 # This is the amount of time for which robot takes a turn when meets a junction (~ 0.2 to 0.5)

last_turn = "straight"  #This variable remembers the last action happened

i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000) # Declaring an I2C line on which LCD Screen is connected
lcd = I2cLcd(i2c, 39, 2, 16) # Telling the type of configuration for the LCD Screen

#You should put the sequence that robot should follow across junctions
action_list = ['R', 'L', 'L', 'L', 'R', 'R', 'R', 'L']
action_index = 0  # To track the current action in the list

while action_index < len(action_list):  # Continue as long as there are actions in the list
    left_value = int(read_left_ir()) #Reads from left IR Sensor
    right_value = int(read_right_ir()) #Reads from right IR Sensor
        
    if left_value and not right_value: #If Black line is detected on left sensor
        lcd.clear()
        robot_forward(base_speed, 0)  # Left motor runs, right motor stops
        last_turn = "left"
        
    elif right_value and not left_value: #If black line is detected on right sensor
        lcd.clear()
        robot_forward(0, base_speed)  # Right motor runs, left motor stops
        last_turn = "right"
        
    elif left_value and right_value: #If black line is detected on both left & Right sensor
        
        current_action = action_list[action_index] # Both sensors detect the line, perform the next action from the list
        
        # Robot is given some cooldown time to think and avoid any unneccessary action
        robot_stop()
        lcd.putstr("   Thinking...  ")
        time.sleep(1.5)
        lcd.clear()
        
        # The robot now follows the next action item given by you in the list
        if current_action == 'R':
            robot_forward(base_speed, base_speed)
            time.sleep(int(timeToMoveForward))
            robot_axis_left(base_speed, base_speed)  # Turn left
            lcd.putstr("R")
            time.sleep(int(timeToTakeTurn))
            last_turn = "right"
        elif current_action == 'L':
            robot_forward(base_speed, base_speed)
            time.sleep(int(timeToMoveForward))
            robot_axis_right(base_speed, base_speed)  # Turn right
            lcd.putstr("L")
            time.sleep(int(timeToTakeTurn))
            last_turn = "left"        
        
        action_index += 1 #Once this action is completed, next action will be picked next time robot meets an intersection
        
    else:
        lcd.clear()
        # Here the line is lost so it does the last remembered turn
        if last_turn == "left":
            robot_forward(base_speed, 0)  # Keep turning left
        elif last_turn == "right":
            robot_forward(0, base_speed)  # Keep turning right
        else:
            robot_forward(base_speed, base_speed)  # Move straight if no last turn info
    
    time.sleep(0.0000001) #Here we give very minute time to processors to finish pending tasks

# After all actions are completed, stop the robot
robot_stop()
