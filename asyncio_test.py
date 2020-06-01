import asyncio

import cloudpickle


async def print_number(number):
    print(number)

async def handle_echo(reader, writer):
    data = await reader.read(1024 * 1024 * 10)

    print(data)

    loop.run_until_complete(
        asyncio.wait([
            print_number(data)
        ])
    )
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


if __name__ == "__main__":

    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()
