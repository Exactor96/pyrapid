import asyncio
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from cloudpickle.cloudpickle import dumps, loads

pExecutor = ProcessPoolExecutor(max_workers=os.cpu_count())
tExecutor = ThreadPoolExecutor(max_workers=os.cpu_count())
PORT = 8888
BUFF = 1024 * 10

def run_encoded(payload):
    data_dict = loads(payload)
    func = data_dict['func']
    args = data_dict['args']
    return func(*args)


async def handle_tasks(reader, writer):
    data = await reader.read(BUFF)
    recv_dict = loads(data)

    func = recv_dict['func']
    args = recv_dict['args']

    loop = asyncio.get_event_loop()
    if recv_dict['exec_type'] == 'THREAD':
        task = loop.run_in_executor(tExecutor, func, *args)
        results = await asyncio.gather(task)

    elif recv_dict['exec_type'] == 'PROCESS':
        task = loop.run_in_executor(pExecutor, run_encoded, data)
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
        handle_tasks, '0.0.0.0', PORT)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())

