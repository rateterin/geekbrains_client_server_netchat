"""Unit-тесты общих функций"""

import sys
import os
import unittest
import json
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.vars import ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.funcs import get_message, send_message


class TestSocket:
    """
    Тестовый класс для тестирования отправки и получения,
    при создании требует словарь, который будет прогонятся
    через тестовую функцию
    """
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        """
        Тестовая функция отправки, корретно  кодирует сообщение,
        так-же сохраняет что должно было отправлено в сокет.
        message_to_send - то, что отправляем в сокет
        :param message_to_send:
        :return:
        """
        json_test_message = json.dumps(self.test_dict)
        # кодирует сообщение
        self.encoded_message = json_test_message.encode(ENCODING)
        # сохраняем что должно было отправлено в сокет
        self.received_message = message_to_send

    def recv(self, max_len):
        """
        Получаем данные из сокета
        :param max_len:
        :return:
        """
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class Tests(unittest.TestCase):
    """
    Тестовый класс, собственно выполняющий тестирование.
    """
    def setUp(self) -> None:
        self.test_dict_send = {
            ACTION: PRESENCE,
            TIME: 123456.654321,
            USER: {
                ACCOUNT_NAME: 'test_account_name'
            }
        }
        self.test_dict_recv_ok = {RESPONSE: 200}
        self.test_dict_recv_err = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }
        # экземпляр тестового словаря, хранит собственно тестовый словарь
        self.test_socket = TestSocket(self.test_dict_send)
        # для теста функции приема сообщения
        self.test_sock_ok = TestSocket(self.test_dict_recv_ok)
        self.test_sock_err = TestSocket(self.test_dict_recv_err)

    def test_send_message(self):
        """
        Тестируем корректность работы фукции отправки,
        создадим тестовый сокет и проверим корректность отправки словаря
        :return:
        """
        # вызов тестируемой функции, результаты будут сохранены в тестовом сокете
        send_message(self.test_socket, self.test_dict_send)
        # проверка корректности кодирования словаря.
        # сравниваем результат тестового кодирования и результат кодирования от тестируемой функции
        self.assertEqual(self.test_socket.encoded_message, self.test_socket.received_message)
        # дополнительно, проверим генерацию исключения, при не словаре на входе.
        with self.assertRaises(Exception):
            send_message(self.test_socket, 'not_dict')

    def test_get_message(self):
        """
        Тест функции приёма сообщения
        :return:
        """
        # тест корректной расшифровки корректного словаря
        self.assertEqual(get_message(self.test_sock_ok), self.test_dict_recv_ok)
        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(get_message(self.test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
