import socket
import settings

if __name__ == '__main__':
    choice = input('Enter: ')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((settings.IP, settings.PORT))
    s.listen(1)
    conn, addr = s.accept()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((settings.IP, settings.PORT))
    s.sendall('Hello, world')
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))

    while 1:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
    conn.close()


