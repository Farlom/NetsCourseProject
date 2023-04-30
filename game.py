from tkinter import *
from server import *
from client import Client
import time
from threading import Thread
import asyncio
from tkinter.ttk import Combobox





def show_lobby():

    # welcome_window.destroy()
    lobby = Tk()

    lobby.title('Ожидание игроков...')
    lobby.geometry('800x600')
    # lobby.mainloop()


def create_game():
    server = Server()
    lobby = Tk()
    welcome_window.destroy()
    lobby.title('Ожидание игроков...')
    lobby.geometry('800x600')

    def send_broadcast():
        server.send_broadcast()
        lobby.after(5000, send_broadcast)

    send_broadcast()


def join():
    client = Client()
    lobby = Tk()
    welcome_window.destroy()
    lobby.title('Подключение...')
    lobby.geometry('800x600')
    client.get_server_ip()
    client.handshake_with_server()
    print(client.get_server_ip())


welcome_window = Tk()
welcome_window.title("ATARI PING PONG")
welcome_window.geometry('800x600')
welcome_window.grid()
connect_button = Button(welcome_window, text="Создать игру", command=create_game)
connect_button.grid(column=5, row=0)
create_button = Button(welcome_window, text="Присоединится к игре", command=join)
create_button.grid(column=5, row=1)
# combo = Combobox(window)
# combo['values'] = (1, 2, 3, 4, 5, "Текст")
# combo.current(1)  # установите вариант по умолчанию
# combo.grid(column=0, row=0)
welcome_window.mainloop()
