from ROBOT_CONFIGURATIONS import *
from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import *
from EXTERNAL_SENSOR_STREAM import *
from machine import Pin, PWM
import time
from ESP import send_data, get_mac_address

base_speed, turn_speed = user_set_speeds()

base_speed = float(base_speed)
turn_speed = float(turn_speed)

if when_to_trigger() == "White":
    follow_black_line = False
elif when_to_trigger() == "Black":
    follow_black_line = True
else:
    follow_black_line = True

last_error = 0
integral = 0

def off_line_action():
    action = when_triggered()  # Options: "u_turn", "straight", "stop"
    if action == "Take U-Turn":
        robot_axis_right(base_speed, base_speed)
        time.sleep(0)
        
    elif action == "Take Left":
        robot_axis_left(base_speed, base_speed)
        time.sleep(0.0)
        
    elif action == "Take Right":
        robot_axis_right(turn_speed, turn_speed)
        time.sleep(0.0)
        
    elif action == "Stop":
        robot_stop()
        
    else:
        robot_axis_right(turn_speed, turn_speed)
        time.sleep(1)

while True:
    if (str(user_control_method())) == "COM":
        ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()
        left_ir_value, right_ir_value, distance, latitude, longitude, satellites = external_sensor_datas()
        mac_suffix = get_mac_address()
        
        data = [ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude,left_ir_value, right_ir_value, distance, latitude, longitude, satellites, battery_voltage, mac_suffix]
        print(data)
        
    elif (str(user_control_method())) == "TelX":
        send_data()
    
    left_value = int(read_left_ir())
    right_value = int(read_right_ir())
        
    if follow_black_line == True:
        if left_value and not right_value:
            robot_forward(base_speed, turn_speed)
        elif right_value and not left_value:
            robot_forward(turn_speed, base_speed)
        elif left_value and right_value:
            off_line_action()
            integral = 0
        else:
            robot_forward(base_speed, base_speed)
    
    if follow_black_line == False:
        if not left_value and right_value:
            robot_forward(base_speed, turn_speed)
        elif not right_value and left_value:
            robot_forward(turn_speed, base_speed)
        elif not left_value and not right_value:
            off_line_action()
            integral = 0
        else:
            robot_forward(base_speed, base_speed)
    
    time.sleep(0.00000001)



