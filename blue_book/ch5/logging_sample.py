from logging import (
    getLogger,
    Formatter,
    FileHandler,
    StreamHandler,
    DEBUG,
    ERROR,
)

import requests


logger = getLogger(__name__)

# output format
default_format = '[%(levelname)s] %(asctime)s %(name)s %(filename)s:%(lineno)d %(message)s'
default_formatter = Formatter(default_format)
funcname_formatter = Formatter(default_format + '(%(funcname)s)')

# log handler for console output
log_stream_handler = StreamHandler()
log_stream_handler.setFormatter(default_formatter)
log_stream_handler.setLevel(DEBUG)

# log handler for file output
log_file_handler = FileHandler(filename="crawler.log")
log_file_handler.setFormatter(funcname_formatter)
log_file_handler.setLevel(ERROR)

# set handler and level to logger
logger.setLevel(DEBUG)
logger.addHandler(log_stream_handler)
logger.addHandler(log_file_handler)


def logging_example():
    logger.info('Start crawling') # info level message
    logger.warning('Not crawling because outer site') # warning level message
    logger.error('Not found page') # error level message

    try:
        r = requests.get('ttps://www.youtube.com/watch?v=LWfWY4AEAdo', timeout=1)
    except requests.exceptions.RequestException as e:
        logger.exception('Raise error in requests: %r', e)


if __name__ == "__main__":
    logging_example()