import os
import socket

from cloudpickle import dumps, loads

BUFF = 1024 * 10

HOST = '192.168.1.181'
PORT = 8888


def factorial1(num):
    """Функция вычисления факториала"""
    ts = time.monotonic()
    f = 1
    for i in range(1, num + 1):
        f *= i
    return f'last_num: {f % 10} ,factorial_size: {f.__sizeof__()}, {time.monotonic() - ts}'


def send_func(func, args, exec_type, commands_dict=None):
    """Функция отправки, сериализации и получения результата"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer_dict = {
        'func': func,
        'args': args,
        'exec_type': exec_type,
        'commands': commands_dict
    }
    transfer_data = dumps(transfer_dict)
    s.connect((HOST, PORT))
    s.send(transfer_data)
    result_data = s.recv(BUFF)
    result = loads(result_data)
    print(result)
    return result


if __name__ == '__main__':
    import time
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

    RUN_TIMES = 100
    tpe = ThreadPoolExecutor(max_workers=RUN_TIMES)
    ppe = ProcessPoolExecutor(max_workers=os.cpu_count())
    start = time.monotonic()

    # симуляция отправки от разных клиентов
    t = tpe.map(send_func,

                (factorial1 for i in range(RUN_TIMES)),
                ((100000,) for i in range(RUN_TIMES)),
                ('PROCESS' for i in range(RUN_TIMES)),
                )

    tpe.shutdown(wait=True)

    print(f'distributed duration: {time.monotonic() - start}')
    start = time.monotonic()

    # Последовательное исполнение
    for i in range(RUN_TIMES):
        factorial1(100000)
    print(f'local sync duration: {time.monotonic() - start}')

    start = time.monotonic()
    # Распараллеливание через процессы (не работает из-за большого количество одновременных задач)
    p = ppe.map(factorial1,
                (100000,) * RUN_TIMES, chunksize=os.cpu_count()

                )
    # Рабочий вариант распараллеливания через процессы
    lst = []
    for i in range(RUN_TIMES):
        lst.append(ppe.submit(factorial1, 100000))
    ppe.shutdown(wait=True)
    for res in lst:
        print(res.result())

    print(f'local multiprocess duration: {time.monotonic() - start}')

    # Локальное исполнение в потоках
    tpe = ThreadPoolExecutor(max_workers=os.cpu_count())
    start = time.monotonic()
    p = tpe.map(factorial1,
                (100000,) * RUN_TIMES

                )
    tpe.shutdown(wait=False)
    for res in p:
        print(res)

    print(f'local multithread duration: {time.monotonic() - start}')
