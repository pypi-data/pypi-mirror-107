""" Модуль описания различных принтеров

"""

from __future__ import annotations

import os
import pathlib as pa
import re
import typing as _T

from rlogging import formaters, utils
from rlogging.records import Record


class BasePrinter(object):
    """ Основной класс Принтер.

    Принтер - функционал, который обрабатывает, выводит или сохраняет Log.

    """

    _started: bool = False

    def start(self):
        """ Запуск Принтера """

    def stop(self):
        """ Остановка Принтера """

    def __del__(self):
        if self._started:
            self.stop()

    def print(self, record: Record):
        """ Принт лога

        Args:
            record (Record): Некий лог

        Raises:
            AttributeError: Дочерний класс не переназначил данный метод

        """

        raise AttributeError('Принтер "{0}" не переназначил функцию принта'.format(
            self.__class__.__name__
        ))


class TerminalPrinter(BasePrinter):
    """ Принтер, выводящий сообщения в консоль

    Args:
        colors (dict[str, str]): Цвет сообщения соответствующий уровня лога.

    """

    formater: formaters.BaseFormater

    colors: dict = {
        'rubbish': '0m',
        'debug': '37m',
        'info': '32m',
        'warning': '33m',
        'error': '31m',
        'critical': '31m',
    }

    def __init__(self, formater: formaters.BaseFormater) -> None:
        self.formater = formater

    def print(self, record: Record):
        text = self.formater.formate(record)

        # Добавление цвета
        text = '\033[' + self.colors[record.loggingLevelLabel] + text + '\033[0m'

        print(text)


class FilePrinter(utils.SubProcessMixing, BasePrinter):
    """ Принтер, выводящий сообщения в консоль """

    formater: formaters.BaseFormater
    filePath: str
    maxFileSize: int
    checkSizeEveryThisRepeat: int

    # Количество записей без проверки веса файла
    _repeatScore: int

    def __init__(self,
                 formater: formaters.BaseFormater,
                 filePath: os.PathLike,
                 maxFileSize: int = 83886080,
                 checkSizeEveryThisRepeat: int = 500
                 ) -> None:
        """ Инициализация объекта

        Args:
            formater (formaters.BaseFormater): Форматер выходных данных.
            filePath (os.PathLike): Путь до файла.
            maxFileSize (int): Максимальное вес файла в битах. Default 10MB.
            checkSizeEveryThisRepeat (int): После скольких записей проверять файла на соответствие допустимому весу. Defaults to 500.

        """

        self.formater = formater
        self.filePath = filePath
        self.maxFileSize = maxFileSize
        self.checkSizeEveryThisRepeat = checkSizeEveryThisRepeat

        self._repeatScore = -1

    @staticmethod
    def __create_file(stringPath: str):
        """ Создание файла и родительских папок

        Args:
            stringPath (str): Путь до файла

        """

        paPath = pa.Path(stringPath)

        if not paPath.parent.is_dir():
            paPath.parent.mkdir(parents=True)

        if not paPath.is_file():
            paPath.write_text('')

    def on_process(self):
        files: dict[str, _T.IO] = {}

        while True:
            record = self._queue.get()

            if record is None:
                break

            (path, string) = record

            if path not in files:
                self.__create_file(path)
                files[path] = open(path, 'a')

            files[path].write(string)

        for path, fileIO in files.items():
            fileIO.close()

    def __check_file_size(self):
        """ Проверка файла на соответствие заданому максимальному значению.

        Returns:
            str: Файл в который нужно записывать логи.

        """

        self.filePath = os.path.abspath(self.filePath)

        try:
            size = os.path.getsize(self.filePath)

        except FileNotFoundError:
            size = 0

        if size > self.maxFileSize:
            fileNameNoExtension, fileExtension = os.path.splitext(self.filePath)
            path, fileName = os.path.split(fileNameNoExtension)

            fileNameMath = re.search(r'([\s\S]*)\.(\d*)$', fileName)
            if fileNameMath is not None:
                fileName = fileNameMath.group(1)
                count = int(fileNameMath.group(2))
                count += 1
                fileName = fileName + '.' + str(count)

            else:
                fileName = fileName + '.1'

            self.filePath = path + '/' + fileName + fileExtension

    def __count_file_size(self):
        self._repeatScore += 1
        if self.checkSizeEveryThisRepeat == self._repeatScore or self._repeatScore == 0:
            self.__check_file_size()
            self._repeatScore = 0

    def print(self, record: Record):
        self.__count_file_size()

        text = self.formater.formate(record)

        text += '\n'

        self._queue.put(
            (self.filePath, text)
        )


class PrintersPool(object):
    """ Класс для создания пула Принтеров """

    printers: list[BasePrinter]

    def __init__(self, printers: list[BasePrinter]) -> None:
        self.printers = printers

    def print(self, record: Record):
        """ Передача лога в Принтеры пула

        Args:
            record (Record): Некий лог

        """

        for printer in self.printers:
            printer.print(record)
