import logging
import sys

import config


class LoggerFactory(object):
    _logger = None

    def __init__(self):
        pass

    @staticmethod
    def get_logger():
        if LoggerFactory._logger:
            return LoggerFactory._logger

        logger = logging.getLogger("LetoLogger")
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(config.LOG_FORMAT)

        file_logger = logging.FileHandler(config.LOG_FILE, "w")
        file_logger.setLevel(logging.DEBUG)
        file_logger.setFormatter(formatter)

        console_logger = logging.StreamHandler(sys.stdout)
        console_logger.setLevel(logging.INFO)
        console_logger.setFormatter(formatter)

        logger.addHandler(file_logger)
        logger.addHandler(console_logger)

        LoggerFactory._logger = logger

        return logger
