MAX_USERS = 99
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

# Протокол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'

# Сервер хранит тут имена аккаунтов авторизованных пользователей
authorised_users = {'Guest'}
