""" Модуль гибкого логирования """

from rlogging import daemon, handlers, loggers, main, printers, main
from rlogging.main import (get_logger, registration_logger, start_loggers,
                           stop_loggers)

# alpha beta release
__version__ = (0, 0, 4, 'alpha', 0)
