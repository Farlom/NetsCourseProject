import socket
import settings


class Client:
    # socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = None

    # socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)):
        self.socket = sock
        self.socket.bind(('', settings.PORT))

    def send_packet(self, message, port=settings.SERVER_PORT):
        destination_address = (self.server_ip, port)
        sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sending_socket.sendto(message.encode(), destination_address)

    def connect_to_server(self):
        data = 0
        while data == 0:
            m = self.socket.recvfrom(14)
            data = m[0].decode()
        self.server_ip = data
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', settings.CLIENT_PORT))

    def handshake_with_server(self):
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destination_address = (self.server_ip, settings.SERVER_PORT)
        self.socket.sendto(f'Hello, I`m using port {settings.SERVER_PORT}. Client'.encode(), destination_address)
        # self.socket.sendto('123'.encode(), destination_address)

    def connection_ack(self) -> bool:
        data = 0
        while data == 0:
            m, addr = self.socket.recvfrom(35)
            data = m.decode()
        if addr[0] == self.server_ip:
            # self.socket.bind(('', settings.CLIENT_PORT))
            return True

    def deserialize(self):
        # listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # listening_socket.bind(('', settings.CLIENT_PORT))
        data = 0
        while data == 0:
            m = self.socket.recvfrom(6)
            data = m[0].decode()
        return int(data[0:2]), int(data[2:4]), int(data[4:6])

