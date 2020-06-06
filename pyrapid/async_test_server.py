import asyncio
import concurrent
from concurrent.futures import ProcessPoolExecutor

import cloudpickle

num = 0
num_jobs = 25
executor = ProcessPoolExecutor(max_workers=num_jobs)
BUFF = 1024 * 10


async def runner(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    loop.run_in_executor(concurrent.futures.ProcessPoolExecutor(), func, *args)


async def handle_echo(reader, writer):
    data = reader.read(BUFF)
    recv_dict = cloudpickle.loads(data)

    func = recv_dict['func']
    args = recv_dict['args']

    loop = asyncio.get_event_loop()
    print(*args)
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
    serialized_results = cloudpickle.dumps(results)
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
