import settings
from server import Server
from client import Client
import time
from threading import Thread

import socket

choice = int(input("Клиент = 1, Сервер = 2: "))

if choice == 1:
    client = Client()
    client.connect_to_server()
    print(client.server_ip)

    client.handshake_with_server()


elif choice == 2:
    server = Server()
    connection = False

    def send_broadcast():
        global connection
        while server.client_ip is None:
            server.send_broadcast()
            time.sleep(5)
        connection = True
        print('Подключение установлено')

    def get_client_ip():
        server.get_client_ip()
        print(server.client_ip)

    thread_broad = Thread(target=send_broadcast)
    thread_client = Thread(target=get_client_ip)
    thread_broad.start()
    thread_client.start()

    while True:
        if thread_broad.is_alive():
            time.sleep(1)
        else:
            break

    server.handshake_with_client()


