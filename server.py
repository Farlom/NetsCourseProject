import socket
import settings

message = settings.IP
destination_address = ('<broadcast>', settings.PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(message.encode(), destination_address)
# print("Looking for replies; press Ctrl-C to stop.")
#
# while 1:
#     (buf, address) = s.recvfrom(10100)
#     if not len(buf):
#         break
#     print("received from %s: %s" %(address, buf))
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((settings.IP, settings.PORT))
# s.listen(1)
# conn, addr = s.accept()
# while 1:
#     data = conn.recv(1024)
#     if not data:
#         break
#     conn.sendall(data)
# conn.close()