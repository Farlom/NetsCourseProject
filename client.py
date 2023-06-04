import socket
import settings


class Client:
    server_ip = None

    def send_packet(self, message, port=settings.SERVER_PORT):
        destination_address = (self.server_ip, port)
        sending_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sending_socket.sendto(message.encode(), destination_address)
        sending_socket.close()

    def connect_to_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', settings.PORT))
        data = 0
        while data == 0:
            m = sock.recvfrom(14)
            data = m[0].decode()
        self.server_ip = data
        sock.close()


    def handshake_with_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destination_address = (self.server_ip, settings.SERVER_PORT)
        sock.sendto(f'Hello, I`m using port {settings.SERVER_PORT}. Client'.encode(), destination_address)
        sock.close()

    def connection_ack(self) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', settings.CLIENT_PORT))
        data = 0
        while data == 0:
            m, addr = sock.recvfrom(35)
            data = m.decode()
        if addr[0] == self.server_ip:
            sock.close()
            return True

    def recieve_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', settings.CLIENT_PORT))

        data = 0
        while data == 0:
            m = sock.recvfrom(7)
            data = m[0].decode()
        sock.close()
        return data


