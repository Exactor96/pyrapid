import abc
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os




class Strategy(metaclass=abc.ABCMeta):
    """
    Базовый класс стратегии
    """
    @abc.abstractmethod
    def execute(self):
        pass


class MultiThreadStrategy(Strategy):
    """
    Класс конкурентного исполнения
    """
    def __init__(self, function, local_kwargs: dict, global_kwargs: dict, thread_nums=os.cpu_count()):
        self.thread_count = thread_nums
        self.thread_pool = ThreadPoolExecutor(max_workers=self.thread_count)
        self.func = function
        self.local_kwargs = local_kwargs
        self.global_kwargs = global_kwargs

    def execute(self):
        """
        Функция выполнения функции в отдельном потоке конкурентно
        :return:
        """
        self.thread_pool.submit(self.func, **self.local_kwargs, **self.global_kwargs)


class MultiProcessStrategy(Strategy):
    """
    Класс многопроцессного исполнения
    """
    def __init__(self, function, local_kwargs: dict, global_kwargs: dict, max_process=os.cpu_count()):
        self.max_process = max_process
        self.process_pool = ProcessPoolExecutor(max_workers=self.max_process)
        self.func = function
        self.local_kwargs = local_kwargs
        self.global_kwargs = global_kwargs

    def get_process_pool(self):
        pass

    def execute(self):
        """
        Функция выполнения функции в отдельном процессе
        :return:
        """
        self.process_pool.submit(self.func, **self.local_kwargs, **self.global_kwargs)


