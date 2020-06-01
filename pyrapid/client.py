import asyncio
import socket
import requests
import cloudpickle

BUFF = 1024 ** 2 * 10
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


def factorial(num):
    f = 1
    for i in range(1, num + 1):
        f *= i
    return f'last_num: {f % 10} ,factorial_size: {f.__sizeof__()}'


def make_db(name):
    import sqlite3
    sqlite3.connect(str(name)+'.sqlite3')


def send_func(func, args):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer_dict = {'func': func, 'args': args}
    transfer_data = cloudpickle.dumps(transfer_dict)
    s.connect((HOST, PORT))
    s.send(transfer_data)
    result_data = s.recv(BUFF)
    result = cloudpickle.loads(result_data)
    print(result)


async def tcp_echo_client(func, args, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)

    transfer_dict = {'func': func, 'args': args}
    transfer_data = cloudpickle.dumps(transfer_dict)
    writer.write(transfer_data)
    writer.close()

    result_data = await reader.read(BUFF)
    result = cloudpickle.loads(result_data)
    print(result)


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
    tasks = [asyncio.create_task(each)
             for each in [
                 tcp_echo_client(factorial, (100000,), loop),
                 tcp_echo_client(factorial, (100001,), loop),
                 tcp_echo_client(factorial, (100002,), loop),
                 tcp_echo_client(factorial, (100003,), loop),
                 tcp_echo_client(factorial, (100004,), loop),
                 tcp_echo_client(factorial, (100005,), loop),
                 tcp_echo_client(factorial, (100006,), loop),
                 tcp_echo_client(factorial, (100007,), loop),
                 tcp_echo_client(factorial, (100008,), loop),
                 tcp_echo_client(factorial, (100009,), loop),
                 tcp_echo_client(factorial, (100010,), loop),
                 tcp_echo_client(factorial, (100011,), loop),
                 tcp_echo_client(factorial, (100012,), loop),
                 tcp_echo_client(factorial, (100013,), loop),
                 tcp_echo_client(factorial, (100014,), loop),
                 tcp_echo_client(factorial, (100015,), loop),
                 tcp_echo_client(factorial, (100016,), loop),
                 tcp_echo_client(factorial, (100017,), loop),
                 tcp_echo_client(factorial, (100018,), loop),
                 tcp_echo_client(factorial, (100019,), loop),
                 tcp_echo_client(factorial, (100020,), loop),
             ]

             ]

    results = [await asyncio.gather(task) for task in tasks]

if __name__ == '__main__':
    import time
    start = time.monotonic()
    asyncio.run(main())
    print(time.monotonic() - start)


    # start = time.monotonic()
    # for i in range(100001):
    #     print(colatz(i))
    #
    # print(time.monotonic() - start)
