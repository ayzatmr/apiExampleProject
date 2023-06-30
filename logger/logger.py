import logging.config
import os
import pathlib
from logging import handlers

import yaml

from definitions import LOGGER_CONF_PATH, ROOT_DIR
from utils.decorator import func_once


def set_log_path(path):
    return os.path.join(ROOT_DIR, 'logger', 'logs', path)


def debug_file_handler():
    """
    maxBytes = value in Bytes - sent param to constructor if you want to split log file into few files
    mode='w' or 'a' - sent param to constructor if you want to rewrite debug file for any test
    If maxBytes had been sent 'mode' param automatically sets to 'a'
    """
    pathlib.Path(os.path.join(ROOT_DIR, 'logger', 'logs')).mkdir(parents=True, exist_ok=True)
    handler = handlers.RotatingFileHandler(set_log_path('debug.log'), mode='w', backupCount=20, encoding='utf8',
                                           maxBytes=2560000)

    return handler


def info_file_handler():
    pathlib.Path(os.path.join(ROOT_DIR, 'logger', 'logs')).mkdir(parents=True, exist_ok=True)
    return handlers.RotatingFileHandler(set_log_path('info.log'), backupCount=20, encoding='utf8', maxBytes=2560000)


def error_file_handler():
    pathlib.Path(os.path.join(ROOT_DIR, 'logger', 'logs')).mkdir(parents=True, exist_ok=True)
    return handlers.RotatingFileHandler(set_log_path('error.log'), backupCount=20, encoding='utf8', maxBytes=2560000)


@func_once
def prepared_logger():
    """
    Setup logging configuration
    """
    if os.path.exists(LOGGER_CONF_PATH):
        with open(LOGGER_CONF_PATH, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(filename="myLog.log", level=logging.DEBUG)
    return logging.getLogger()
