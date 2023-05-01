import socket
import settings


class Server:
    ip = settings.IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client_ip = None

    # def __init__(self, sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)):
    #     self.server_socket = sock
    #     self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_broadcast(self):
        destination_address = ('<broadcast>', settings.PORT)
        Server.server_socket.sendto(settings.IP.encode(), destination_address)

    def send_packet(self, message):
        destination_address = ('<broadcast>', settings.PORT)
        Server.server_socket.sendto(message.encode(), destination_address)

    def get_client_ip(self):
        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listening_socket.bind(('', settings.SERVER_PORT))

        data = 0
        while data == 0:
            m, addr = listening_socket.recvfrom(1024)
            data = addr[0]
        self.client_ip = data
        # self.socket.bind((self.client_ip, settings.CLIENT_PORT))

    def connect_to_server(self):
        data = 0
        while data == 0:
            m = self.server_socket.recvfrom(1024)
            data = m[0].decode()
        # self.client_ip = data
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.socket.bind(('', settings.SERVER_PORT))

    def handshake_with_client(self):
        destination_address = (self.client_ip, settings.CLIENT_PORT)
        self.server_socket.sendto(f'Hello, I`m using port {settings.CLIENT_PORT}. Server'.encode(), destination_address)

    def connection_ack(self) -> bool:
        ...
