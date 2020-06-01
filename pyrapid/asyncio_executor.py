import asyncio
from concurrent.futures import ProcessPoolExecutor
import time


def factorial(num):
    f = 1
    for i in range(1, num + 1):
      f *= i
    return f'last_num: {f % 10} ,factorial_size: {f.__sizeof__()}'


def eratosthenes(n):     # n - число, до которого хотим найти простые числа
    start = time.monotonic_ns()
    sieve = list(range(n + 1))
    sieve[1] = 0    # без этой строки итоговый список будет содержать единицу
    for i in sieve:
        if i > 1:
            for j in range(i + i, len(sieve), i):
                sieve[j] = 0
    sieve1 = [x for x in sieve if sieve[x] != 0]
    print(f'eratosthenes: {n}', time.monotonic_ns() - start)
    return sieve1


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


async def main(loop):
    executor = ProcessPoolExecutor()
    tasks = []
    for i in [100, 1000, 10000, 100000, 10**6, 10**7, 10**8]:
        tasks.append(loop.run_in_executor(executor, eratosthenes, i))

    #asyncio.gather()
    # print(tasks)
    # r = await tasks[0]
    # print(r)
    task = await asyncio.gather(*tasks)
    #print(task)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    start = time.monotonic()
    loop.run_until_complete(main(loop))
    # for i in [100, 1000, 10000, 100000, 10**6, 10**7, 10**8]:
    #     eratosthenes(i)
    print(time.monotonic() - start)