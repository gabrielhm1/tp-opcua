from opcua import Client

opc_server_url = "opc.tcp://SOVBRC02ZX4MYMD6N-2.local:53530/OPCUA/SimulationServer"
client = Client(opc_server_url)
client.connect()

def request_var(motor_index,var):
    node = client.get_root_node()
    return node.get_child(["0:Objects", f"3:Motor", f"3:motor{motor_index}",f"3:{var}"])

def set_var(motor_index,var,value):
    values = request_var(motor_index,var)
    values.set_value(value)

def get_var(motor_index,var):
    values = request_var(motor_index,var)
    return values.get_value()

def disconnect():
    client.disconnect()

def get_node_id():
    for i in range(1,12):
        voltage = request_var(i,"voltage").nodeid
        print(f"{{name=\"motor{i}Voltage\", namespace=\"3\", identifier_type=\"i\", identifier=\"{voltage}\", tags=[[\"id\",\"motor{i}\"]}},")
        speed = request_var(i,"speed").nodeid
        print(f"{{name=\"motor{i}Speed\", namespace=\"3\", identifier_type=\"i\", identifier=\"{speed}\", tags=[[\"id\",\"motor{i}\"]}},")
        torque = request_var(i,"torque").nodeid
        print(f"{{name=\"motor{i}Torque\", namespace=\"3\", identifier_type=\"i\", identifier=\"{torque}\", tags=[[\"id\",\"motor{i}\"]}},")
        operation = request_var(i,"operation").nodeid
        print(f"{{name=\"motor{i}Operation\", namespace=\"3\", identifier_type=\"i\", identifier=\"{operation}\", tags=[[\"id\",\"motor{i}\"]}},")
        status = request_var(i,"status").nodeid
        print(f"{{name=\"motor{i}Status\", namespace=\"3\", identifier_type=\"i\", identifier=\"{status}\", tags=[[\"id\",\"motor{i}\"]}},")

get_node_id()