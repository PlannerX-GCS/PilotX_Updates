from ROBOT_CONFIGURATIONS import robot_category

if robot_category() == "-1":
    pass

if robot_category() == "0":
    exec(open("/LINE_FOLLOWER.py").read())
    
elif robot_category() == "1":
    exec(open("/OBSTACLE_AVOIDER.py").read())
    
elif robot_category() == "2":
    exec(open("/DISTANCE_METER.py").read())

elif robot_category() == "3":
    exec(open("/INCLINOMETER.py").read())

elif robot_category() == "4":
    exec(open("/TRAFFIC_LIGHT.py").read())

elif robot_category() == "5":
    exec(open("/DIGITAL_TEMPERATURE_METER.py").read())

elif robot_category() == "6":
    exec(open("/WEATHER_STATION.py").read())

elif robot_category() == "7":
    exec(open("/GESTURE_ROBOT.py").read())

elif robot_category() == "8":
    exec(open("/LIGHT_AVOIDER.py").read())

elif robot_category() == "9":
    exec(open("/OBJECT_COUNTER.py").read())
    
elif robot_category() == "10":
    exec(open("/Codex_Code.py").read())
