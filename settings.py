import socket
from msvcrt import getch
GAME_WIDTH = 40
GAME_HEIGHT = 15
PORT = 21312
SERVER_PORT = 21313
CLIENT_PORT = 21314
IP = socket.gethostbyname(socket.gethostname())

# if getch().decode() == 's':
#     print(123)