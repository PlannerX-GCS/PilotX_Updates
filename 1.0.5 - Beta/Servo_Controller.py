import machine
import time

def additional_servos():
    servos = []
    servos_180 = []
    servos_360 = []
    reference = {"A":7, "B":8, "C":9, "D":10, "E":11, "F":12, "G":13, "H":2, "I":3, "J":4, "K":5, "L":6, "M":22}


    with open('Nodes_Configuration.txt', 'r') as file:
            lines = file.readlines()
            
    for line in lines:
        items = line.split(',')

    # Define the suffixes (A to L)
    suffixes = [chr(i) for i in range(ord('A'), ord('L') + 1)]

    # Process the items and append suffixes, cycling through the list if necessary
    processed_items = [
        f"{item} @{suffixes[i]}" if i < 12 else item
        for i, item in enumerate(items)]
    


    for processed_item in processed_items:
        values = processed_item.strip().split(',')
        for value in values:
            if str(value)[-1:] in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"] and "Servo 180" in str(value):
                servos_180.append(reference[str(value)[-1:]])
            elif str(value)[-1:] in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"] and "Servo 360" in str(value):
                servos_360.append(reference[str(value)[-1:]])
            elif str(value) == "None":
                servos.append("NA")
                
                
    Servo_Motors_180 = [machine.PWM(machine.Pin(pin)) for pin in servos_180]  # For 180° servos
    Servo_Motors_360 = [machine.PWM(machine.Pin(pin)) for pin in servos_360]  # For 360° servos
    print(Servo_Motors_180, Servo_Motors_360)

    for motor in Servo_Motors_180 + Servo_Motors_360:
        motor.freq(50)    
        
    return Servo_Motors_180, Servo_Motors_360

def control_servos(angle):
    Servo_Motors_180, Servo_Motors_360 = additional_servos()
    if 0 <= angle <= 180:
        duty = int((angle / 180) * (16384 - 3277) + 3277)
        for motor in Servo_Motors_180:
            motor.duty_u16(duty)  # Set PWM duty cycle for 180° servo
        for motor in Servo_Motors_360:
            motor.duty_u16(duty)  # Set PWM duty cycle for 180° servo
    else:
        pass
    
control_servos(180)
    

