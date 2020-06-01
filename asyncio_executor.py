import asyncio
import concurrent.futures
import logging
import sys
import time


def block_task(prefix, num):
    f = 1
    for i in range(1, num + 1):
      f *= i
    return f'last_num: {f % 10} ,factorial: {f}'


async def async_task(prefix, n):
    """A coroutine intended to run in the asyncio event loop to verify that it
    works concurrently with the blocking tasks"""
    log = logging.getLogger(f'{prefix}_asyncio({n})')
    for i in range(5):
        log.info(f'running {i}')
        await asyncio.sleep(0.5)
    log.info('done')
    return f'a{n ** 2}'


async def run_tasks(prefix, executor, func, *args):
    """Runs blocking tasks in the executor and spawns off a few coroutines to run
    concurrently with the blocking tasks."""
    log = logging.getLogger(f'{prefix}_run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()

    blocking_tasks = [
                         loop.run_in_executor(executor, func, prefix, *args)
                     ] + [async_task(prefix, *args)]

    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='PID %(process)5s %(threadName)-25s %(name)-25s: %(message)s',
        stream=sys.stderr,
    )

    th_executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    pr_executor = concurrent.futures.ProcessPoolExecutor(max_workers=3)

    event_loop = asyncio.get_event_loop()
    try:
        w = asyncio.wait([run_tasks('th', th_executor, block_task, 125),
                          run_tasks('pr', pr_executor, block_task, 125)
                          ])
        event_loop.run_until_complete(w)
    finally:
        event_loop.close()


asyncio.run(main())