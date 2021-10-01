import subprocess
import time
from sys import platform

# Для Linux! Укажите строку запуска команды в терминале, установленном у вас.
LAUNCH_IN_TERMINAL = 'xfce4-terminal --command='

PROCESS = []
print(platform)
if platform == 'win32':
    creation_flags = subprocess.CREATE_NEW_CONSOLE
else:
    creation_flags = 0


def start_process(cmd_line):
    if platform == 'win32':
        PROCESS.append(subprocess.Popen(cmd_line, creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif platform in ('linux', 'linux2'):
        PROCESS.append(subprocess.Popen(f'{LAUNCH_IN_TERMINAL}"{cmd_line}"', shell=True))
    return


while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        start_process('python server.py')
        time.sleep(1)
        for i in range(1):
            start_process('python client.py -m send')
        for i in range(2):
            start_process('python client.py -m listen')
    elif ACTION == 'x':
        while PROCESS:
            proc_to_kill = PROCESS.pop()
            proc_to_kill.kill()
