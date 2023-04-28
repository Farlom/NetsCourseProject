import socket
import settings

class Client:
    pass


# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind(('', settings.PORT))
# data = 0
# while data == 0:
#     m=s.recvfrom(4096)
#     data = m[0].decode()
#     # print('len(m)='+str(len(m)))
#     # print('len(m[0])='+str(len(m[0])))
#     # print(m[0])
#     #
#     # print('len(m[1])='+str(len(m[1])))
#     # print(m[1])
#
# print(data)
# s.sendto('Hello'.encode(), (data, 21313))

raw_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# raw_sock.connect(('192.168.171.11', settings.PORT))
raw_sock.sendto('Hello'.encode(), ('192.168.171.11', 21312))
raw_sock.close()
print(123)