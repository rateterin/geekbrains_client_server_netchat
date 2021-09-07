import socket
import json
from sys import argv
from time import time as timestamp
from common.vars import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.funcs import get_message, send_message


def show_usage():
    print(f'Usage: {argv[0].split("/").pop()} [<addr>] [<port>]')
    print(f'Usage: <addr> - ip-address, optional, default 127.0.0.1')
    print(f'Usage: <port> - number of port, integer from 1024 to 65535, optional, default 7777')


def get_address():
    if len(argv) > 1:
        a = argv[1]
        octets = a.split('.')
        if all(octet.isdecimal() for octet in octets) and all(0 <= int(octet) <= 255 for octet in octets):
            return a
        else:
            print('Указан не корректный ip-адрес в параметрах запуска')
            print()
            show_usage()
            exit(1)
    return '127.0.0.1'


def get_port():
    if len(argv) > 2:
        p = argv[2]
        if p.isdecimal() and 1024 <= int(p) <= 65535:
            return int(p)
        else:
            print('В качестве порта следует указать целое число от 1024 до 65535!')
            print()
            show_usage()
            exit(1)
    return 7777


HOST = get_address()
PORT = get_port()


def presence_message(account_name: str = 'Guest'):
    msg = {ACTION: PRESENCE, TIME: timestamp(), USER: {ACCOUNT_NAME: account_name}}
    return msg


def parse_response(response):
    if RESPONSE in response:
        print(response)
        if response[RESPONSE] == 200:
            return '200: OK'
        return f'400: {response[ERROR]}'
    raise ValueError


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError as e:
        print(str(e))
        exit(e.errno)
    send_message(sock, presence_message())
    try:
        print(parse_response(get_message(sock)))
    except ValueError:
        print('При декодировании сообщения от сервера возникли проблемы')
        exit(1)


if __name__ == '__main__':
    main()
