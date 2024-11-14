from ROBOT_CONFIGURATIONS import *
from machine import Pin,PWM, time_pulse_us
import time

#Setting up differences between controlled devices, their upper and lower limits and controlling devices

CONTROLLED_DEVICE_DETAILS = [] #Contains all Controlled devices pin numbers and their upper and lower limits
CONTROLLED_PINS = [] #This will contain only pins numbers from controlled devices to be converted to PWM Pin and excludes any upper or lower servo limit text data

VEHICLE_CONTROLLER_PINS = [] #Contains Pin Numbers of devices which help in controlling the vehicles
MODE_SWITCHES = [] #Contains Pin Number of those input devices which help in changing the mode
CONTROLLER_PINS = [] #This will contain only pins numbers from both vehicle controller pins and mode switches to be converted to PWM Pin

_,VEHICLE_CONTROLLER_PINS, VEHICLE_DEVICE_DETAILS = robot_node_mapping()
_, MODE_SWITCHES,_ = mode_selection()

#Final Controller Pins & Controlled Pins

CONTROLLER_PINS = VEHICLE_CONTROLLER_PINS + MODE_SWITCHES

CONTROLLED_PINS = [VEHICLE_DEVICE_DETAILS[0], VEHICLE_DEVICE_DETAILS[1], VEHICLE_DEVICE_DETAILS[2], VEHICLE_DEVICE_DETAILS[3], VEHICLE_DEVICE_DETAILS[4], VEHICLE_DEVICE_DETAILS[5], VEHICLE_DEVICE_DETAILS[6], VEHICLE_DEVICE_DETAILS[7], VEHICLE_DEVICE_DETAILS[8], VEHICLE_DEVICE_DETAILS[11], VEHICLE_DEVICE_DETAILS[14], VEHICLE_DEVICE_DETAILS[17], VEHICLE_DEVICE_DETAILS[20], VEHICLE_DEVICE_DETAILS[23], VEHICLE_DEVICE_DETAILS[26], VEHICLE_DEVICE_DETAILS[29], VEHICLE_DEVICE_DETAILS[32], VEHICLE_DEVICE_DETAILS[33], VEHICLE_DEVICE_DETAILS[34]]

CONTROLLER_PINS_WITHOUT_NONE = []
CONTROLLED_PINS_WITHOUT_NONE = []

flag = 0

for CONTROLLER_PIN in CONTROLLER_PINS:
    if CONTROLLER_PIN == "NA" or CONTROLLER_PIN == "None":
        CONTROLLER_PINS_WITHOUT_NONE.append(int(28))
    else:
        CONTROLLER_PINS_WITHOUT_NONE.append(int(str(CONTROLLER_PIN)[-2:]))
        
        
for CONTROLLED_PIN in CONTROLLED_PINS:
    if CONTROLLED_PIN == "NA" or CONTROLLED_PIN == "None":
        CONTROLLED_PINS_WITHOUT_NONE.append(int(28))
    else:
        CONTROLLED_PINS_WITHOUT_NONE.append(int(str(CONTROLLED_PIN)[-2:]))        

ALL_CONTROLLERS = [machine.Pin(pin, machine.Pin.IN) for pin in CONTROLLER_PINS_WITHOUT_NONE] #All controller pins including mode switch pins converted to PWM Pin Number style
ALL_CONTROLLED = [machine.Pin(pin, machine.Pin.OUT) for pin in CONTROLLED_PINS_WITHOUT_NONE] #All controlled pins converted to PWM Pin Number style


pwm_values = [1500] * len(ALL_CONTROLLERS + ALL_CONTROLLED)  # Assuming a neutral position

SPEED_PIN_LEFT = PWM(Pin(ALL_CONTROLLED[16]))
SPEED_PIN_RIGHT = PWM(Pin(ALL_CONTROLLED[17]))

SPEED_PIN_LEFT.freq(1000)
SPEED_PIN_RIGHT.freq(1000)

def robot_forward(left_speed, right_speed):
    ALL_CONTROLLED[0].high()
    ALL_CONTROLLED[1].low()
    
    ALL_CONTROLLED[2].high()
    ALL_CONTROLLED[3].low()
    
    ALL_CONTROLLED[4].high()
    ALL_CONTROLLED[5].low()
    
    ALL_CONTROLLED[6].high()
    ALL_CONTROLLED[7].low()
    
    SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))
    SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))


def robot_reverse(left_speed, right_speed):
    ALL_CONTROLLED[0].low()
    ALL_CONTROLLED[1].high()
    
    ALL_CONTROLLED[2].low()
    ALL_CONTROLLED[3].high()
    
    ALL_CONTROLLED[4].low()
    ALL_CONTROLLED[5].high()
    
    ALL_CONTROLLED[6].low()
    ALL_CONTROLLED[7].high()

    SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))
    SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))

def robot_stop():
    ALL_CONTROLLED[0].low()
    ALL_CONTROLLED[1].low()
    
    ALL_CONTROLLED[2].low()
    ALL_CONTROLLED[3].low()
    
    ALL_CONTROLLED[4].low()
    ALL_CONTROLLED[5].low()
    
    ALL_CONTROLLED[6].low()
    ALL_CONTROLLED[7].low()
    
def robot_axis_right(left_speed, right_speed):
    ALL_CONTROLLED[0].high()
    ALL_CONTROLLED[1].low()
    
    ALL_CONTROLLED[2].high()
    ALL_CONTROLLED[3].low()
    
    ALL_CONTROLLED[4].low()
    ALL_CONTROLLED[5].high()
    
    ALL_CONTROLLED[6].low()
    ALL_CONTROLLED[7].high()

    SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))
    SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
    
def robot_axis_left(left_speed, right_speed):
    ALL_CONTROLLED[0].low()
    ALL_CONTROLLED[1].high()
    
    ALL_CONTROLLED[2].low()
    ALL_CONTROLLED[3].high()
    
    ALL_CONTROLLED[4].high()
    ALL_CONTROLLED[5].low()
    
    ALL_CONTROLLED[6].high()
    ALL_CONTROLLED[7].low()

    SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))
    SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
    
def robot_slide_right(left_speed, right_speed):
    ALL_CONTROLLED[0].low()
    ALL_CONTROLLED[1].high()
    
    ALL_CONTROLLED[2].high()
    ALL_CONTROLLED[3].low()
    
    ALL_CONTROLLED[4].high()
    ALL_CONTROLLED[5].low()
    
    ALL_CONTROLLED[6].low()
    ALL_CONTROLLED[7].high()

    SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))
    SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
    
def robot_slide_left(left_speed, right_speed):
    ALL_CONTROLLED[0].high()
    ALL_CONTROLLED[1].low()
    
    ALL_CONTROLLED[2].low()
    ALL_CONTROLLED[3].high()
    
    ALL_CONTROLLED[4].low()
    ALL_CONTROLLED[5].high()
    
    ALL_CONTROLLED[6].high()
    ALL_CONTROLLED[7].low()

    SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))
    SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
    
def run_left_motors_only(left_speed, right_speed):
    ALL_CONTROLLED[0].high()
    ALL_CONTROLLED[1].low()
    
    ALL_CONTROLLED[2].high()
    ALL_CONTROLLED[3].low()
    
    ALL_CONTROLLED[4].low()
    ALL_CONTROLLED[5].low()
    
    ALL_CONTROLLED[6].low()
    ALL_CONTROLLED[7].low()

    SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))
    SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
    
def run_right_motors_only(left_speed, right_speed):
    ALL_CONTROLLED[0].low()
    ALL_CONTROLLED[1].low()
    
    ALL_CONTROLLED[2].low()
    ALL_CONTROLLED[3].low()
    
    ALL_CONTROLLED[4].high()
    ALL_CONTROLLED[5].low()
    
    ALL_CONTROLLED[6].high()
    ALL_CONTROLLED[7].low()

    SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))
    SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
    
def move_steer_1(angle): 
            set_servo_angle(machine.PWM(machine.Pin(ALL_CONTROLLED[8])), angle, CONTROLLED_DEVICE_DETAILS[9], CONTROLLED_DEVICE_DETAILS[10])
            
def move_steer_2(angle):
            set_servo_angle(machine.PWM(machine.Pin(ALL_CONTROLLED[9])), angle, CONTROLLED_DEVICE_DETAILS[12], CONTROLLED_DEVICE_DETAILS[13])
            
def move_shoulder_z(angle):
            set_servo_angle(machine.PWM(machine.Pin(ALL_CONTROLLED[10])), angle, CONTROLLED_DEVICE_DETAILS[15], CONTROLLED_DEVICE_DETAILS[16])
            
def move_shoulder_x(angle):
            set_servo_angle(machine.PWM(machine.Pin(ALL_CONTROLLED[11])), angle, CONTROLLED_DEVICE_DETAILS[18], CONTROLLED_DEVICE_DETAILS[19])
            
def move_elbow(angle):
            set_servo_angle(machine.PWM(machine.Pin(ALL_CONTROLLED[12])), angle, CONTROLLED_DEVICE_DETAILS[21], CONTROLLED_DEVICE_DETAILS[22])
            
def move_wrist(angle):
            set_servo_angle(machine.PWM(machine.Pin(ALL_CONTROLLED[13])), angle, CONTROLLED_DEVICE_DETAILS[24], CONTROLLED_DEVICE_DETAILS[25])
            
def move_gripper_1(angle):
            set_servo_angle(machine.PWM(machine.Pin(ALL_CONTROLLED[14])), angle, CONTROLLED_DEVICE_DETAILS[27], CONTROLLED_DEVICE_DETAILS[28])
            
def move_gripper_2(angle):
            set_servo_angle(machine.PWM(machine.Pin(ALL_CONTROLLED[15])), angle, CONTROLLED_DEVICE_DETAILS[30], CONTROLLED_DEVICE_DETAILS[31])

def read_left_ir():
    left_ir_value = ALL_CONTROLLERS[11].value()
    return left_ir_value

def read_right_ir():
    right_ir_value = ALL_CONTROLLERS[12].value()
    return right_ir_value

def obstacle_distance():
    ALL_CONTROLLED[18].low()
    time.sleep_us(2)
    ALL_CONTROLLED[18].high()
    time.sleep_us(10)
    ALL_CONTROLLED[18].low()

    pulse_duration = time_pulse_us(ALL_CONTROLLERS[13], 1, 30000)  # Wait for echo to go high (max 30ms)
    if pulse_duration < 0:
        return -1

    distance = (pulse_duration * 34300) / 2 / 1000000  # Convert microseconds to seconds, then to cm
    return distance
