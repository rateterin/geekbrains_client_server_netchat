import sys
import os
import logging
from common.vars import LOG_LEVEL, ENCODING


sys.path.append('../')
CLIENT_FORMATTER = logging.Formatter('%(asctime)-27s %(levelname)-12s %(filename)-25s %(message)s')
log_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_file = os.path.join(log_file, 'logs', 'client.log')
LOG_TO_STDERR = logging.StreamHandler(sys.stderr)
LOG_TO_STDERR.setFormatter(CLIENT_FORMATTER)
LOG_TO_STDERR.setLevel(logging.DEBUG)
LOG_TO_FILE = logging.FileHandler(log_file, encoding=ENCODING)
LOG_TO_FILE.setFormatter(CLIENT_FORMATTER)
log = logging.getLogger('client.py')
log.addHandler(LOG_TO_FILE)
log.setLevel(LOG_LEVEL)


if __name__ == '__main__':
    log.addHandler(LOG_TO_STDERR)
    log.critical('Critical_level_log_message')
    log.error('Error_level_log_message')
    log.warning('Warning_level_log_message')
    log.info('Info_level_log_message')
    log.debug('Debug_level_log_message')
