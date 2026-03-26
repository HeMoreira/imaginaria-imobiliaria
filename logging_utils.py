import logging
from logging.config import dictConfig
from flask import request, has_request_context

# Um filtro customizado para pegar dados da requisição Flask se ela existir
class RequestContextFilter(logging.Filter):
    def filter(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
        else:
            record.url = 'N/A'
            record.remote_addr = 'N/A'
            record.method = 'N/A'
        if isinstance(record.msg, str):
            record.msg = record.msg.replace('\n', ' [/N] ').replace('\r', ' [/N] ')
        return True

def init_app_logging(app):
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'request_context': {
                '()': RequestContextFilter,
            },
        },
        'formatters': {
            'standard': {
                'format': '%(asctime)s | %(levelname)s | %(remote_addr)s | %(method)s %(url)s | %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'filters': ['request_context'],
            },
            'security_file': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/security.log',
                'maxBytes': 5000000,
                'backupCount': 3,
                'formatter': 'standard',
                'filters': ['request_context'],
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default', 'security_file'],
                'level': 'INFO',
                'propagate': True
            }
        }
    }
    
    dictConfig(LOGGING_CONFIG)