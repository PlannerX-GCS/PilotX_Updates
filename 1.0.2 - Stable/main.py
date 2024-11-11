from ROBOT_CONFIGURATIONS import robot_category

if robot_category() == "0":
    exec(open("/LINE_FOLLOWER.py").read())
    
elif robot_category() == "1":
    exec(open("/OBSTACLE_AVOIDER.py").read())
    
elif robot_category() == "2":
    exec(open("/SELF_BALANCING_ROBOT.py").read())
    
elif robot_category() == "5":
    exec(open("/Codex_Code.py").read())