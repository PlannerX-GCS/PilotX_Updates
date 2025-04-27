from ROBOT_ACTIONS import *
from GPS_DATA_STREAM import *

def external_sensor_datas():
    left_ir_value = read_left_ir()
    right_ir_value = read_right_ir()
    
    distance = obstacle_distance()
    
    latitude, longitude, satellites = gps_data()
    
    return left_ir_value, right_ir_value, distance, latitude, longitude, satellites
