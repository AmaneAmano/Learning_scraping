import os

BASE_DIR = os.path.relpath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'log')

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)


LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': True,
    # setting output format
    'formatters': {
        'default': {
            '()': 'colorlog.ColoredFormatter',
            'format': '\t'.join([
                "%(log_color)s[%(levelname)s]",  # log level
                "asctime:%(asctime)s",  # log output date
                "process:%(process)d",  # process name
                "thread:%(thread)s",
                "module:%(module)s",
                "%(pathname)s:%(lineno)d",
                "message:%(message)s",
            ]),
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'simple': {
            '()': 'colorlog.ColoredFormatter',
            'format': '\t'.join([
                "%(log_color)s[%(levelname)s]",  # log level
                "asctime:%(asctime)s",  # log output date
                "message:%(message)s",
            ]),
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'query': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(cyan)s[SQL] %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': "DEBUG",
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'crawler.log'),
            'formatter': 'default',
            'backupCount': 3,
            'maxBytes': 1024 * 1024 * 2,
        },
        'console': {
            'level': "DEBUG",
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'console_simple': {
            'level': "DEBUG",
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'query': {
            'level': "DEBUG",
            'class': 'logging.StreamHandler',
            'formatter': 'query',
        },
    },
    'root': {
        'handlers': ['file', 'console_simple'],
        'level': 'DEBUG',
    },
    'loggers': {
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'my_project': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}