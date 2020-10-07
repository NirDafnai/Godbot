import logging
import sys

import config

LOGGER_NAME = "LetoLogger"


class LoggerFactory(object):
    _logger = None

    @staticmethod
    def get_logger():
        if LoggerFactory._logger is not None:
            return LoggerFactory._logger

        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(config.LOG_FORMAT)

        file_logger = LoggerFactory._init_file_logger(formatter, logging.DEBUG)
        console_logger = LoggerFactory._init_stream_logger(formatter, logging.INFO)

        logger.addHandler(file_logger)
        logger.addHandler(console_logger)

        LoggerFactory._logger = logger

        return logger

    @staticmethod
    def _init_file_logger(formatter: logging.Formatter, level):
        file_logger = logging.FileHandler(config.LOG_FILE, "w")
        file_logger.setLevel(level)
        file_logger.setFormatter(formatter)
        return file_logger
    
    @staticmethod
    def _init_stream_logger(formatter: logging.Formatter, level):
        console_logger = logging.StreamHandler(sys.stdout)
        console_logger.setLevel(level)
        console_logger.setFormatter(formatter)
        return console_logger
