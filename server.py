import socket
import json
import logging
import argparse
from sys import argv
from time import time as timestamp
from common.vars import MAX_USERS, authorised_users, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, \
    DEFAULT_ADDRESS, DEFAULT_PORT
from common.funcs import get_message, send_message, validate_host, validate_port
from log.conf import server_log_config
from log.decorators import log


logger = logging.getLogger('server.py')


@log
def __error_400():
    return {RESPONSE: 400, ERROR: 'Bad request'}


@log
def __error_500():
    return {RESPONSE: 500, TIME: timestamp()}


@log
def response(arg):
    if ACTION in arg and arg[ACTION] == PRESENCE and \
            TIME in arg and \
            USER in arg and \
            ACCOUNT_NAME in arg[USER] and arg[USER][ACCOUNT_NAME] in authorised_users:
        try:
            test_time = float(arg[TIME])
        except ValueError:
            logger.warning('Время в запросе не корректно')
            return __error_400()
        else:
            if test_time < 0:
                logger.warning('Время в запросе не корректно')
                return __error_400()
            resp = {RESPONSE: 200}
            logger.info('Сообщение от клиента успешно декодировано. Возвращаем клиенту 200')
            print()
            print('Send response to client:')
            print(resp)
            return resp
    logger.warning('Запрос от клиента не корректен. Возвращаем клиенту 400')
    logger.debug(arg)
    return __error_400()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default='', nargs='?')
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    namespace = parser.parse_args(argv[1:])

    host = namespace.a
    port = namespace.p

    if host:
        validate_host(host, logger)
    validate_port(port, logger)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(MAX_USERS)
    logger.info('Сервер запущен')
    logger.info('Сервер запущен.')
    if host:
        logger.info(f'Сервер принимает подключения на порту {port} адреса {host}')
    else:
        logger.info(f'Сервер принимает подключения на порту {port} всех доступных адресов')
    while True:
        conn, addr = sock.accept()
        logger.info('Принято соединение от клиента')
        logger.debug(addr)
        try:
            client_msg = get_message(conn)
        except (ValueError, json.JSONDecodeError):
            logger.warning('Во время приема сообщения от клиента возникла ошибка.')
            logger.debug(f'Клиент {addr}')
        else:
            logger.info('Принято сообщение от клиента.')
            print()
            print('Received message from client:')
            print(client_msg)
            if ACTION in client_msg.keys():
                if client_msg[ACTION] == PRESENCE:
                    # что-то делаем с client_msg['user']
                    # если всё ок - отправляем ответ
                    response_to_client = response(client_msg)
                    send_message(conn, response_to_client)
                    # если ошибка
                    # send_message(conn, __error_500())


if __name__ == '__main__':
    main()
