import time

import requests


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
        return f'{lst.__sizeof__() / (1024 ** 3)} gigabytes'
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
    sqlite3.connect(str(name) + '.sqlite3')


def count_len_web(url, delay):
    response = requests.get(url)
    import time
    time.sleep(delay)
    return url, f'delayed: {delay}', f'size: {response.__sizeof__()}'


def func_inner_call():
    print(death_list(100))
    print(death_list(200))
    print(factorial1(25))
    print(make_db(789))


def gen_collatz(limit, loop):
    i = 1
    while i <= limit:
        yield colatz, (i,), loop
        i += 1


def gen_factorials(start, stop, loop):
    i = start
    while i <= stop:
        yield factorial1, (i,), loop
        i += 1
