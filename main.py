import server
import time
import socket
import keyboard
from client import Client
# import server
if __name__ == '__main__':
    # client = Client()
    # client.handshake_with_server()
    # server = server.Server()
    # server.handshake_with_client()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

    sock.sendto('123'.encode(), ('192.168.171.7', 21313))
    # stop = False
    # while True:
    #     server.send_broadcast()
    #     time.sleep(5)

    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    # sock.sendto("utf-8".encode(), (settings.IP, 21313))
    # while not stop:
    #     if keyboard.is_pressed('down'):
    #         server.send_packet('down')
    #         stop = True
    #
    #     if keyboard.is_pressed('up'):
    #         server.send_packet('up')


