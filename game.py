import settings
from structure import Struct
import random
import time
import os
import keyboard
from server import Server
from client import Client
from threading import Thread


class Pong:

    field = [' '] * settings.GAME_HEIGHT
    for i in range(settings.GAME_HEIGHT):
        field[i] = [' '] * settings.GAME_WIDTH

    player = Struct(4, int(settings.GAME_HEIGHT / 2))
    opponent = Struct(settings.GAME_WIDTH - 5, int(settings.GAME_HEIGHT / 2))
    ball = Struct(random.randint(10, settings.GAME_WIDTH - 11), int(settings.GAME_HEIGHT / 2), random.randint(1, 4))
    gameover = False

    def __init_conn(self, choice=2):
        if choice == 1:
            self.is_server = True
            self.socket = Server()
            self.connection = False

            def send_broadcast():

                while self.socket.client_ip is None:
                    self.socket.send_broadcast()
                    time.sleep(5)
                self.connection = True
                print('Подключение установлено')

            def get_client_ip():
                self.socket.get_client_ip()
                print(self.socket.client_ip)

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
            self.client_socket = Client()
            self.client_socket.connect_to_server()
            print(self.client_socket.server_ip)
            self.client_socket.handshake_with_server()
            print(self.client_socket.connection_ack())

    def __init__(self, choice):

        self.__init_conn(choice)
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
        for i in range(settings.GAME_HEIGHT):
            for j in range(settings.GAME_WIDTH):
                print(self.field[i][j], end='')
            print()

    def update(self):
        if self.is_server:
            self.logic()
            self.field[self.ball.y][self.ball.x] = ' '

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

            for i in range(settings.GAME_HEIGHT):
                for j in range(settings.GAME_WIDTH):

                    if i == self.player.y and j == self.player.x:
                        self.field[i][j] = '|'
                    if i == self.opponent.y and j == self.opponent.x:
                        self.field[i][j] = '|'

                    if i == self.ball.y and j == self.ball.x:
                        self.field[i][j] = 'o'
            os.system('cls')
            self.show()

            # def send_packet():
            #     self.socket.send_packet(f'{self.ball.x:02d}{self.ball.y:02d}{self.player.y:02d}')
            #
            # def deserialize():
            #     self.socket.deserialize()
            self.socket.send_packet(f'{self.ball.x:02d}{self.ball.y:02d}{self.player.y:02d}')
            # thread_send = Thread(target=send_packet)  # __ ballX __ ballY __ playerY
            # thread_get = Thread(target=deserialize)
            # thread_send.start()
            # thread_get.start()
        else:
            if self.client_socket.deserialize() == (99, 99, 99):
                self.gameover = True
            else:
                self.field[self.ball.y][self.ball.x] = ' '
                self.field[self.opponent.y][self.opponent.x] = ' '
                self.ball.x, self.ball.y, self.opponent.y = self.client_socket.deserialize()
                print(self.ball.x, self.ball.y, self.opponent.y)
                self.field[self.ball.y][self.ball.x] = 'o'
                self.field[self.opponent.y][self.opponent.x] = '|'
                os.system('cls')
                self.show()
                self.client_socket.send_packet(f'9999{self.player.y:02d}')
            # thread_deserialize = Thread(target=deserialize)
            # thread_send = Thread(target=send_packet)
            # thread_deserialize.start()
            # thread_send.start()

            # Thread(target=self.client_socket.send_packet(f'#1#2{self.player.y:02d}')).start()

    def logic(self):
        if self.ball.y == 1 and self.ball.dir == 1:
            self.ball.dir = 4
        elif self.ball.y == 1 and self.ball.dir == 2:
            self.ball.dir = 3
        elif self.ball.y == settings.GAME_HEIGHT-2 and self.ball.dir == 3:
            self.ball.dir = 2
        elif self.ball.y == settings.GAME_HEIGHT-2 and self.ball.dir == 4:
            self.ball.dir = 1

        if self.ball.x == self.player.x+1 and self.player.y + 1 >= self.ball.y > self.player.y - 1:
            if self.ball.dir == 1:
                self.ball.dir = 2
            elif self.ball.dir == 4:
                self.ball.dir = 3

        if self.ball.x == 2 or self.ball.x == settings.GAME_WIDTH - 2:
            self.gameover = True

    def movement(self):
        if keyboard.is_pressed('s'):
            self.field[self.player.y][self.player.x] = ' '
            self.player.y += 1
        elif keyboard.is_pressed('w'):
            self.field[self.player.y][self.player.x] = ' '
            self.player.y -= 1

    def start(self):
        while not self.gameover:
            self.update()
            self.movement()
            time.sleep(0.25)
            # if not self.is_server:
                # print(self.socket.deserialize())
        if self.is_server and self.gameover:
            self.socket.send_packet('999999')
        return 0
