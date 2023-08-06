""" Основной модуль пакета rcore

"""

# Версия приложения
__version__ = 1.1

# Отладка
__debug_mod__ = True

import os
import pathlib as pa
import typing as _T

import rlogging

from rcore import analyze
from rcore import exception as ex
from rcore import rpath
from rcore.config import cf

""" Основные переменные приложения """


analyze.init('rcore')

logger = rlogging.get_logger('mainLogger')


def logging_setup():
    """ Настройка логеров """

    lineFormater = rlogging.formaters.LineFormater()

    # Вывод критических ошибок
    # terminalPrinter = rlogging.printers.TerminalPrinter()
    # terminalPrinter.formater = lineFormater

    # mainProcessHandler = rlogging.handlers.MainProcessHandler()
    # mainProcessHandler.printersPool = rlogging.printers.PrintersPool([
    #     terminalPrinter
    # ])

    # Вывод всех сообщений
    filePrinter = rlogging.printers.FilePrinter(
        lineFormater,
        str(rpath.rPath('logs/rcore.log', fromPath='project.cache'))
    )

    subProcessHandler = rlogging.handlers.SubProcessHandler()
    subProcessHandler.printersPool = rlogging.printers.PrintersPool([
        filePrinter
    ])

    logger.handlersPool = rlogging.handlers.HandlersPool([
        # mainProcessHandler,
        subProcessHandler
    ])
    logger.minLogLevel = 0

    rlogging.start_loggers()


""" Пример функций инициализации приложения """


def set_path(userPath: _T.Union[pa.Path, str], projectPath: _T.Union[pa.Path, str, None] = None):
    """ Инициализация корневых путей приложения """

    from . import rpath

    if isinstance(userPath, str):
        userPath = pa.Path(userPath)

    if projectPath is None:
        projectPath = pa.Path(__file__).parent

    elif isinstance(projectPath, str):
        projectPath = pa.Path(projectPath)

    rpath.rPaths.init(
        userPath,
        projectPath,
        pa.Path(__file__).parent
    )


def set_config(patterns: list = [], files: dict = {}, dictconfig: dict = {}):
    """ Определение файлов конфигурации. """

    cf.init({
        'project': patterns,
        'app': ['*.json']
    }, files, dictconfig)


""" Пример работы с rcore

Функции init и start являются примерами инициализации и запуска программы.
Функцию stop можно вызывать надстройками.

"""


def init():
    """ Инициализация приложения rcore.

    Запуск необходимых функций, процессов, etc.

    """

    logger.info('Инициализация rcore')

    logging_setup()


def stop():
    """ Остановка всех служб rcore """

    logger.info('Остановка всех служб rcore')

    analyze.stop()
    rlogging.stop_loggers()


@ex.exceptions(stop)
def start():
    """ Запуск основного функционала приложения """

    logger.info('Запуск rcore')

    set_path(os.getcwd(), os.path.dirname(__file__))
    init()

    from . import cli
    cli.start()
