import socket
import settings

message = settings.IP
destination_address = ('<broadcast>', settings.PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.sendto(message.encode(), destination_address)
