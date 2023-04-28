import socket
import settings


class Server:
    ip = settings.IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_broadcast(self):
        destination_address = ('<broadcast>', settings.PORT)
        Server.server_socket.sendto(settings.IP.encode(), destination_address)

    def send_packet(self, message):
        destination_address = ('<broadcast>', settings.PORT)
        Server.server_socket.sendto(message.encode(), destination_address)


