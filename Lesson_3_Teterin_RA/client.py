import socket
import json
from sys import argv
from time import time as timestamp
from common.funcs import get_message, send_message


def show_usage():
    print(f'Usage: {argv[0].split("/").pop()} <addr> [<port>]')
    print(f'Usage: <addr> - ip-address, required')
    print(f'Usage: <port> - number of port, integer from 1024 to 65535, optional')


def get_address():
    if len(argv) > 1:
        return argv[1]
    show_usage()
    exit()


def get_port():
    if len(argv) > 2:
        if argv[2].isdecimal():
            return int(argv[2])
    return 7777


HOST = get_address()
PORT = get_port()


def presence_message(account_name: str = 'Guest'):
    if not account_name:
        return False
    msg = {'action': 'presence', 'time': timestamp(), 'user': {'account_name': account_name}}
    return msg


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError as e:
        print(str(e))
        exit(e.errno)
    send_message(sock, presence_message())
    try:
        response = get_message(sock)
    except (ValueError, json.JSONDecodeError):
        print('При декодировании сообщения от сервера возникли проблемы')
    else:
        print(response)


if __name__ == '__main__':
    main()
