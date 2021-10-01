import socket
import logging
import argparse
import threading
import time
from sys import argv
from time import time as timestamp
from common.vars import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_ADDRESS, DEFAULT_PORT
from common.funcs import get_message, send_message, validate_host, validate_port
from log.conf import client_log_config
from log.decorators import log


logger = logging.getLogger('client.py')
__exit = False


@log
def presence_message(account_name: str = 'Guest'):
    msg = {ACTION: PRESENCE, TIME: timestamp(), USER: {ACCOUNT_NAME: account_name}}
    return msg


@log
def parse_message(response):
    if RESPONSE in response:
        print(response)
        if response[RESPONSE] == 200:
            return '200: OK'
        return f'400: {response[ERROR]}'
    elif (ACTION and TIME and 'to' and 'from' and 'message') in response and response[ACTION] == 'msg':
        return response['message']
    elif (ACTION and TIME and 'to' and 'cmd' and 'data') in response and \
            response[ACTION] == 'response' and response['cmd'] == '/?':
        return f'Сейчас в чате: {str(", ".join([el for el in sorted(response["data"])]))}'
    else:
        raise ValueError


@log
def encode_message(message, account_name='Guest'):
    if ':' in message:
        to = message.split(':', 1)[0]
        msg = message.split(':', 1)[1]
    else:
        to = '#'
        msg = message
    _enc_msg = {
        ACTION: 'msg',
        TIME: timestamp(),
        'to': to,
        'from': account_name,
        'message': msg
    }
    return _enc_msg


@log
def encode_cmd(cmd, account_name='Guest'):
    if cmd in ('/?',):
        _enc_cmd = {
            ACTION: 'cmd',
            TIME: timestamp(),
            ACCOUNT_NAME: account_name
        }


def th_listen(sock, nick):
    while not __exit:
        msg = get_message(sock)
        try:
            msg_text = parse_message(msg)
        except:
            logger.critical('Ошибка при приеме сообщения от сервера. Завершение.')
        else:
            if 'from' in msg:
                print(f'{msg["from"]}: {msg_text}')
            else:
                print(msg_text)


def th_ui(sock, nick):
    while True:
        # Когда это разрастется - нужно будет запихнуть это в команду /help
        print(f'Привет, {nick}!')
        print('Введите сообщение для отправки всем.')
        print('Введите Имя, двоеточие и сообщение для отправки личного сообщения.')
        print('Узнать кто сейчас в чате - /?')
        print('Для выхода - просто нажмите "Enter".')
        message = input()
        if message:
            try:
                enc_message = encode_message(message, account_name=nick)
            except:
                logger.critical('Ошибка при кодировании сообщения. Завершение.')
                __exit = True
                break
            else:
                logger.info('Сообщение успешно закодировано.')
            try:
                send_message(sock, enc_message)
            except:
                logger.critical('Ошибка отправки сообщения на сервер. Завершение.')
                __exit = True
                break
        else:
            logger.info('Завершение по команде пользователя')
            __exit = True
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(argv[1:])

    host = namespace.addr
    port = namespace.port
    name = namespace.name

    validate_host(host, logger)

    validate_port(port, logger)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except ConnectionRefusedError as e:
        logger.critical('Не удалось подключиться к серверу! Завершение.')
        logger.debug(f'name={name} host={host} port={port}')
        exit(e.errno)
    else:
        logger.info('Успешное подключение к серверному сокету.')
    try:
        send_message(sock, presence_message(name))
    except:
        logger.critical('Ошибка при отправке presence-сообщения на сервер. Завершение.')
        exit(1)
    else:
        logger.info('На сервер успешно отправлено presence-сообщение.')
    try:
        enc_presence_response = get_message(sock)
    except:
        logger.critical('Ошибка приема presence-ответа. Завершение.')
        exit(1)
    else:
        logger.info('Успешно принят presence-ответ от сервера. Декодирую...')
    try:
        parse_message(enc_presence_response)
    except ValueError:
        logger.error('При декодировании сообщения от сервера возникли проблемы. Завершение.')
        exit(1)
    else:
        logger.info('Успешно декодировано сообщение от сервера.')

    receiver_thread = threading.Thread(target=th_listen, name='client_receiver_thread', args=(sock, name), daemon=True)
    receiver_thread.daemon = True
    receiver_thread.start()
    logger.info('Запущен процесс, принимающий сообщения.')

    ui_thread = threading.Thread(target=th_ui, name='client_ui_thread', args=(sock, name), daemon=True)
    ui_thread.daemon = True
    ui_thread.start()
    logger.info('Запущен процесс взаимодействия с пользователем/отправки сообщения.')

    while True:
        time.sleep(1)
        if receiver_thread.is_alive() and ui_thread.is_alive():
            continue
        break


if __name__ == '__main__':
    main()
