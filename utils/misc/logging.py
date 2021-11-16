import logging

file_error_handler = logging.FileHandler('handlers/errors/errors.log')
file_error_handler.setLevel(logging.ERROR)
formatter = logging.Formatter(u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')
file_error_handler.setFormatter(formatter)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )
