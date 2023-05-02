import socket
import settings


class Server:
    ip = settings.IP
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client_ip = None

    # def __init__(self, sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)):
    #     self.server_socket = sock
    #     self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_broadcast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        destination_address = ('<broadcast>', settings.PORT)
        sock.sendto(settings.IP.encode(), destination_address)

        sock.close()

    def send_packet(self, message, port=settings.CLIENT_PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destination_address = (self.client_ip, port)
        sock.sendto(message.encode(), destination_address)
        sock.close()

    def get_client_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', settings.SERVER_PORT))

        data = 0
        while data == 0:
            m, addr = sock.recvfrom(1024)
            data = addr[0]
        self.client_ip = data

        sock.close()
        # self.socket.bind((self.client_ip, settings.CLIENT_PORT))

    def handshake_with_client(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destination_address = (self.client_ip, settings.CLIENT_PORT)
        sock.sendto(f'Hello, I`m using port {settings.CLIENT_PORT}. Server'.encode(), destination_address)
        sock.close()

    def packet_ack(self) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', settings.SERVER_PORT))

        data = 0
        while data == 0:
            m, addr = sock.recvfrom(1024)
        sock.close()
        return True

    def deserialize(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', settings.SERVER_PORT))
        data = 0
        while data == 0:
            m = sock.recvfrom(6)
            data = m[0].decode()

        sock.close()
        return int(data[4:6])
