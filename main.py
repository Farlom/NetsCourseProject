from game import Pong

if __name__ == '__main__':
    choice = int(input('Создать игру: 1, присоединится к игре: 2. Ввод: '))
    game = Pong(choice)
    game.start()
