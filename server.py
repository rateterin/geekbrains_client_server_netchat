import socket
import logging
import argparse
import select
from sys import argv
from time import time as timestamp
from common.vars import MAX_USERS, authorised_users, users_sockets, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, MESSAGE, ERROR, DEFAULT_ADDRESS, DEFAULT_PORT
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
def process_message(msg, messages, sender):
    if ACTION in msg and msg[ACTION] == PRESENCE and \
            (TIME and USER) in msg and \
            ACCOUNT_NAME in msg[USER]:
        if msg[USER][ACCOUNT_NAME] not in authorised_users:
            # пока просто авторизуем))
            authorised_users.append(msg[USER][ACCOUNT_NAME])
            users_sockets.append(sender)
        send_message(sender, {RESPONSE: 200})
    elif (ACTION and TIME and 'from' and 'to' and 'message') in msg and msg[ACTION] == MESSAGE and \
            (msg['to'] and msg['from']) in authorised_users:
        messages.append((msg['to'], msg['from'], msg['message']))
    elif (ACTION and TIME and ACCOUNT_NAME) in msg and '/?' in ACTION and ACCOUNT_NAME in authorised_users:
        messages.append((msg['to'], msg['from'], msg['message']))
    else:
        send_message(sender, __error_400)
    return


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
    sock.settimeout(0.5)
    sock.listen(MAX_USERS)
    logger.info('Сервер запущен')
    logger.info('Сервер запущен.')
    if host:
        logger.info(f'Сервер принимает подключения на порту {port} адреса {host}')
    else:
        logger.info(f'Сервер принимает подключения на порту {port} всех доступных адресов')
    clients = []
    messages = []
    while True:
        try:
            conn, addr = sock.accept()
        except OSError:
            pass
        else:
            logger.info('Принято соединение от клиента')
            logger.debug(addr)
            clients.append(conn)
        senders = []
        receivers = []
        _err = []
        try:
            if clients:
                senders, receivers, _err = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if senders:
            for sender in senders:
                try:
                    process_message(get_message(sender), messages, sender)
                except:
                    logger.info(f'При приеме сообщения. Потеряна связь с клиентом {sender.getpeername()}')
                    clients.remove(sender)

        if receivers and messages:
            for message in messages:
                if message[2] == '/?':
                    msg = {
                        ACTION: 'response',
                        TIME: timestamp(),
                        'to': message[1],
                        'cmd': '/?',
                        'data': authorised_users[1:]
                    }
                else:
                    msg = {
                        ACTION: 'msg',
                        TIME: timestamp(),
                        'from': message[1],
                        'to': message[0],
                        'message': message[2]
                    }
                for receiver in receivers:
                    if msg['to'] == '#' or msg['to'] == authorised_users[users_sockets.index(receiver)]:
                        try:
                            send_message(receiver, msg)
                        except:
                            logger.info(f'При отправке сообщения. Потеряна связь с клиентом {receiver.getpeername()}')
                            clients.remove(receiver)
            messages = []


if __name__ == '__main__':
    main()
