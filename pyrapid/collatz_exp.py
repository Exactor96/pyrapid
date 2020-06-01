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


import time

start = time.monotonic()

for i in range(40000, 40021, 1):
    factorial(i)

print(time.monotonic() - start)