import os
import logging
import traceback
import inspect
from sys import argv
from .conf import server_log_config
from .conf import client_log_config


logger = logging.getLogger(os.path.basename(argv[0]))


def log(func):
    def wrap(*args, **kwargs):
        log.__doc__ = func.__doc__
        log.__name__ = func.__name__
        logger.debug(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func.__module__}. Вызов из'
                     f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return func(*args, **kwargs)
    return wrap
