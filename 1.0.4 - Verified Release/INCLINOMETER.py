from INTERNAL_SENSOR_STREAM import *
from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from lcd_api import *

i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 39, 2, 16)

# Display initialization message
lcd.putstr("  Initialising  ")
lcd.move_to(0, 1)
lcd.putstr("  Inclinometer  ")
sleep(2)

lcd.clear()

# Display calibration message
lcd.putstr("  Calibrating  ")
lcd.move_to(0, 1)
lcd.putstr("Keep sensor flat")

# Collect samples for 4 seconds
calibration_duration = 4  # Calibration period in seconds
sample_interval = 0.1     # Interval between samples (in seconds)
samples = int(calibration_duration / sample_interval)

pitch_sum = 0
roll_sum = 0

for i in range(samples):
    # Fetch sensor data
    ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()
    
    # Accumulate pitch and roll values
    pitch_sum += pitch
    roll_sum += roll
    
    # Optional: Show a progress bar on the LCD
    lcd.move_to(0, 1)
    lcd.putstr("Calibrating {}% ".format(int((i + 1) / samples * 100)))
    sleep(sample_interval)

# Calculate offsets as the average of the sampled values
offset_pitch = pitch_sum / samples
offset_roll = roll_sum / samples

# Clear LCD after calibration
lcd.clear()
lcd.putstr("Calibration Done")
sleep(2)

lcd.clear()

# Main loop to display tilt values
while True:
    # Fetch sensor data
    ax, ay, az, gx, gy, gz, error_code, pitch, roll, tempC, pres_hPa, altitude, battery_voltage = internal_sensor_datas()

    # Calculate relative tilt values
    x_tilt = int(pitch - offset_pitch)
    y_tilt = int(roll - offset_roll)

    # Display tilt values on the LCD
    lcd.move_to(0, 0)
    lcd.putstr("X-Tilt: {:>3}".format(x_tilt))  # Format for alignment
    lcd.move_to(0, 1)
    lcd.putstr("Y-Tilt: {:>3}".format(y_tilt))

    sleep(0.5)

