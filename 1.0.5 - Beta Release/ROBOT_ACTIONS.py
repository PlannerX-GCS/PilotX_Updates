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

SPEED_PIN_LEFT = PWM(LEFT_MOTOR_SPEED_PINS[0]) if LEFT_MOTOR_SPEED_PINS else None
SPEED_PIN_RIGHT = PWM(RIGHT_MOTOR_SPEED_PINS[0]) if RIGHT_MOTOR_SPEED_PINS else None

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
    try:
        LEFT_MOTORS_PINS[0].low()
        LEFT_MOTORS_PINS[1].high()
        
        RIGHT_MOTORS_PINS[0].low()
        RIGHT_MOTORS_PINS[1].high()
        
        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
    
    except:
        pass


def robot_stop():
    try:
        LEFT_MOTORS_PINS[0].low()
        LEFT_MOTORS_PINS[1].low()
        
        RIGHT_MOTORS_PINS[0].low()
        RIGHT_MOTORS_PINS[1].low()
        
    except:
        pass
        
def robot_axis_right(left_speed, right_speed):
    try:
        LEFT_MOTORS_PINS[0].high()
        LEFT_MOTORS_PINS[1].low()
        
        RIGHT_MOTORS_PINS[0].low()
        RIGHT_MOTORS_PINS[1].high()
        
        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
            
    except:
        pass

    
def robot_axis_left(left_speed, right_speed):
    try:
        LEFT_MOTORS_PINS[0].low()
        LEFT_MOTORS_PINS[1].high()
        
        RIGHT_MOTORS_PINS[0].high()
        RIGHT_MOTORS_PINS[1].low()

        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
            
    except:
        pass
    
def run_left_motors_only(left_speed, right_speed):
    try:
        LEFT_MOTORS_PINS[0].high()
        LEFT_MOTORS_PINS[1].low()
        
        RIGHT_MOTORS_PINS[0].low()
        RIGHT_MOTORS_PINS[1].low()
        
        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
            
    except:
        pass

    
def run_right_motors_only(left_speed, right_speed):
    try:
        LEFT_MOTORS_PINS[0].low()
        LEFT_MOTORS_PINS[1].low()
        
        RIGHT_MOTORS_PINS[0].high()
        RIGHT_MOTORS_PINS[1].low()

        if SPEED_PIN_LEFT:
            SPEED_PIN_LEFT.duty_u16(int(left_speed*65535))

        if SPEED_PIN_RIGHT:
            SPEED_PIN_RIGHT.duty_u16(int(right_speed*65535))
            
    except:
        pass

base_speed, turn_speed = user_set_speeds()

def move_servo(angle):
    try:
        set_servo_angle(machine.PWM(machine.Pin(SERVO_PINS[0])), angle, base_speed, turn_speed)
    
    except:
        pass
            
def read_left_ir():
    try:
        left_ir_value = LEFT_IR_PINS[0].value()
        return left_ir_value
    
    except:
        return 0

def read_right_ir():
    try:
        right_ir_value = RIGHT_IR_PINS[0].value()
        return right_ir_value
    
    except:
        return 0

def obstacle_distance():
    try:
        TRIGGER_PINS[0].low()
        time.sleep_us(2)
        TRIGGER_PINS[0].high()
        time.sleep_us(10)
        TRIGGER_PINS[0].low()

        pulse_duration = time_pulse_us(ECHO_PINS[0], 1, 30000)  # Wait for echo to go high (max 30ms)
        if pulse_duration < 0:
            return -1

        distance = (pulse_duration * 34300) / 2 / 1000000  # Convert microseconds to seconds, then to cm
        return distance
    
    except:
        return -1
    
    
