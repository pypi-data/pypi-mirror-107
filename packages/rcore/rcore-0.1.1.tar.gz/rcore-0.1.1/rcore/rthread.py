""" Модуль инструментов для работы с ветвлениямии процессов и потоков

"""

from __future__ import annotations
import multiprocessing as _M
import os
import threading as _Th
import typing as _T

import rlogging

logger = rlogging.get_logger('mainLogger')


class ThreadsPool(object):
    """ Pool группирующий список процессов """

    threads: list[_Th.Thread]

    def __init__(self) -> None:
        self.threads = []

    def append(self, thread: _Th.Thread):
        """ Запуск процесса и добавление его в pool

        Args:
            process (_Th.Thread): Новый процесс в пуле

        """

        thread.start()
        self.threads.append(thread)

    def join(self):
        """ Завершение потоков из pool """

        for thread in self.threads:
            thread.join()


class ThreadMixin(_Th.Thread):
    """ Надстройка над классом потока """

    def __init__(self, *args, **kwargs) -> None:
        logger.debug('Инициализация объекта потока-класса "{0}" : {1}'.format(
            self.__class__.__name__, os.getpid()
        ))
        super().__init__(*args, **kwargs)

    def run(self):
        logger.debug('Запуск потока-класса "{0}" : {1}'.format(
            self.__class__.__name__, os.getpid()
        ))

    def join(self, *args, **kwargs):
        logger.debug('Ожидание остановки потока-класса "{0}" : {1}'.format(
            self.__class__.__name__, os.getpid()
        ))
        super().join(*args, **kwargs)


class ProcessesPool(object):
    """ Pool группирующий список процессов """

    processes: list[_M.Process]

    def __init__(self) -> None:
        self.processes = []

    def append(self, process: _M.Process):
        """ Запуск процесса и добавление его в pool

        Args:
            process (_M.Process): Новый процесс в пуле

        """

        process.start()
        self.processes.append(process)

    def join(self):
        """ Завершение и Удаление процессов из pool """

        for process in self.processes:
            process.join()

        for process in self.processes:
            process.terminate()


class OnAsyncMixin(object):
    """ Миксин для выполнения кода некого класса в отдельном потоке/процессе """

    @classmethod
    def run_process(cls, *args, **kwargs) -> _M.Process:
        """ Создание процесса с таргетом на функцию on_process этого класса

        Args:
            args (_T.Any): Значения для инициализации объекта.
            kwargs (_T.Any): Значения для инициализации объекта.

        Returns:
            _M.Process: Новый процесс

        """

        logger.debug('Создание процесса для выполнения кода класса "{0}"'.format(
            cls.__name__
        ))

        processObj = cls(*args, **kwargs)

        return _M.Process(target=processObj.on_process)

    def on_process(self):
        """ Эта функция будет запускаться в отдельном процессе

        Raises:
            ValueError: Класс не переопределил функцию "on_process"

        """

        raise ValueError('Класс "{0}" не переопределил функцию "on_process"'.format(
            self.__class__.__name__
        ))

    @classmethod
    def run_thread(cls, *args, **kwargs) -> _Th.Thread:
        """ Создание потока с таргетом на функцию on_thread этого класса

        Args:
            args (_T.Any): Значения для инициализации объекта.
            kwargs (_T.Any): Значения для инициализации объекта.

        Returns:
            _Th.Thread: Новый процесс

        """

        logger.debug('Создание потока для выполнения кода класса "{0}"'.format(
            cls.__name__
        ))

        threadObj = cls(*args, **kwargs)

        return _Th.Thread(target=threadObj.on_thread)

    def on_thread(self):
        """ Эта функция будет запускаться в отдельном потоке

        Raises:
            ValueError: Класс не переопределил функцию "on_thread"

        """

        raise ValueError('Класс "{0}" не переопределил функцию "on_thread"'.format(
            self.__class__.__name__
        ))
