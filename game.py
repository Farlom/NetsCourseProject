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

    def __init__(self, choice):
        if choice == 1:
            self.is_server = True
            self.server = Server()
            self.connection = False

            def send_broadcast():

                while self.server.client_ip is None:
                    self.server.send_broadcast()
                    time.sleep(5)
                self.connection = True
                print('Подключение установлено')

            def get_client_ip():
                self.server.get_client_ip()
                print(self.server.client_ip)

            thread_broad = Thread(target=send_broadcast)
            thread_client = Thread(target=get_client_ip)
            thread_broad.start()
            thread_client.start()

            while True:
                if thread_broad.is_alive():
                    time.sleep(1)
                else:
                    break

            self.server.handshake_with_client()
        elif choice == 2:
            self.is_server = False
            self.client = Client()
            self.client.connect_to_server()
            print(self.client.server_ip)

            self.client.handshake_with_server()

            print(self.client.connection_ack())

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
        self.server.send_packet(f'{self.ball.x:02d}{self.ball.y:02d}{self.player.y:02d}')  # __ ballX __ ballY __ playerY

    def update_ball(self):
        ...

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
