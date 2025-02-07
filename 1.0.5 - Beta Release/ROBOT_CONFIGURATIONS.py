from collections import OrderedDict
import machine
import utime

def robot_category():
    with open('Vehicle_Variables.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        values = line.strip().split(',')
    robot_category = values[2]
    
    return robot_category


def robot_node_mapping():

    LEFT_IR = []
    RIGHT_IR = []
    LEFT_MOTORS = []
    RIGHT_MOTORS = []
    LEFT_MOTOR_SPEED = []
    RIGHT_MOTOR_SPEED = []
    ECHO = []
    TRIGGER = []
    SERVO = []
    RGB_RED = []
    RGB_BLUE = []
    RGB_GREEN = []
    RGB_SINGLE = []
    LDR = []
    
    reference = {"A":7, "B":8, "C":9, "D":10, "E":11, "F":12, "G":13, "H":2, "I":3, "J":4, "K":5, "L":6, "M":22}

    # Open the file and read lines
    with open('Nodes_Configuration.txt', 'r') as file:
        lines = file.readlines()
        
    # Extract values from each line and populate the dictionary
    for line in lines:
        values = line.strip().split(',')
        for value in values:
            if "No Connection" in str(value):
                pass
            elif str(value)[-1:] in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]:
                port_number = reference[str(value)[-1:]]
            
                if "Left IR" in value:
                    LEFT_IR.append(port_number)
                elif "Right IR" in value:
                    RIGHT_IR.append(port_number)
                elif "Left DC Motor A1" in value or "Left DC Motor A2" in value:
                    LEFT_MOTORS.append(port_number)
                elif "Right DC Motor B1" in value or "Right DC Motor B2" in value:
                    RIGHT_MOTORS.append(port_number)
                elif "Left DC Motor Speed" in value:
                    LEFT_MOTOR_SPEED.append(port_number)
                elif "Right DC Motor Speed" in value:
                    RIGHT_MOTOR_SPEED.append(port_number)
                elif "Echo" in value:
                    ECHO.append(port_number)
                elif "Trig" in value:
                    TRIGGER.append(port_number)
                elif "Servo" in value:
                    SERVO.append(port_number)
                elif "RGB Red" in value:
                    RGB_RED.append(port_number)
                elif "RGB Blue" in value:
                    RGB_BLUE.append(port_number)
                elif "RGB Green" in value:
                    RGB_GREEN.append(port_number)
                elif "RGB Single" in value:
                    RGB_SINGLE.append(port_number)
                elif "LDR" in value:
                    LDR.append(port_number)
                                                            
    return LEFT_IR, RIGHT_IR, LEFT_MOTORS, RIGHT_MOTORS, LEFT_MOTOR_SPEED, RIGHT_MOTOR_SPEED, ECHO, TRIGGER, SERVO, RGB_RED, RGB_BLUE, RGB_GREEN, RGB_SINGLE, LDR

def mode_selection():
    vehicle_modes = OrderedDict()
    channel_numbers = []
    mode_switches = []
    mode_triggers = []
    reference = {"A":2, "B":3, "C":4, "D":5, "E":6, "F":7, "G":8, "H":9, "I":10, "J":11, "K":12, "L":13, "M":22}

    # Open the file and read lines
    with open('User_Settings.txt', 'r') as file:
        lines = file.readlines()
        
    # Extract values from each line and populate the dictionary
    for line in lines:
        values = line.strip().split(',')
        for value in values:
            if str(value)[-1:] in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]:
                channel_numbers.append(reference[str(value)[-1:]])
            elif value == "":
                channel_numbers.append("NA")
            else:
                channel_numbers.append(str(value))
                
        vehicle_modes["Default"] = (channel_numbers[4], channel_numbers[15])
        vehicle_modes["Route_Planner"] = (channel_numbers[5], channel_numbers[16])
        vehicle_modes["Remote_Control"] = (channel_numbers[6], channel_numbers[17])
        
        mode_switches += [channel_numbers[4], channel_numbers[5], channel_numbers[6]]
        mode_triggers += [channel_numbers[15], channel_numbers[16], channel_numbers[17]]
        
        
    return vehicle_modes, mode_switches, mode_triggers

def start_mode_type():
    with open("User_Settings.txt", "r") as file:
        line = file.readline()
        items = line.strip().split(',')
        
        start_mode = items[21]
        
    return start_mode
        
def user_control_method():
    with open("User_Settings.txt", "r") as file:
        line = file.readline()
        items = line.strip().split(',')
        
    if items[0] == "1":
        controller_type = "COM"
    if items[1] == "1":
        controller_type = "TelX"
    
    return controller_type

def set_servo_angle(pwm, angle, min_angle=None, max_angle=None):
    # If min_angle or max_angle is None, use default values
    min_angle = min_angle if min_angle is not None else 0
    max_angle = max_angle if max_angle is not None else 180
    
    # Ensure the angle is within the specified limits
    angle = max(min(angle, max_angle), min_angle)
    
    # Map the angle to the pulse duration
    pulse_width = int((angle / 180) * 1000) + 1000
    duty = int(pulse_width * 65535 / 20000)
    pwm.duty_u16(duty)
    
def mode_check(channel, string_condition):
    mode = 0
    operator = string_condition[0]
    if string_condition == "" or string_condition == "NA":
        threshold = 0
    else:   
        threshold = int(string_condition[1:])
    
    if operator == "<":
        if int(channel) < threshold:
            mode = 1
    elif operator == ">":
        if int(channel) > threshold:
            mode = 1
    else:
        mode = 0
    
    return mode
    
def mission_execution(filename):
    seq_number = []
    action = []
    time_deg_rad = []
    dist_time = []
    times = []
    auto = []
    steerable = []
    with_previous = []
    rpm = []
    voltage = []
    diameter = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        values = line.strip().split(',')
        seq_number.append(values[0])
        action.append(values[1])
        time_deg_rad.append(values[2])
        dist_time.append(values[3])
        times.append(values[4])
        auto.append(values[5])
        steerable.append(values[6])
        with_previous.append(values[8])
        rpm.append(values[9])
        voltage.append(values[10])
        diameter.append(values[11])
        mission_repeat.append(values[12])
        
    return seq_number, action, time_deg_rad, dist_time, times, auto, steerable, with_previous, rpm[0], voltage[0], diameter[0], mission_repeat[0]

def mode_checking(switch1, switch2, switch3):
    _, _, mode_triggers = mode_selection()
    if mode_check(switch1, str(mode_triggers[0])) == 1:
        drive_mode = "Default"
        
    elif mode_check(switch2, str(mode_triggers[1])) == 1:
        drive_mode = "Route_Planner"
        
    elif mode_check(switch3, str(mode_triggers[2])) == 1:
        drive_mode = "Remote Control"
        
    else:
        drive_mode = "Default"
        
    return drive_mode

def user_set_speeds():
    with open("User_Settings.txt", "r") as file:
        line = file.readline()
        items = line.strip().split(',')
        
        base_speed = items[8]
        turn_speed = items[9]
        
    return base_speed, turn_speed

def PID_values():
    with open("User_Settings.txt", "r") as file:
        line = file.readline()
        items = line.strip().split(',')
        
        KP = items[18]
        KI = items[19]
        KD = items[20]

    return KP, KI, KD

def when_to_trigger():
    with open("User_Settings.txt", "r") as file:
        line = file.readline()
        items = line.strip().split(',')
        
        triggering_point = items[10]

    return triggering_point

def when_triggered():
    with open("User_Settings.txt", "r") as file:
        line = file.readline()
        items = line.strip().split(',')
        
        triggered_point = items[11]

    return triggered_point

def wifi_settings():
    with open("User_Settings.txt", "r") as file:
        line = file.readline()
        items = line.strip().split(',')
        
        password = items[14]
        ip_address = items[16]
        port = items[15]
        latency = items[17]

    return password, port, ip_address, latency

