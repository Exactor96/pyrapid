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
    """Функция установки пакетов, через pip"""
    await asyncio.subprocess.create_subprocess_exec(sys.executable, "-m", "pip", "install", package)


async def set_buffer_size(new_buff_size):
    """установка значения BUFF"""
    global BUFF
    BUFF = new_buff_size


# Словарь с зарегистрированными командами
COMMAND_GLOBAL_DICT = {
    'pip': install,
    'setBUFF': set_buffer_size,

}


def run_encoded(payload):
    """fix для ошибки сериализации в интерпретаторе (ProcessPoolExecutor) не может сериализовать функцию в отличие от
    ThreadPoolExecutor, поэтому десериализация происходит внутри процесса"""
    data_dict = loads(payload)
    func = data_dict['func']
    args = data_dict['args']
    return func(*args)


async def handle_tasks(reader, writer):
    """Основная функция обработчик входящего запроса"""
    data = await reader.read(BUFF)

    # Десериализация
    recv_dict = loads(data)

    func = recv_dict['func']
    args = recv_dict['args']

    # Проверка и Исполнение команд
    recv_commands = recv_dict.get('commands')

    if recv_commands:
        for command, args in recv_commands.items():
            if command in COMMAND_GLOBAL_DICT.keys():
                await COMMAND_GLOBAL_DICT[command](*args)

    loop = asyncio.get_event_loop()

    # Проверка типа исполнения, выбор походящего исполнителя
    if recv_dict['exec_type'] == 'THREAD':
        # Исполнение в потоке
        task = loop.run_in_executor(tExecutor, func, *args)
        time_start = time.monotonic()
        result = await asyncio.gather(task)
        time_end = time.monotonic()
    elif recv_dict['exec_type'] == 'PROCESS':
        # Исполнение в процессе
        task = loop.run_in_executor(pExecutor, run_encoded, data)
        time_start = time.monotonic()
        result = await asyncio.gather(task)
        time_end = time.monotonic()
    else:
        # Исполнение в цикле asyncio
        time_start = time.monotonic()
        result = func(*args)
        time_end = time.monotonic()

    # Формирование результатов
    results = {
        'result': result,
        'duration': time_end - time_start,
        'hostname': platform.node()
    }
    # Оправка результатов обратно клиенту
    serialized_result = dumps(results)
    writer.write(serialized_result)
    await writer.drain()

    writer.close()


async def main():
    """основная функция выполняемая в цикле asyncio, создает асинхронный TCP сервер и обрабатывает запросы
    """
    server = await asyncio.start_server(
        handle_tasks, '0.0.0.0', PORT)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    # Точка входа в программу
    asyncio.run(main())
