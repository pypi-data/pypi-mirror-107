import logging
from logging import config as logging_config
from logging import handlers

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters":
        {
            "default": {
                "format": "%(asctime)s  %(filename)s:%(lineno)3d | %(levelname)s  %(message)s"
            },
            "root": {
                "format": "ROOT- %(asctime)s  %(filename)s:%(lineno)3d | %(levelname)s  %(message)s"
            }
        },
    "handlers":
        {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default"
            },
            "root_console": {
                "class": "logging.StreamHandler",
                "formatter": "root"
            }
        },
    "loggers":
        {
            "app":
                {
                    "handlers": ["console"],
                    "level": "INFO",
                    # Don't send it up my namespace for additional handling
                    "propagate": False
                }
        },
    "root": {
        "handlers": ["root_console"],
        "level": "INFO"
    }
}


def file_handler(filename):
    timed_rotating_file_handler = handlers.TimedRotatingFileHandler(
        filename=filename, when="D", backupCount=3, encoding='utf-8'
    )
    format_str = logging.Formatter(LOGGING_CONFIG['formatters']['default']['format'])
    timed_rotating_file_handler.setFormatter(format_str)
    return timed_rotating_file_handler


logging_config.dictConfig(LOGGING_CONFIG)
format_str = logging.Formatter(LOGGING_CONFIG['formatters']['default']['format'])
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(format_str)
Logger = logging.getLogger('app')
# Logger.addHandler(stream_handler)
