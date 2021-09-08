"""Unit-тесты сервера"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.vars import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import response


class TestServer(unittest.TestCase):
    """
    В сервере только 1 функция для тестирования
    """
    def setUp(self) -> None:
        self.err_dict = {
            RESPONSE: 400,
            ERROR: 'Bad request'
        }
        self.ok_dict = {RESPONSE: 200}

    def test_no_action(self):
        """Ошибка если нет действия"""
        self.assertEqual(response(
            {TIME: '123456.654321', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        """Ошибка если неизвестное действие"""
        self.assertEqual(response(
            {ACTION: 'Wrong', TIME: '123456.654321', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.assertEqual(response(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_time(self):
        """Ошибка, если штамп времени не корректен"""
        self.assertEqual(response(
            {ACTION: PRESENCE, TIME: '-123456.654321', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(response(
            {ACTION: PRESENCE, TIME: '123456.654321'}), self.err_dict)

    def test_unknown_user(self):
        """Ошибка - не Guest"""
        self.assertEqual(response(
            {ACTION: PRESENCE, TIME: 123456.654321, USER: {ACCOUNT_NAME: 'Guest1'}}), self.err_dict)

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(response(
            {ACTION: PRESENCE, TIME: 123456.654321, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
