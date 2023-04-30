import socket
import settings


class Server:
    ip = settings.IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client_ip = None

    def send_broadcast(self):
        destination_address = ('<broadcast>', settings.PORT)
        Server.server_socket.sendto(settings.IP.encode(), destination_address)

    def send_packet(self, message):
        destination_address = ('<broadcast>', settings.PORT)
        Server.server_socket.sendto(message.encode(), destination_address)

    def get_client_ip(self):
        ...

    def handshake_with_client(self):
        destination_address = ('<broadcast>', settings.CLIENT_PORT)
        self.server_socket.sendto(f'Hello, I`m using port {settings.SERVER_PORT}. Server'.encode(), destination_address)

