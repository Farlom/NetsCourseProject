import settings
from structure import Struct
import random
import time
import os
# import keyboard
from server import Server
from client import Client
import protocol
from threading import Thread
from msvcrt import getch


class Pong:

    field = [' '] * settings.GAME_HEIGHT
    for i in range(settings.GAME_HEIGHT):
        field[i] = [' '] * settings.GAME_WIDTH

    ball = Struct(random.randint(10, settings.GAME_WIDTH - 11), int(settings.GAME_HEIGHT / 2), random.randint(1, 4))
    gameover = False

    def __init_conn(self, choice=2):
        if choice == 1:
            self.is_server = True
            self.socket = Server()
            self.connection = False

            self.player = Struct(4, int(settings.GAME_HEIGHT / 2))
            self.opponent = Struct(settings.GAME_WIDTH - 5, int(settings.GAME_HEIGHT / 2))

            def send_broadcast():

                while self.socket.client_ip is None:
                    self.socket.send_broadcast()
                    time.sleep(5)
                self.connection = True
                print('Подключение установлено')

            def get_client_ip():
                self.socket.get_client_ip()
                print(f'Client IP: {self.socket.client_ip}')

            thread_broad = Thread(target=send_broadcast)
            thread_client = Thread(target=get_client_ip)
            thread_broad.start()
            thread_client.start()

            while True:
                if thread_broad.is_alive():
                    time.sleep(1)
                else:
                    break

            self.socket.handshake_with_client()
        elif choice == 2:
            self.is_server = False

            self.opponent = Struct(4, int(settings.GAME_HEIGHT / 2))
            self.player = Struct(settings.GAME_WIDTH - 5, int(settings.GAME_HEIGHT / 2))

            self.client_socket = Client()
            self.client_socket.connect_to_server()
            print(f'Server IP: {self.client_socket.server_ip}')
            self.client_socket.handshake_with_server()

            if self.client_socket.connection_ack():
                print('Подключение с сервером установлено')

    def __init__(self, choice):

        self.__init_conn(choice)

        if choice == 1:
            ch = input('Тестовый режим (1=True; 2=False): ')
            if ch == '1':
                self.MODE = True
            else:
                self.MODE = False
            print(self.MODE)
        for i in range(settings.GAME_HEIGHT):
            for j in range(settings.GAME_WIDTH):
                if j == 0 or j == settings.GAME_WIDTH - 1:
                    self.field[i][j] = '#'
                if i == 0 or i == settings.GAME_HEIGHT - 1:
                    self.field[i][j] = '#'

                if i == self.player.y and j == self.player.x:
                    self.field[i][j] = '|'
                if i == self.opponent.y and j == self.opponent.x:
                    self.field[i][j] = '|'

                if i == self.ball.y and j == self.ball.x:
                    self.field[i][j] = 'o'

    def show(self):
        os.system('cls')
        for i in range(settings.GAME_HEIGHT):
            for j in range(settings.GAME_WIDTH):
                print(self.field[i][j], end='')
            print()

    def update(self):
        if self.is_server:

            self.__update_ball()

            self.socket.send_packet(protocol.serialize(self.is_server, (self.ball.x, self.ball.y, self.player.y)))

            self.field[self.opponent.y][self.opponent.x] = ' '
            self.opponent.y = protocol.deserialize(self.is_server, self.socket.recieve_packet())

            self.field[self.opponent.y][self.opponent.x] = '|'

            self.show()

        else:
            self.field[self.ball.y][self.ball.x] = ' '
            self.field[self.opponent.y][self.opponent.x] = ' '
            self.ball.x, self.ball.y, self.opponent.y, self.gameover = protocol.deserialize(self.is_server, self.client_socket.recieve_packet())

            if not self.gameover:
                self.field[self.ball.y][self.ball.x] = 'o'
                self.field[self.opponent.y][self.opponent.x] = '|'
                self.show()
                self.client_socket.send_packet(protocol.serialize(self.is_server, (self.player.y, 0)))

    def __update_ball(self):
        self.logic()
        self.field[self.ball.y][self.ball.x] = ' '

        # изменение координат мяча в зависимости от направления
        if self.ball.dir == 1:
            self.ball.x -= 1
            self.ball.y -= 1
        elif self.ball.dir == 2:
            self.ball.x += 1
            self.ball.y -= 1
        elif self.ball.dir == 3:
            self.ball.x += 1
            self.ball.y += 1
        elif self.ball.dir == 4:
            self.ball.x -= 1
            self.ball.y += 1

        self.field[self.ball.y][self.ball.x] = 'o'
        time.sleep(0.25)

    def logic(self):

        # логика коллизий мяча со стенками
        if self.ball.y == 1 and self.ball.dir == 1:
            self.ball.dir = 4
        elif self.ball.y == 1 and self.ball.dir == 2:
            self.ball.dir = 3
        elif self.ball.y == settings.GAME_HEIGHT-2 and self.ball.dir == 3:
            self.ball.dir = 2
        elif self.ball.y == settings.GAME_HEIGHT-2 and self.ball.dir == 4:
            self.ball.dir = 1

        # логика коллизий мяча с игроком
        if self.ball.x == self.player.x+1 and self.player.y + 1 >= self.ball.y > self.player.y - 1:
            if self.ball.dir == 1:
                self.ball.dir = 2
            elif self.ball.dir == 4:
                self.ball.dir = 3

        # логика коллизий мяча с оппонентом
        if self.ball.x == self.opponent.x - 1 and self.opponent.y + 1 >= self.ball.y > self.opponent.y - 1:
            if self.ball.dir == 2:
                self.ball.dir = 1
            elif self.ball.dir == 3:
                self.ball.dir = 4

        # режим игры
        if self.MODE:
            if self.ball.x == 1 and self.ball.dir == 1:
                self.ball.dir = 2
            elif self.ball.x == 1 and self.ball.dir == 4:
                self.ball.dir = 3
            elif self.ball.x == settings.GAME_WIDTH - 2 and self.ball.dir == 2:
                self.ball.dir = 1
            elif self.ball.x == settings.GAME_WIDTH - 2 and self.ball.dir == 3:
                self.ball.dir = 4
        else:
            if self.ball.x == 1 or self.ball.x == settings.GAME_WIDTH - 2:
                self.gameover = True

    def movement(self):
        while True:
            if self.gameover:
                return
            else:
                key = getch().decode()
                if key == 's':
                    if self.player.y < settings.GAME_HEIGHT - 2:
                        self.field[self.player.y][self.player.x] = ' '
                        self.player.y += 1
                        self.field[self.player.y][self.player.x] = '|'
                        self.show()
                if key == 'w':
                    if 1 < self.player.y:
                        self.field[self.player.y][self.player.x] = ' '
                        self.player.y -= 1
                        self.field[self.player.y][self.player.x] = '|'
                        self.show()

    def start(self):
        thread_movement = Thread(target=self.movement)
        thread_movement.start()

        while not self.gameover:
            self.update()
        print('GAMEOVER')
        if self.is_server and self.gameover:
            self.socket.send_packet(protocol.serialize(self.is_server, (random.randint(0, 99),
                                                                        random.randint(0, 99),
                                                                        random.randint(0, 99),
                                                                        1)))
        return 0
