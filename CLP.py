import threading
from opcua import Client
import socket
from utils import clp_server
import json
import os

options = {"1": "start", "2": "stop", "3": "stop_all", "4": "motor_info"}

def opc_client():
    client = Client("opc.tcp://SOVBRC02ZX4MYMD6N-2.local:53530/OPCUA/SimulationServer")
    client.connect()

    client.disconnect()


def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("clp", int(os.getenv("TCP_PORT"))))
    server.listen(1)
    is_connection_open = False
    while True:
        if not is_connection_open:
            client_socket, addr = server.accept()
            is_connection_open = True
        try:
            print("Esperando dados do cliente")
            data = client_socket.recv(1024)
            data_decoded = data.decode().replace("'", '"')
            print(data_decoded)

            data_decoded = json.loads(data_decoded)
            print(type(data_decoded))
            response = {}
            if data_decoded["option"] == "1":
                print("Start Option Selected")
                response = clp_server.start_motor(data_decoded["payload"])
                print(response)
            elif data_decoded["option"] == "2":
                print("Stop Option Selected")
                response = clp_server.stop_motor(data_decoded["payload"])
            elif data_decoded["option"] == "3":
                print("Stop All Option Selected")
                response = clp_server.stop_all_motors()
            elif data_decoded["option"] == "4":
                print("Motor Info Option Selected")
                response = clp_server.get_motor_info(data_decoded["payload"])
            elif data_decoded["option"] == "5":
                print("Exit Option Selected")
                client_socket.close()
                client_socket.send("{status: 'success', message: 'Connection closed'}".encode())
                
                is_connection_open = False
                break
            client_socket.send(str(response).encode())
        except:
            client_socket.close()
            server.close()
            clp_server.disconnect()
            exit(0)


if __name__ == "__main__":
    tcp_thread = threading.Thread(target=tcp_server)

    tcp_thread.start()

    tcp_thread.join()
