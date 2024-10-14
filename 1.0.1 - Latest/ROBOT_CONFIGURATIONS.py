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
    # Initialize an empty dictionary
    mapped_port_number = OrderedDict()
    port_number = []
    controllers = []
    controlled = []
    reference = {"A":7, "B":8, "C":9, "D":10, "E":11, "F":12, "G":13, "H":2, "I":3, "J":4, "K":5, "L":6, "M":22}

    # Open the file and read lines
    with open('Node_Mapping_Variables.txt', 'r') as file:
        lines = file.readlines()
        
    # Extract values from each line and populate the dictionary
    for line in lines:
        values = line.strip().split(',')
        for value in values:
            if "RC_3" in str(value):
                port_number.append("THR_"+ str(reference[str(value)[-1:]]))
            elif str(value)[-1:] in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"] and "RC_3" not in str(value):
                port_number.append(reference[str(value)[-1:]])
            elif str(value) == "None":
                port_number.append("NA")
            elif value == "":
                port_number.append(int(0))
            else:
                port_number.append(int(value))
        mapped_port_number["FLM"] = ((port_number[0]), (port_number[1]))
        mapped_port_number["RLM"] = ((port_number[2]), (port_number[3]))
        mapped_port_number["RRM"] = ((port_number[4]), (port_number[5]))
        mapped_port_number["FRM"] = ((port_number[6]), (port_number[7]))
        mapped_port_number["Steer 1"] = ((port_number[8]), (port_number[9]), (port_number[10]))
        mapped_port_number["Steer 2"] = ((port_number[11]), (port_number[12]), (port_number[13]))
        mapped_port_number["Wrist"] = ((port_number[14]), (port_number[15]), (port_number[16]))
        mapped_port_number["Elbow"] = ((port_number[17]), (port_number[18]), (port_number[19]))
        mapped_port_number["Shoulder_Z"] = ((port_number[20]), (port_number[21]), (port_number[22]))
        mapped_port_number["Shoulder_X"] = ((port_number[23]), (port_number[24]), (port_number[25]))
        mapped_port_number["Gripper_1"] = ((port_number[26]), (port_number[27]), (port_number[28]))
        mapped_port_number["Gripper_2"] = ((port_number[29]), (port_number[30]), (port_number[31]))
        mapped_port_number["FB_Controller"] = ((port_number[32]))
        mapped_port_number["Axis_Turn_Controller"] = ((port_number[33]))
        mapped_port_number["Slide_Controller"] = ((port_number[34]))
        mapped_port_number["Steer_1_Controller"] = ((port_number[35]))
        mapped_port_number["Steer_2_Controller"] = ((port_number[36]))
        mapped_port_number["Shoulder_Z_Controller"] = ((port_number[37]))
        mapped_port_number["Shoulder_X_Controller"] = ((port_number[38]))
        mapped_port_number["Elbow_Controller"] = ((port_number[39]))
        mapped_port_number["Wrist_Controller"] = ((port_number[40]))
        mapped_port_number["Gripper_1_Controller"] = ((port_number[41]))
        mapped_port_number["Gripper_2_Controller"] = ((port_number[42]))
        mapped_port_number["Speed_Controller_1"] = ((port_number[43]))
        mapped_port_number["Speed_Controller_2"] = ((port_number[44]))
        mapped_port_number["IR_Left"] = ((port_number[45]))
        mapped_port_number["IR_Right"] = ((port_number[46]))
        mapped_port_number["Trigger"] = ((port_number[47]))
        mapped_port_number["Echo"] = ((port_number[48]))

        
        
        controllers += [port_number[32], port_number[33], port_number[34], port_number[35], port_number[36], port_number[37], port_number[38], port_number[39], port_number[40], port_number[41], port_number[42], port_number[45], port_number[46], port_number[48]]
        controlled += [port_number[i] for i in range(32)]
        controlled += [(port_number[43]), (port_number[44]),  port_number[47]]

    return mapped_port_number, controllers, controlled


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






