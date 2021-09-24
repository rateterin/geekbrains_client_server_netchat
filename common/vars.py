import logging


MAX_USERS = 99
BUFFER_SIZE = 1024
ENCODING = 'utf-8'
DEFAULT_ADDRESS = '127.0.0.1'
DEFAULT_PORT = 7777
LOG_LEVEL = logging.DEBUG

# Протокол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
MESSAGE = 'msg'
ACCOUNT_NAME = 'account_name'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'

# Сервер хранит тут имена аккаунтов авторизованных пользователей
authorised_users = ['Guest']
users_sockets = [None]
