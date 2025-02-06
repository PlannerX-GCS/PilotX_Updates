from ROBOT_CONFIGURATIONS import *
from machine import Pin,PWM, time_pulse_us
import time

LEFT_IR, RIGHT_IR, LEFT_MOTORS, RIGHT_MOTORS, LEFT_MOTOR_SPEED, RIGHT_MOTOR_SPEED, ECHO, TRIGGER, SERVO, RGB_RED, RGB_BLUE, RGB_GREEN, RGB_SINGLE, LDR = robot_node_mapping()

LEFT_IR_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in LEFT_IR if pin]
RIGHT_IR_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in RIGHT_IR if pin]

LEFT_MOTORS_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in LEFT_MOTORS if pin]
RIGHT_MOTORS_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RIGHT_MOTORS if pin]

LEFT_MOTOR_SPEED_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in LEFT_MOTOR_SPEED if pin]
RIGHT_MOTOR_SPEED_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RIGHT_MOTOR_SPEED if pin]

ECHO_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in ECHO if pin]
TRIGGER_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in TRIGGER if pin]

SERVO_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in SERVO if pin]

RGB_RED_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RGB_RED if pin]
RGB_BLUE_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RGB_BLUE if pin]
RGB_GREEN_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RGB_GREEN if pin]
RGB_SINGLE_PINS = [machine.Pin(int(pin), machine.Pin.OUT) for pin in RGB_SINGLE if pin]

LDR_PINS = [machine.Pin(int(pin), machine.Pin.IN) for pin in LDR if pin]

SPEED_PIN_LEFT = PWM(LEFT_MOTOR_SPEED_PINS) if LEFT_MOTOR_SPEED_PINS else None
SPEED_PIN_RIGHT = PWM(RIGHT_MOTOR_SPEED_PINS) if RIGHT_MOTOR_SPEED_PINS else None

if SPEED_PIN_LEFT:
    SPEED_PIN_LEFT.freq(1000)

if SPEED_PIN_RIGHT:
    SPEED_PIN_RIGHT.freq(1000)

def robot_forward(left_speed, right_speed):
    LEFT_MOTORS_PINS[0].high()
    LEFT_MOTORS_PINS[1].low()
    
    RIGHT_MOTORS_PINS[0].high()
    RIGHT_MOTORS_PINS[1].low()

    if SPEED_PIN_LEFT:
        SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

    if SPEED_PIN_RIGHT:
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
