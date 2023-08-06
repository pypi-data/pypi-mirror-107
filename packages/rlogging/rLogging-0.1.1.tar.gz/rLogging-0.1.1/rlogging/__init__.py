""" Модуль гибкого логирования """

from rlogging import handlers, loggers, printers, service
from rlogging.main import (get_logger, registration_logger, start_loggers,
                           stop_loggers)

# alpha release
__version__ = '0.1.1'
