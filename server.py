import socket
import settings


class Server:
    ip = settings.IP
    client_ip = None

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

    def handshake_with_client(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destination_address = (self.client_ip, settings.CLIENT_PORT)
        sock.sendto(f'Hello, I`m using port {settings.CLIENT_PORT}. Server'.encode(), destination_address)
        sock.close()

    def recieve_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', settings.SERVER_PORT))
        data = 0
        while data == 0:
            m = sock.recvfrom(7)
            data = m[0].decode()

        sock.close()
        return data
