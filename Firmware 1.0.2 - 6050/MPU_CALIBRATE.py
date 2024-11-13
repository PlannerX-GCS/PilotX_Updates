from machine import I2C
from mpu6500 import MPU6500
from bmp085 import BMP180
import utime
import math

# Initialize I2C
i2c = I2C(1, sda=26, scl=27)  # Update pins if necessary

# Initialize sensors
mpu_sensor = MPU6500(i2c=i2c)
bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 101325

def calculate_pitch_roll(ax, ay, az):
    """ Calculate pitch and roll from accelerometer data. """
    pitch = math.atan2(ay, math.sqrt(ax**2 + az**2)) * (180 / math.pi)
    roll = math.atan2(ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)
    return pitch, roll

def offset_calculation(count=100):
    """ Capture offsets by averaging pitch and roll values over 'count' samples. """
    pitch_offset = 0.0
    roll_offset = 0.0
    
    for _ in range(count):
        ax, ay, az = mpu_sensor.acceleration  # Read accelerometer values
        pitch, roll = calculate_pitch_roll(ax, ay, az)
        
        pitch_offset += pitch
        roll_offset += roll
        
        utime.sleep_ms(50)  # Small delay between readings
    
    # Average the accumulated offsets
    pitch_offset /= count
    roll_offset /= count
    
    return pitch_offset, roll_offset
        
def corrections(count=50):
    """ Calculate correction factors by comparing sensor readings with expected values. """
    pitch_correction_factor = 0.0
    roll_correction_factor = 0.0

    print("Place the board flat with the X-axis pointing up for pitch correction.")
    utime.sleep(3)
    
    pitch_sum = 0.0
    for _ in range(count):
        ax, ay, az = mpu_sensor.acceleration  # Read accelerometer values
        pitch, _ = calculate_pitch_roll(ax, ay, az)
        pitch_sum += pitch
        utime.sleep_ms(50)
    
    avg_pitch = pitch_sum / count
    pitch_correction_factor = 90 / avg_pitch if avg_pitch != 0 else 1.0  # Avoid division by zero

    print("Place the board flat with the Y-axis pointing up for roll correction.")
    utime.sleep(3)
    
    roll_sum = 0.0
    for _ in range(count):
        ax, ay, az = mpu_sensor.acceleration  # Read accelerometer values
        _, roll = calculate_pitch_roll(ax, ay, az)
        roll_sum += roll
        utime.sleep_ms(50)
    
    avg_roll = roll_sum / count
    roll_correction_factor = 90 / avg_roll if avg_roll != 0 else 1.0  # Avoid division by zero
    
    return pitch_correction_factor, roll_correction_factor

# Main logic
print("Offset calculation starts in 3 seconds. Please keep the board still.")
utime.sleep(3)
pitch_offset, roll_offset = offset_calculation()
print("Offset calculation completed. Pitch offset:", pitch_offset, "Roll offset:", roll_offset)

utime.sleep(1)
print("Correction factor calculation starts in 3 seconds.")
utime.sleep(3)
pitch_correction_factor, roll_correction_factor = corrections()
print("Correction factor calculation completed.")

# Save the results to a file
with open("MPUCorrections.txt", "w") as file:
    data = f"{pitch_offset},{roll_offset},{pitch_correction_factor},{roll_correction_factor}"
    file.write(data)
