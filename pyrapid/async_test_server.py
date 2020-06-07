import asyncio
import os
import platform
import sys
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from cloudpickle.cloudpickle import dumps, loads

pExecutor = ProcessPoolExecutor(max_workers=os.cpu_count())
tExecutor = ThreadPoolExecutor(max_workers=os.cpu_count())
PORT = os.environ.get('PORT') or 8888
BUFF = 1024 * 10


async def install(package):
    await asyncio.subprocess.create_subprocess_exec(sys.executable, "-m", "pip", "install", package)


async def set_buffer_size(new_buff_size):
    global BUFF
    BUFF = new_buff_size


COMMAND_GLOBAL_DICT = {
    'pip': install,
    'setBUFF': set_buffer_size,

}


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

    recv_commands = recv_dict.get('commands')

    if recv_commands:
        for command, args in recv_commands.items():
            if command in COMMAND_GLOBAL_DICT.keys():
                await COMMAND_GLOBAL_DICT[command](*args)

    loop = asyncio.get_event_loop()
    if recv_dict['exec_type'] == 'THREAD':
        task = loop.run_in_executor(tExecutor, func, *args)
        time_start = time.monotonic()
        result = await asyncio.gather(task)
        time_end = time.monotonic()
    elif recv_dict['exec_type'] == 'PROCESS':
        task = loop.run_in_executor(pExecutor, run_encoded, data)
        time_start = time.monotonic()
        result = await asyncio.gather(task)
        time_end = time.monotonic()
    else:
        time_start = time.monotonic()
        result = func(*args)
        time_end = time.monotonic()

    results = {
        'result': result,
        'duration': time_end - time_start,
        'hostname': platform.node()
    }

    serialized_result = dumps(results)
    writer.write(serialized_result)
    await writer.drain()

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
