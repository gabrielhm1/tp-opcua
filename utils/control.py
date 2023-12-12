def check_sequency(motors):
    sequency =[]
    for k,v in motors.items():
        if v["operation"] == "start":
            sequency.append(int(k.split("motor")[1]))    
    for i in range(len(sequency) - 1):
        if sequency[i] + 1 == sequency[i+1]:
            return True
    
    return False
    