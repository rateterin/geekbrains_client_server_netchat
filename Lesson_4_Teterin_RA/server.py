import socket
import json
from sys import argv
from time import time as timestamp
from common.vars import MAX_USERS,  authorised_users, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.funcs import get_message, send_message


def __get_arg(arg):
    if arg in argv:
        i = argv.index(arg) + 1
        if len(argv) > i:
            return argv[i]
        else:
            print('Ошибка при обработке параметров строки запуска')
            print()
            show_usage()
            exit(1)
    return None


def __error_400():
    return {RESPONSE: 400, ERROR: 'Bad request'}


def __error_500():
    return {RESPONSE: 500, TIME: timestamp()}


def show_usage():
    print(f'Usage: {argv[0].split("/").pop()} [-a <addr>] [-p <port>]')
    print(f'Usage: <addr> - ip-address, optional, default all available ip\'s')
    print(f'Usage: <port> - number of port, integer from 1024 to 65535, optional, default 7777')


def get_address():
    a = __get_arg('-a')
    if a:
        return a
    return '127.0.0.1'


def get_port():
    p = __get_arg('-p')
    if p:
        if p.isdecimal() and 1024 <= int(p) <= 65535:
            return int(p)
        else:
            print('В качестве порта следует указать целое число от 1024 до 65535!')
            print()
            show_usage()
            exit(1)
    return 7777


def response(arg):
    if ACTION in arg and arg[ACTION] == PRESENCE and \
            TIME in arg and \
            USER in arg and \
            ACCOUNT_NAME in arg[USER] and arg[USER][ACCOUNT_NAME] in authorised_users:
        try:
            test_time = float(arg[TIME])
        except ValueError:
            return __error_400()
        else:
            if test_time < 0:
                return __error_400()
            resp = {RESPONSE: 200}
            print()
            print('Send response to client:')
            print(resp)
            return resp
    return __error_400()


def main():
    host = get_address()
    port = get_port()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(MAX_USERS)
    while True:
        conn, addr = sock.accept()
        try:
            client_msg = get_message(conn)
        except (ValueError, json.JSONDecodeError):
            print('Принятое от клиента сообщение не корректно.')
        else:
            print()
            print('Received message from client:')
            print(client_msg)
            if ACTION in client_msg.keys():
                if client_msg[ACTION] == PRESENCE:
                    # что-то делаем с client_msg['user']
                    # если всё ок - отправляем ответ
                    send_message(conn, response(client_msg))
                    # если ошибка
                    # send_message(conn, __error_500())


if __name__ == '__main__':
    main()
