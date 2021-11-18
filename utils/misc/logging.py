import logging


class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.__level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno <= self.__level


file_error_handler = logging.FileHandler('handlers/errors/errors.log')
file_error_handler.setLevel(logging.ERROR)
formatter = logging.Formatter(u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')
file_error_handler.setFormatter(formatter)
file_info_handler = logging.FileHandler('info.log')
file_info_handler.setLevel(logging.INFO)
file_info_handler.addFilter(LevelFilter(logging.INFO))
file_info_handler.setFormatter(formatter)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )
