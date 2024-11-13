from ROBOT_CONFIGURATIONS import *
from ROBOT_ACTIONS import *
from INTERNAL_SENSOR_STREAM import *
from EXTERNAL_SENSOR_STREAM import *
from machine import Pin, PWM
import time
from ESP import send_data, get_mac_address

Kp, Ki, Kd = PID_values()

Kp = float(Kp)
Ki = float(Ki)
Kd = float(Kd)

base_speed, turn_speed = user_set_speeds()
base_speed = float(base_speed)
turn_speed = float(turn_speed)

last_error = 0
integral = 0

def obstacle_detected():
    action = when_triggered()
    
    distance = obstacle_distance()

    while distance < target_distance:
        
        distance = obstacle_distance()
        
        if action == "Take U-Turn":
            robot_axis_right(base_speed, base_speed)
            
        elif action == "Take Left":
            robot_axis_left(base_speed, base_speed)
            
        elif action == "Take Right":
            robot_axis_right(turn_speed, turn_speed)
            
        elif action == "Stop":
            robot_stop()
            
        else:
            robot_axis_right(turn_speed, turn_speed)

while True:
    if (str(user_control_method())) == "COM":
        ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()
        left_ir_value, right_ir_value, distance, latitude, longitude, satellites = external_sensor_datas()
        mac_suffix = get_mac_address()
        
        data = [ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude,left_ir_value, right_ir_value, distance, latitude, longitude, satellites, battery_voltage, mac_suffix]
        print(data)
        
    elif (str(user_control_method())) == "TelX":
        send_data()
    
    sensor_data = internal_sensor_datas()
    
    distance = obstacle_distance()
    
    # Calculate PID error (for example, distance from obstacle or path deviation)
    target_distance = int(when_to_trigger())  # Define the target trigger distance
    error = abs(distance-target_distance)
    
    # Calculate integral and derivative
    integral += error
    derivative = error - last_error
    last_error = error
    
    # Calculate PID output
    pid_output = (Kp * error) + (Ki * integral) + (Kd * derivative)
    
    # Adjust motor speeds based on PID output
    left_motor_speed = base_speed + pid_output
    right_motor_speed = base_speed + pid_output
        
    # Ensure motor speeds are within valid range (e.g., 0 to maximum speed)
    left_motor_speed = max(0, min(left_motor_speed, base_speed))
    right_motor_speed = max(0, min(right_motor_speed, base_speed))

    if distance == -1:
        pass
    
    elif distance > target_distance:
        print("forward")
        robot_forward(left_motor_speed, right_motor_speed)
    
    elif distance <= target_distance:
        print("detected")
        obstacle_detected()
            
    time.sleep(0.0001)  # Adjust the loop delay for smoother control
