from tkinter import *
from server import *
import time
from threading import Thread
from tkinter.ttk import Combobox

def handshake(sock, window):
    sock.send_broadcast()
    window.after(5000, sock.send_broadcast())

def create_game():
    welcome_window.destroy()
    lobby = Tk()
    lobby.title('Ожидание игроков...')
    lobby.geometry('800x600')

    now = time.time()

    server = Server()
    handshake(server, lobby)
    # new_thread = Thread(target=server.send_broadcast())
    # while 1 != 2:
    #     ...
    #     # server.send_broadcast()
    #     # time.sleep(5)

welcome_window = Tk()
welcome_window.title("ATARI PING PONG")
welcome_window.geometry('800x600')
welcome_window.grid()
connect_button = Button(welcome_window, text="Создать игру", command=create_game)
connect_button.grid(column=5, row=0)
create_button = Button(welcome_window, text="Присоединится к игре")
create_button.grid(column=5, row=1)
# combo = Combobox(window)
# combo['values'] = (1, 2, 3, 4, 5, "Текст")
# combo.current(1)  # установите вариант по умолчанию
# combo.grid(column=0, row=0)
welcome_window.mainloop()
