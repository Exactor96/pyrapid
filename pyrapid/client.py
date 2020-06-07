import asyncio
import socket
import time

import requests
from dill import dumps, loads

BUFF = 1024 * 10
#HOST = 'ip172-18-0-9-brc84ptim9m000c5ovug-8888.direct.labs.play-with-docker.com'
HOST = 'localhost'
PORT = 8888


def death_list(n):
    lst = []
    for i in range(n):
        for j in range(n):
            for g in range(n):
                lst.append([i, j, g])
    size = lst.__sizeof__()

    if size < 1024:
        return f'{size} bytes'
    elif size / 1024 < 1024:
        return f'{lst.__sizeof__() / 1024} kilobytes'
    elif size / 1024 ** 2 < 1024:
        return f'{lst.__sizeof__() / (1024 ** 2)} megabytes'
    elif size / 1024 ** 3 < 1024:
        return f'{lst.__sizeof__() / (1024 ** 3) } gigabytes'
    else:
        return f'{lst.__sizeof__()} bytes or too much'


def colatz(num):
    res = []
    if num <= 1:
        return [1, ]
    while num != 1:
        if num % 2 == 0:
            res.append(num)
            num /= 2
        elif num % 2 == 1:
            res.append(num)
            num = num * 3 + 1
    return res


def factorial1(num):
    ts = time.monotonic()
    print(f'num {num}')
    f = 1
    for i in range(1, num + 1):
        f *= i
    return f'last_num: {f % 10} ,factorial_size: {f.__sizeof__()}, {time.monotonic() - ts}'


def make_db(name):
    import sqlite3
    sqlite3.connect(str(name)+'.sqlite3')


def send_func(func, args, exec_type):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer_dict = {'func': func, 'args': args, 'exec_type': exec_type}
    transfer_data = dumps(transfer_dict)
    s.connect((HOST, PORT))
    s.send(transfer_data)
    result_data = s.recv(BUFF)
    result = loads(result_data)
    print(result)


async def tcp_echo_client(func, args, exec_type, loop):
    reader, writer = await asyncio.open_connection('localhost', 8888,
                                                   loop=loop)

    transfer_dict = {'func': func, 'args': args, 'exec_type': exec_type}
    transfer_data = dumps(transfer_dict)
    writer.write(transfer_data)
    writer.close()

    result_data = await reader.read(-1)

    print(result_data)
    if result_data:
        result = loads(result_data)
        print(result)
        return result
    else:
        print('empty result')
        return None


def count_len_web(url, delay):
    response = requests.get(url)
    import time
    time.sleep(delay)
    return url, f'delayed: {delay}', f'size: {response.__sizeof__()}'


def func_inner_call():
    print(death_list(100))
    print(death_list(200))
    print(factorial(25))
    print(make_db(789))


def gen_collatz(limit, loop):
    i=1
    while i <= limit:
        yield colatz, (i,), loop
        i+=1


def gen_factorials(start, stop, loop):
    i = start
    while i <= stop:
        yield factorial, (i,), loop
        i+=1


async def main():
    loop = asyncio.get_event_loop()
    t = asyncio.create_task(tcp_echo_client(factorial, (100000,), 'THREAD', loop))
    await asyncio.gather(t)
    # tasks = [asyncio.create_task(each)
    #          for each in [
    #              tcp_echo_client(factorial, (100000,), 'THREAD', loop),
    #              tcp_echo_client(factorial, (100001,), 'THREAD', loop),
    #              # tcp_echo_client(colatz, (100002,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100003,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100004,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100005,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100006,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100007,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100008,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100009,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100010,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100011,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100012,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100013,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100014,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100015,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100016,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100017,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100018,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100019,), 'PROCESS', loop),
    #              # tcp_echo_client(colatz, (100020,), 'PROCESS', loop),
    #          ]
    #
    #          ]
    #
    # for task in tasks:
    #     await asyncio.gather(task)

if __name__ == '__main__':
    import time
    start = time.monotonic()
    # asyncio.run(main())
    # print(time.monotonic() - start)

    send_func(factorial1, (100000,), 'THREAD')
    send_func(factorial1, (100000,), 'PROCESS')
    send_func(factorial1, (100000,), 'PROCESS')
    send_func(factorial1, (100000,), 'PROCESS')
    send_func(factorial1, (100000,), 'PROCESS')
    send_func(factorial1, (100000,), 'PROCESS')
    send_func(factorial1, (100000,), 'PROCESS')
    print(f'duration: {time.monotonic() - start}')
    # start = time.monotonic()
    # for i in range(100001):
    #     print(colatz(i))
    #
    # print(time.monotonic() - start)
