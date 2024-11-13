from machine import I2C
from mpu6500 import MPU6500
import utime
import math
from ROBOT_ACTIONS import *
from ESP import send_data, get_mac_address
from EXTERNAL_SENSOR_STREAM import *
from ROBOT_CONFIGURATIONS import *
from INTERNAL_SENSOR_STREAM import *


# Initialize I2C
i2c = I2C(1, sda=26, scl=27)  # Update pins if necessary

pitch = 0
roll = 0

# Initialize sensors
mpu_sensor = MPU6500(i2c=i2c)

with open("MPUCorrections.txt", "r") as file:
    data = file.read()  # Read the entire content as a string
    pitch_offset, roll_offset, pitch_correction_factor, roll_correction_factor = map(float, data.split(','))

def calculate_pitch_roll(ax, ay, az, pitch_offset=0, roll_offset=0, pitch_correction_factor=1.0, roll_correction_factor=1.0):
    # Calculate pitch (rotation around X-axis) and roll (rotation around Y-axis)
    pitch = math.atan2(ay, az) * 180 / math.pi - pitch_offset
    roll = math.atan2(-ax, -az) * 180 / math.pi - roll_offset

    # Apply correction factors
    pitch *= pitch_correction_factor
    roll *= roll_correction_factor

    return pitch, roll

# PID variables
integral_error = 0
last_error = 0

# PID constants (fine-tune as necessary)
Kp = 0.02
Kd = 0.10
Ki = 0.00

# Moving average filter for smooth pitch and roll values
def moving_average(new_value, history, length=3):
    history.append(new_value)
    if len(history) > length:
        history.pop(0)
    return sum(history) / len(history)

# Initialize pitch and roll history for filtering
pitch_history = []
roll_history = []

# Scaling factor for converting PID output to duty cycle range

def pid_control(current_value, setpoint=90):
    global integral_error, last_error
    
    # Calculate the PID errors
    error = setpoint + current_value
    integral_error += error
    integral_error = max(min(integral_error, 100), -100)  # Limit the integral to prevent wind-up
    
    derivative_error = error - last_error
    last_error = error
    
    # PID calculation
    output = Kp * error + Ki * integral_error + Kd * derivative_error
    
    # Scale output to the range [0.8, 1]
    # Assuming `output` normally ranges from 0 to 100

    return abs(output*4)


def balance():
    global pitch, roll

    try:
        ax, ay, az = mpu_sensor.acceleration  # Read accelerometer values
        # Calculate pitch and roll with filtering
        pitch_raw, roll_raw = calculate_pitch_roll(ax, ay, az, pitch_offset, roll_offset, pitch_correction_factor, roll_correction_factor)
        
        # Apply moving average filtering
        pitch = moving_average(pitch_raw, pitch_history)
        roll = moving_average(roll_raw, roll_history)
        
        # PID control
        output = pid_control(current_value=roll, setpoint=90)
        
        print(f"PID Output: {output}, Roll: {roll}")

        # Balance control based on roll
        if abs(roll + 90) < 1.5:  # Tolerance for stopping the robot
            robot_stop()
        elif roll > -90:
            # If roll is over 90 degrees, reverse to balance
            robot_reverse(output*1.1, output)
        else:
            # If roll is under 90 degrees, move forward to balance
            robot_forward(output*1.1, output)
            
    except Exception as e:
        print("Error:", e)

# Main loop
while True:
    if (str(user_control_method())) == "COM":
        ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()
        left_ir_value, right_ir_value, distance, latitude, longitude, satellites = external_sensor_datas()
        mac_suffix = get_mac_address()
        
        data = [ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude,left_ir_value, right_ir_value, distance, latitude, longitude, satellites, battery_voltage, mac_suffix]
        print(data)
        
    elif (str(user_control_method())) == "TelX":
        send_data()
        
    balance()
    utime.sleep_ms(50)  # Adjust delay for responsive control (try reducing for more real-time response)
