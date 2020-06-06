import asyncio
import os
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor

from .strategy import MultiProcessStrategy, MultiThreadStrategy


class Executor:
    """
    Класс исполнителя
    """

    class Queues:
        """Вложенный класс для очередей под каждый вид исполнения"""
        def __init__(self):
            self.process_execution_queue = []
            self.thread_execution_queue = []
            self.asyncio_execution_queue = []

        def add_task(self, task, execution_strategy):
            if execution_strategy == isinstance(MultiProcessStrategy):
                self.process_execution_queue.append(task)
            elif execution_strategy == isinstance(MultiThreadStrategy):
                self.thread_execution_queue.append(task)
            elif execution_strategy == isinstance(AsyncStrategy):
                self.asyncio_execution_queue.append(task)

        def get_task(self, execution_strategy):
            if execution_strategy == isinstance(MultiProcessStrategy):
                return self.process_execution_queue.pop()
            elif execution_strategy == isinstance(MultiThreadStrategy):
                return self.thread_execution_queue.pop()
            elif execution_strategy == isinstance(AsyncStrategy):
                return self.asyncio_execution_queue.pop()

    def __init__(self, data: dict, config: dict):
        """
        Конструктор класса
        :param data:
        :param config:
        """
        self.config = config
        self.process_pool = ProcessPoolExecutor(max_workers=config.get('max_process')
                                                or self._get_default_max_process())

        self.thread_pool = ThreadPoolExecutor(max_workers=config.get('max_thread_count')
                                              or self._get_default_thread_count())
        self.asyncio_loop = asyncio.get_event_loop()
        self.venv = Venv()
        self.strategy = config['strategy']
        self.network = Network(config['host'], config['port'])
        self.func = data['func']
        self.local_kwargs = data['local_kwargs']
        self.global_kwargs = data['global_kwargs']

    @staticmethod
    def _get_default_max_process():
        return os.cpu_count()

    @staticmethod
    def _get_default_thread_count():
        return os.cpu_count()

    def execute(self):
        """
        Функиция вызывает выполнение переданной функции и возвращает ее резальтат по сети.
        :return:
        """

        if self.strategy == isinstance(MultiProcessStrategy):
            self.venv.create()
            result = self.strategy.execute()
            self.network.send_result(result)
        elif self.strategy == isinstance(MultiThreadStrategy):
            pass
        elif self.strategy == isinstance(AsyncStrategy):
            pass


