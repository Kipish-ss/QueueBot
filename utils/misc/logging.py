import logging
import sys


class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.__level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno <= self.__level


def get_logger(handle_info=True, handle_errors=True):
    logger = logging.getLogger(__name__)
    format_str = u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s'
    formatter = logging.Formatter(format_str)
    logger.setLevel(level=logging.INFO)
    path = sys.path[1]
    if handle_info:
        file_info_handler = logging.FileHandler(f'{path}/info.log')
        file_info_handler.setLevel(logging.INFO)
        file_info_handler.addFilter(LevelFilter(logging.INFO))
        file_info_handler.setFormatter(formatter)
        logger.addHandler(file_info_handler)
    if handle_errors:
        file_error_handler = logging.FileHandler(f'{path}/errors.log')
        file_error_handler.setLevel(logging.ERROR)
        file_error_handler.setFormatter(formatter)
        logger.addHandler(file_error_handler)
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.INFO)
    return logger


logger = get_logger()
