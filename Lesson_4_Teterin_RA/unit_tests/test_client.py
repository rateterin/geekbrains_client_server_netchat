"""Unit-тесты клиента"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.vars import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import presence_message, parse_response


class TestClass(unittest.TestCase):
    """
    Класс с тестами
    """

    def test_empty_presence(self):
        """Тест функции формирования сообщения-присутствия без параметров"""
        test = presence_message()
        test[TIME] = 123456.654321
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 123456.654321, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_def_presence(self):
        """Тест функции формирования сообщения-присутствия с непустым параметром account_name"""
        test = presence_message('User1')
        test[TIME] = 123456.654321
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 123456.654321, USER: {ACCOUNT_NAME: 'User1'}})

    def test_200_parse(self):
        """Тест корректного разбора ответа 200"""
        self.assertEqual(parse_response({RESPONSE: 200}), '200: OK')

    def test_400_parse(self):
        """Тест корректного разбора 400"""
        self.assertEqual(parse_response({RESPONSE: 400, ERROR: 'Bad Request'}), '400: Bad Request')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, parse_response, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
