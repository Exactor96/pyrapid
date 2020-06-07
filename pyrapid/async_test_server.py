import asyncio
import concurrent
import logging
import time
from concurrent.futures import ProcessPoolExecutor
from dill import dumps, loads
#from cloudpickle.cloudpickle import dumps, loads
#from pathos.multiprocessing import ProcessPool


num = 0
num_jobs = 25
#executor = ProcessPool(max_workers=num_jobs)
BUFF = 1024 * 10


async def run_blocking_tasks(executor, func, args):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    result = loop.run_in_executor(executor, func, args)
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.gather(result)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')
    return results


async def handle_echo(reader, writer):
    data = await reader.read(BUFF)
    recv_dict = loads(data)

    func = recv_dict['func']
    args = recv_dict['args']

    loop = asyncio.get_event_loop()
    print(f'args: {args}')
    print(f"exec_type: {recv_dict['exec_type']}")
    if recv_dict['exec_type'] == 'THREAD':
        task = loop.run_in_executor(concurrent.futures.ThreadPoolExecutor(), func, *args)
        results = await asyncio.gather(task)

    elif recv_dict['exec_type'] == 'PROCESS':
        task = loop.run_in_executor(concurrent.futures.ProcessPoolExecutor(), func, *args)
        results = await asyncio.gather(task)
    else:
        results = func(*args)

    print(type(results))
    print(f'results size {results.__sizeof__()}')
    serialized_results = dumps(results)
    print(serialized_results)

    writer.write(serialized_results)
    await writer.drain()

    print(f"Func with args {args} done!")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '0.0.0.0', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())

