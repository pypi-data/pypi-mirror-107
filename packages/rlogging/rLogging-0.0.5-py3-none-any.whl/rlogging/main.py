
from __future__ import annotations

import typing as _T

from rlogging import formaters, handlers, loggers, printers

LOGGING_LEVELS = {
    0: 'RUBBISH',
    20: 'DEBUG',
    40: 'INFO',
    60: 'WARNING',
    80: 'ERROR',
    100: 'CRITICAL',
}


loggersDict: dict[str, loggers.BaseLogger] = {}


def registration_logger(loggerName: str, loggerType: _T.Type[loggers.BaseLogger]):
    """ Регистрация нового логера с неким типом

    Args:
        loggerName (str): Имя логера
        loggerType (_T.Type[loggers.BaseLogger]): Тип логера

    """

    loggersDict[loggerName] = loggerType(loggerName)


def get_logger(loggerName: str) -> _T.Union[loggers.BaseLogger, loggers.Logger]:
    """ Получение логера.

    Если логер не создан - создание.

    Args:
        loggerName (str): Имя логера

    """

    if loggerName not in loggersDict:
        raise KeyError('Логгер {0} не зарегистрирован'.format(
            loggerName
        ))

    return loggersDict[loggerName]


def construct_logger(loggerName: str, ):
    """ Создание логера

    До создания, все логи хранятся в памяти основного потока.

    После создания логера, очередь передастся в Хендлеры.

    """


def start_loggers():
    """ Остановка всех логеров и их хендлеров

    Raises:
        AttributeError: Попытка запустить логер или хендлер, которые будет бесполезны

    """

    for _, logger in loggersDict.items():

        if logger.handlersPool is None:
            raise AttributeError('Попытка запустить логер ({0}), у которого не установлен пул хендлеров'.format(
                logger.name
            ))

        __start_handlers(logger)
        logger.start()


def __start_handlers(logger: loggers.BaseLogger):
    for handler in logger.handlersPool.handlers:
        if handler.printersPool is None:
            raise AttributeError('Попытка запустить логер ({0}), у которого есть хендлер ({1}), у которого не установлен пул принтеров'.format(
                logger.name,
                handler.__class__.__name__
            ))

        for printer in handler.printersPool.printers:
            printer.start()

        handler.start()


def stop_loggers():
    """ Остановка всех логеров и их хендлеров """

    for _, logger in loggersDict.items():
        for handler in logger.handlersPool.handlers:
            for printer in handler.printersPool.printers:

                printer.stop()
            handler.stop()
        logger.stop()
