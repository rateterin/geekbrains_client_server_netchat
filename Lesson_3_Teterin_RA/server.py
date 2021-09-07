import socket
import json
from sys import argv
from time import time as timestamp
from common.vars import MAX_USERS,  authorised_users
from common.funcs import get_message, send_message


def __get_arg(arg):
    if arg in argv:
        i = argv.index(arg) + 1
        if len(argv) > i:
            return argv[i]
    return None


def get_address():
    a = __get_arg('-a')
    if a:
        return a
    return ''


def get_port():
    p = __get_arg('-p')
    if p:
        if p.isdecimal():
            return int(p)
    return 7777


def response(arg):
    if 'action' in arg and arg['action'] == 'presence' and 'user' in arg and 'account_name' in arg['user'] and \
            arg['user']['account_name'] in authorised_users:
        resp = {'response': 200, 'time': timestamp()}
        print()
        print('Send response to client:')
        print(resp)
        return resp
    return {'response': 400, 'error': 'Bad request'}


def error_500():
    return {'response': 500, 'time': timestamp()}


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
            if 'action' in client_msg.keys():
                if client_msg['action'] == 'presence':
                    # что-то делаем с client_msg['user']
                    # если всё ок - отправляем ответ
                    send_message(conn, response(client_msg))
                    # если ошибка
                    # send_message(conn, error_500())


if __name__ == '__main__':
    main()
