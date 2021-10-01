import subprocess
import time
from sys import platform
from tkinter import Entry, Button, Tk, Label, messagebox, StringVar

from common.vars import DEFAULT_ADDRESS, DEFAULT_PORT


# Для Linux! Укажите строку запуска команды в терминале, установленном у вас.
LAUNCH_IN_TERMINAL = 'xfce4-terminal --command='


class Launcher:

    def __init__(self, master):
        self.master = master
        master.title('Launcher')
        master.geometry('400x200+700+300')

        self.host = StringVar()
        self.port = StringVar()
        self.clients = StringVar()

        self.host_label = Label(master, text='host:')
        self.port_label = Label(master, text='port:')
        self.clients_label = Label(master, text='clients:')

        self.host_label.grid(row=0, column=0, sticky="w")
        self.port_label.grid(row=1, column=0, sticky="w")
        self.clients_label.grid(row=2, column=0, sticky="w")

        self.host_entry = Entry(textvariable=self.host)
        self.port_entry = Entry(textvariable=self.port)
        self.clients_entry = Entry(textvariable=self.clients)

        self.host_entry.insert(0, DEFAULT_ADDRESS)
        self.port_entry.insert(0, DEFAULT_PORT)
        self.clients_entry.insert(0, 3)

        self.host_entry.grid(row=0, column=1, padx=5, pady=5)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)
        self.clients_entry.grid(row=2, column=1, padx=5, pady=5)

        self.start_button = Button(text="Запуск", command=lambda: self.start())
        self.stop_button = Button(text="Закрыть все окна", command=lambda: self.stop())

        self.start_button.grid(row=3, column=1, padx=5, pady=5, sticky="e")
        self.stop_button.grid(row=3, column=2, padx=5, pady=5, sticky="e")

        self.processes = []

    def _start_process(self, cmd_line):
        if platform == 'win32':
            self.processes.append(subprocess.Popen(cmd_line, creationflags=subprocess.CREATE_NEW_CONSOLE))
        elif platform in ('linux', 'linux2'):
            self.processes.append(subprocess.Popen(f'{LAUNCH_IN_TERMINAL}"{cmd_line}"', shell=True))
        return

    def start(self):
        self.processes.append(
            self._start_process(f'python server.py -p {self.port.get()} -a {self.host.get()}'))
        time.sleep(0.5)

        for i in range(int(self.clients.get())):
            self.processes.append(
                self._start_process(f'python client.py {self.host.get()} {self.port.get()} -n test{i + 1}'))

    def stop(self):
        while self.processes:
            proc_to_kill = self.processes.pop()
            proc_to_kill.kill()


root = Tk()
my_gui = Launcher(root)
root.mainloop()
