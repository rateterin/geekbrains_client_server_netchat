import socket
import logging
import argparse
from sys import argv
from time import time as timestamp
from common.vars import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_ADDRESS, DEFAULT_PORT
from common.funcs import get_message, send_message, validate_host, validate_port
from log.conf import client_log_config


CLIENT_LOG = logging.getLogger('client_logger')


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
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    namespace = parser.parse_args(argv[1:])

    host = namespace.addr
    port = namespace.port

    validate_host(host, CLIENT_LOG)

    validate_port(port, CLIENT_LOG)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except ConnectionRefusedError as e:
        CLIENT_LOG.critical('Не удалось подключиться к серверу! Завершение.')
        exit(e.errno)
    else:
        CLIENT_LOG.info('Успешное подключение к серверу.')
    msg_to_server = presence_message()
    send_message(sock, msg_to_server)
    CLIENT_LOG.info('На сервер отправлено сообщение-присутствия')
    CLIENT_LOG.debug(msg_to_server)
    try:
        print(parse_response(get_message(sock)))
    except ValueError:
        CLIENT_LOG.error('При декодировании сообщения от сервера возникли проблемы. Завершение.')
        exit(1)
    else:
        CLIENT_LOG.info('Успешно декодировано сообщение от сервера.')


if __name__ == '__main__':
    main()
