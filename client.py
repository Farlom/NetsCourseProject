import socket
import settings


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', settings.PORT))

while 1:
    m=s.recvfrom(4096)
    print('len(m)='+str(len(m)))
    print('len(m[0])='+str(len(m[0])))
    print(m[0])

    print('len(m[1])='+str(len(m[1])))
    print(m[1])

