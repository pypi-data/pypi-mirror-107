from __future__ import annotations

import functools
import re
import sys
import traceback
import typing as _T
from copy import copy
from dataclasses import dataclass

import rlogging

logger = rlogging.get_logger('mainLogger')


class rTraceback(object):
    """ Traceback Class.
        Each of the values ​​indicates a stage in the program that led to the error.

    Values:
        child (rTraceback) - next stage
    """

    text: _T.Union[str, list, None] = None
    child: _T.Union[rTraceback, None] = None

    def __init__(self, text: _T.Union[str, list, None] = None):
        self.text = text

    def message(self) -> list[str]:
        if isinstance(self.text, str):
            return [self.text]
        return []

    def add_child(self, tp: rTraceback):
        searchchelid = self
        while True:
            if searchchelid.child:
                searchchelid = searchchelid.child
            else:
                searchchelid.child = tp
                break


def print_traceback(tb: rTraceback):
    message = tb.message()

    t = '  '
    if message is None:
        pass
    elif isinstance(message, list):
        for i in message:
            if len(t) > 4:
                t = '  '
            print(t + i)
            t += '  '
    else:
        raise DeveloperIsShitError()

    if tb.child:
        print_traceback(tb.child)


class rTrConfig(rTraceback):

    dictpath: list
    error_value: str

    def __init__(self, dictpath: list, error_value: _T.Any):
        self.dictpath = dictpath
        self.error_value = str(error_value)

    def message(self):
        if self.child and type(self.child) == rTraceback:
            message = [
                'Config: ' + ' > '.join(self.dictpath) + ', error value: ' + self.error_value,
                self.child.message
            ]
        else:
            message = [
                'Config: ' + ' > '.join(self.dictpath),
                'Error value: ' + self.error_value
            ]

        return message


_rTrFileSpan = _T.Union[
    tuple[int, int],
    list[tuple[int, int]],
    None
]


class rTrFile(rTraceback):

    path: str
    span: _rTrFileSpan

    def __init__(self, path: str, span: _rTrFileSpan = None):
        self.path = path
        self.span = span

    def message(self):

        from . import utils

        message = []

        if self.span is not None:
            
            filePath = utils.rPath(self.path)

            spans = self.span if isinstance(self.span, list) else [self.span]
            spans_text = utils.file_span_separate(filePath, spans)

            start_line = utils.search_point_by_lines(filePath, spans[0][0])

            message += [
                f'File "{self.path}", line {str(start_line)}',
                ' ... '.join(spans_text)
            ]

        else:
            message = [
                f'File "{self.path}"',
                'Error in this file'
            ]

        return message


class rEx(Exception):
    """ Extended Exception Class

    Values:
        description (str): exception description

    """

    description: _T.Union[str, None] = None

    def __str__(self):
        if self.description is None:
            return 'Extended Exception Class'
        return self.description

    def __init__(self, description: _T.Union[str, None] = None):
        if description is not None:
            self.description = description


class rExError(rEx):
    """ Исключение подразумевающее ошибку выполнения """

    traceback: _T.Union[rTraceback, None] = None

    def append_traceback(self, tb: rTraceback):
        child = copy(self.traceback)
        self.traceback = tb
        if child:
            self.traceback.add_child(child)
        return self


class rExInfo(rEx):
    """ Информационное исключение """

    text: _T.Union[str, None] = None

    def __init__(self, description: _T.Union[str, None], text: _T.Union[str, None] = None):
        if description is not None:
            self.description = description

        if text is not None:
            self.text = text


class rException(rExError):
    """ Обертка над встроенными исключениями python """

    def __init__(self, exLevel: Exception):
        self.description = type(exLevel).__name__ + ': ' + str(exLevel)


def print_python_traceback(exError):

    from . import main

    if main.__debug_mod__ and type(exError) not in ignoreExceptions:
        exc_type, exc_value, exc_tb = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_tb)
        print()


def exceptions(stopCallback: _T.Union[_T.Callable, None] = None):
    """ Декоратор для обработки исключений.

    В конце выполнения декоратор вызовет функцию остановки приложения.

    Args:
        stopCallback (_T.Callable, optional): Функция для корректной остановки приложения.

    """

    @functools.wraps(exceptions)
    def wrapper(func):

        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            # Обработка исключений об ошибках
            except rExError as exError:
                logger.exception(exError)

                print_python_traceback(exError)

                if exError.traceback:
                    print('Traceback:')
                    print_traceback(exError.traceback)
                    print()

                if exError.description is not None:
                    print(type(exError).__name__ + ': ' + exError.description)

            # Обработка информационных исключений
            except rExInfo as exInfo:
                logger.exception(exInfo)

                print_python_traceback(exInfo)

                print(exInfo.text)

            # Обработка остальных исключений
            except rEx as ex:
                logger.exception(ex)

                print(type(ex).__name__ + ': ', sep='', end='')
                if ex.description:
                    print(ex.description, end='')
                print()

            # Обработка стандартных исключений
            except Exception as errEx:
                logger.exception(errEx)

                print_python_traceback(errEx)

            finally:
                logger.warning('Программа завершилась из-за исключения')
                stopCallback()
                sys.exit(1)

        return inner
    return wrapper


class DDExit(rExInfo):
    """ Вспомогательное исключение для завершения выполнения кода при вызове utils.dd """

    description = 'DD - method for detailed code debugging'


class DeveloperIsShitError(rExError):
    """ Вспомогательное исключение для ловли ситуаций, которые, казалось бы, я предусмотрел """

    def __init__(self, message: str = 'ну тупой'):
        self.description = message


class NotInitPathError(rExError):
    """ Задействован модуль rpath без инициализации RootPaths """

    description = 'Корневые пути проекта не были инициализированны.'


class DirNotFile(rExError):
    """ Попытка выполнить файловую операцию к директори """

    def __init__(self, path):
        self.description = f'You tried to apply a file operation to a folder: "{path}"'


class FileNotDir(rExError):
    """ Попытка выполнить папочную операцию к файлу """

    def __init__(self, path):
        self.description = f'You tried to perform a folder operation on a file: "{path}"'


class NotInitConfig(rExError):
    """ Не инициализирована конфигурация """

    description = 'Not init config data'


class NotInitConfigFile(rExError):
    """ Не обьявлен именованный файл конфигурации """

    def __init__(self, file):
        self.description = f"Config file named {file} not initialized"


@dataclass
class CliHelpPrint(rExInfo):
    """ Вывод информации от CLI. """

    text: str


@dataclass
class CliErrorRequired(rExInfo):
    """ Пропуск обязательного аргумента у команды. """

    text: str


@dataclass
class CliErrorType(rExInfo):
    """ Указано недопустимое типом значение для параметра. """

    text: str


class CliErrorParseArgument(rExError):
    """ В команде содержится невалидный аргумент """

    def __init__(self, word: str):
        self.description = f'В команде содержится невалидный аргумент: "{word}"'


@dataclass
class CliArgumentError(rExError):
    """ Ошибка в обработчике команды запуска """

    description: str


class ItemNotFound(rExError):
    """ В неком наборе значений не найден искомый элемент """

    def __init__(self, array: _T.Any, key: str):
        if isinstance(array, dict):
            self.description = f'in an array where keys are: {list(array.keys())} en will find the key "{key}"'
        else:
            self.description = f'In list "{array}" key "{key}" not found.'


class NoChangeType(rExError):
    """ Невозможно привести к типу """

    def __init__(self, expected: type, received: _T.Any):
        self.description = f'Cannot cast value "{received}" to type "{received}"'


ignoreExceptions = [DDExit]
