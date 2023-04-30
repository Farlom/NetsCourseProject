import pygame
from settings import *
import server
import time
import random

FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создаем игру и окно
pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("ATARI PING PONG")
clock = pygame.time.Clock()

server = server.Server()
# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    server.send_broadcast()
    pygame.time.wait(5000)

    # Рендеринг

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()