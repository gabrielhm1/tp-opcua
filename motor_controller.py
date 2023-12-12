import threading
import time
import utils.opc_functions as opc_functions
import utils.control as control
from opcua import Server, ua, Node

Ra = 0.02
La = 0.01
Ia = 10
Km = 0.5
tl = 0
Jm = 300
B  = 0.5
Kb = 0.98
Dt = 0.35

def simulate_motor_equation(motor_info):
    speed = motor_info["speed"]
    torque = motor_info["torque"]
    if motor_info["status"] == "off":
        motor_info["voltage"] = 0
        speed = speed - 0.01 if speed > 1 else 0
        torque = torque - 0.01 if torque > 1 else 0
    
    
    torque = (Dt*Km*motor_info["voltage"]-Km*Kb*speed*Dt-torque*Ra*Dt+torque*La)/La
    speed = (Jm*speed+Dt*torque-tl*Dt-speed*B*Dt)/Jm if speed >= 0 else 0
    
    motor_info["torque"] = torque if torque > 0 else 0

    motor_info["speed"] = speed if speed  <= 178 else 178
        

# Função para a thread motor
def motor_thread(index,motor_info):
    # Defina os parâmetros do motor

    while True:
        # Simula a equação dinâmica do motor
        simulate_motor_equation(motor_info)
        # print(f"Motor {index}: {motor_info}")

        # Aguarda o próximo período de simulação (mínimo de 100ms)
        time.sleep(0.1)

# Função para a thread de controle
def control_thread(motors):
    while True:
        time.sleep(0.2)
        current_motor_status = {}

        for i in range(1,12):
            current_motor_status[f"motor{i}"] = {"operation": opc_functions.get_var(i,"operation"), "speed": opc_functions.get_var(i,"speed"), "status":opc_functions.get_var(i,"status"),"voltage":opc_functions.get_var(i,"voltage"),"torque":opc_functions.get_var(i,"torque")}
        motors_in_sequency = control.check_sequency(current_motor_status)
        
        # Verifica se há motores em sequência e liga os motores
        if not motors_in_sequency:
            for motor in motors:
                motors[motor]["voltage"] = current_motor_status[motor]["voltage"]
                motors[motor]["operation"] = current_motor_status[motor]["operation"]
                if motors[motor]["operation"] == "start":
                    motors[motor]["status"] = "on"
                else:
                    motors[motor]["status"] = "off"
                    motors[motor]["voltage"] = 0
            
        for motor in motors:
            index = int(motor.split("motor")[1])
            opc_functions.set_var(index,"status",motors[motor]["status"])
            opc_functions.set_var(index,"speed",motors[motor]["speed"])
            opc_functions.set_var(index,"torque",motors[motor]["torque"])
    


# def test_motor(motors):
#     motors["motor1"]["operation"] = "start"
#     motors["motor1"]["voltage"] = 127
#     motors["motor3"]["operation"] = "start"
#     motors["motor3"]["voltage"] = 127
#     motors["motor5"]["operation"] = "start"
#     motors["motor5"]["voltage"] = 127
#     motors["motor7"]["operation"] = "start"
#     motors["motor7"]["voltage"] = 127


if __name__ == "__main__":
    # Inicia as threads
    motors = {f"motor{i}": {"operation": "stop", "speed": 0, "status":"off","voltage":0,"torque":0} for i in range(1, 12)}
    for motor in motors:
            index = int(motor.split("motor")[1])
            opc_functions.set_var(index,"status",motors[motor]["status"])
            opc_functions.set_var(index,"speed",motors[motor]["speed"])
            opc_functions.set_var(index,"torque",motors[motor]["torque"])
            opc_functions.set_var(index,"voltage",motors[motor]["voltage"])
            opc_functions.set_var(index,"operation",motors[motor]["operation"])
    
    
    motor_threads = [threading.Thread(target=motor_thread, args=(i,motors[f"motor{i}"])) for i in range(1, 12)]
    control_thread = threading.Thread(target=control_thread, args=(motors,))

    for thread in motor_threads:
        thread.start()
    control_thread.start()
    # Aguarda todas as threads terminarem
    for thread in motor_threads:
        thread.join()
    control_thread.join()