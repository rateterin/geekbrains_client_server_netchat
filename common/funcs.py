import json
from common.vars import BUFFER_SIZE, ENCODING
from log.conf import server_log_config
from log.conf import client_log_config
from log.decorators import log


@log
def get_message(client):
    """
    Утилита приёма и декодирования сообщения
    принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
    :param client:
    :return:
    """

    encoded_response = client.recv(BUFFER_SIZE)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param sock:
    :param message:
    :return:
    """

    if not isinstance(message, dict):
        raise
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)


@log
def validate_host(host, logger):
    octets = host.split('.')
    if all(octet.isdecimal() for octet in octets) and all(0 <= int(octet) <= 255 for octet in octets):
        pass
    else:
        logger.error('Не корректный адрес в параметрах запуска. Завершение.')
        print('Указан не корректный ip-адрес в параметрах запуска')
        print()
        exit(1)


@log
def validate_port(port, logger):
    if 1024 <= port <= 65535:
        pass
    else:
        logger.error('Не корректный порт в параметрах запуска. Завершение.')
        print('В качестве порта следует указать целое число от 1024 до 65535!')
        print()
        exit(1)
