import socket
import json

import os

def write_file(data):
    with open("historiador.txt", "+a") as f:
        f.write("------------------\n")
        f.write(data)


def operator_menu():
    user_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = ((os.getenv("HOST"), int(os.getenv("TCP_PORT"))))

    data_to_send = {}
    run = True
    user_client.connect(server_addr)
    while run:
        data_to_send = {}
        print("\n1 - Ligar Motor")
        print("2 - Desligar Motor")
        print("3 - Parar Todos os Motores")
        print("4 - Obter Informações de um Motor")
        print("5 - Sair ")
        option = input("Selecione uma opcao: ")
        if option == "1":
            motor_id = input("Selecione um motor para iniciar (1-11): ")
            voltage = input("Informe a tensão de armadura (0-127): ")
            payload = {"motor_id": motor_id, "voltage": voltage}

        elif option == "2":
            motor_id = input("Selecione um motor desligar (1-11): ")
            payload = {"motor_id": motor_id}
        elif option == "3":
            payload = "Stop All"
        elif option == "4":
            motor_id = input("Selecione um motor para obter informação (1-11): ")
            payload = {"motor_id": motor_id}
        elif option == "5":
            payload = "Exit"
            run = False
        else:
            print("Invalid option")
            break

        data_to_send = {"option": option, "payload": payload}
        data_to_send = str(data_to_send).encode()
        user_client.send(data_to_send)

        response = user_client.recv(1024)
        response_decoded = json.loads(response.decode().replace("'", '"'))

        if response_decoded["status"] == "success" and option == "4":
            data_to_write = f"Opção selecionada: {option}\nInformações do motor {payload['motor_id']}:\n Operação: {response_decoded['message']['operation']}\n Velocidade: {response_decoded['message']['speed']}\n Status: {response_decoded['message']['status']}\n Tensão: {response_decoded['message']['voltage']}\n Torque: {response_decoded['message']['torque']}\n"
            print(f"\n{data_to_write}")
        elif response_decoded["status"] == "success":
            print(f"\nOperação realizada com successo. {response_decoded['message']}")
            data_to_write = f"Opção selecionada: {option}\nPayload Enviado:{payload}\nStatus: {response_decoded['status']}\nMensagem: {response_decoded['message']}\n"
        elif response_decoded["status"] == "error":
            print(f"\nErro ao realizar operação. {response_decoded['message']}\n")
            data_to_write = f"Opção selecionada: {option}\nPayload Enviado:{payload}\nStatus: {response_decoded['status']}\nMensagem: {response_decoded['message']}\n"

        write_file(data_to_write)

    user_client.close()


if __name__ == "__main__":
    operator_menu()
