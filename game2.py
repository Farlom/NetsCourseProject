import settings
from server import Server
from client import Client
import time
from threading import Thread
choice = int(input("Клиент = 1, Сервер = 2: "))

if choice == 1:
    client = Client()
    client.connect_to_server()
    print(client.server_ip)

    client.handshake_with_server()


elif choice == 2:
    server = Server()

    def send_broadcast():
        while True:
            server.send_broadcast()
            time.sleep(5)

    def get_client_ip():
        while not server.get_client_ip():
            server.get_client_ip()
        print(server.client_ip)

    thread_broad = Thread(target=send_broadcast)
    # thread_client = Thread(target=get_client_ip)
    thread_broad.start()
    server.get_client_ip()
    # print(server.client_ip)
    # thread_client.start()

