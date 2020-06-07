import asyncio
from time import sleep, time, monotonic
from concurrent.futures import ProcessPoolExecutor



num_jobs = 4
queue = asyncio.Queue()
executor = ProcessPoolExecutor(max_workers=num_jobs)
loop = asyncio.get_event_loop()


def work(num):
    ts = monotonic()
    f = 1
    for i in range(1, num + 1):
        f *= i
    print(f'{num} last_num: {f % 10} ,factorial_size: {f.__sizeof__()}, time: {monotonic() - ts}')
    return f'{num} last_num: {f % 10} ,factorial_size: {f.__sizeof__()}'


async def producer():
    tasks = [loop.run_in_executor(executor, work, (1 + i) * 25000) for i in range(num_jobs)]
    for f in asyncio.as_completed(tasks, loop=loop):
        results = await f
        await queue.put(results)


async def consumer():
    completed = 0
    while completed < num_jobs:
        job = await queue.get()
        completed += 1


s = time()
loop.run_until_complete(asyncio.gather(producer(), consumer()))
print("duration", time() - s)