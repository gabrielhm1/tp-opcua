from utils import opc_functions

def check_sequency(motors):
    for i in range(len(motors) - 1):
        print(motors[i])
        if motors[i] + 1 == motors[i+1]:
            return True
    return False

def start_motor(payload):
    # print(opc_functions.get_var(payload["motor_id"], "operation"))
    print("Obtendo modo de operação dos motores...")
    motors = [opc_functions.get_var(i, "operation") for i in range(1,12)]
    motors_on = [index+1 for index, value in enumerate(motors) if value == "start"]
    motors_on = list(set(motors_on + [int(payload["motor_id"])]))
    print("Verificando se há motores em sequência...")
    is_motor_in_sequency = check_sequency(motors_on)

    print("Verificando se é possível ligar os motores...")
    if len(motors_on) > 4:
        return {"status": "error", "message": "Não é possível ligar mais que 4 motores"}
    elif is_motor_in_sequency:
        return {"status": "error", "message": "Não é possível ligar motores em sequência"}
    else:
        turn_off_motors = [i for i in range(1, 12) if i not in motors_on]
        
        print("Desligando motores...")
        for motor in turn_off_motors:
            opc_functions.set_var(motor, "operation", "stop")

        print("Ligando Motor selecionado...")
        opc_functions.set_var(int(payload["motor_id"]), "operation", "start")
        opc_functions.set_var(int(payload["motor_id"]), "voltage", int(payload["voltage"]))
        return {"status": "success", "message": "Motor ligado"}

def stop_motor(payload):
    opc_functions.set_var(payload["motor_id"], "operation", "stop")
    opc_functions.set_var(payload["motor_id"], "voltage", 0)
    return {"status": "success", "message": "Motores desligados"}

def stop_all_motors():
    for i in range(1, 11):
        opc_functions.set_var(i, "operation", "stop")
        opc_functions.set_var(i, "voltage", 0)
    return {"status": "success", "message": "Motores desligados"}

def get_motor_info(payload):
    motor_id = payload["motor_id"]
    motor_info = {"operation": opc_functions.get_var(motor_id, "operation"), "speed": opc_functions.get_var(motor_id, "speed"), "status": opc_functions.get_var(motor_id, "status"), "voltage": opc_functions.get_var(motor_id, "voltage"), "torque": opc_functions.get_var(motor_id, "torque")}
    return {"status": "success", "message": motor_info}

def disconnect():
    opc_functions.disconnect()