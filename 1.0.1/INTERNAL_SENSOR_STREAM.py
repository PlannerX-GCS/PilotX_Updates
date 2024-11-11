from machine import I2C
from mpu6500 import MPU6500
from bmp085 import BMP180
import utime
import math

# Initialize I2C
i2c = I2C(1, sda=26, scl=27)  # Update pins if necessary

error_code = 0
pitch = 0
roll = 0
tempC = 0
pres_hPa = 0

# Initialize sensors
mpu_sensor = MPU6500(i2c=i2c)
bmp = BMP180(i2c)
bmp.oversample = 2
bmp.sealevel = 101325

with open("MPUCorrections.txt", "r") as file:
    data = file.read()  # Read the entire content as a string
    pitch_offset, roll_offset, pitch_correction_factor, roll_correction_factor = map(float, data.split(','))


def calculate_pitch_roll(ax, ay, az, pitch_offset, roll_offset, pitch_correction_factor, roll_correction_factor):
    """ Calculate pitch and roll from accelerometer data. """
    pitch = math.atan2(ay, math.sqrt(ax**2 + az**2)) * (180 / math.pi)
    roll = math.atan2(ax, math.sqrt(ay**2 + az**2)) * (180 / math.pi)
    pitch = (pitch+pitch_offset)*pitch_correction_factor
    roll = (roll+roll_offset)*roll_correction_factor
    return pitch, roll

def internal_sensor_datas():
    global error_code, pitch, roll, tempC, pres_hPa, altitude
    try:
        ax, ay, az = mpu_sensor.acceleration  # Read accelerometer values
        gx, gy, gz = mpu_sensor.gyro  # Read gyroscope values
        # Calculate pitch and roll
        pitch, roll = calculate_pitch_roll(ax, ay, az, pitch_offset, roll_offset, pitch_correction_factor, roll_correction_factor)
        
        error_code = 0
        tempC = bmp.temperature    #get the temperature in degree celsius
        pres_hPa = bmp.pressure    #get the pressure in hpa
        altitude = bmp.altitude    #get the altitude
        

        utime.sleep(0.001)  # Delay for 1 second before the next read
    
    except Exception as e:
        error_code = 1
        pitch = 0
        roll = 0
        tempC = 0
        pres_hPa = 0

    return error_code, pitch, roll, tempC, pres_hPa, altitude