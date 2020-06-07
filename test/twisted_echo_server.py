import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
from cloudpickle.cloudpickle import loads, dumps
from twisted.internet import reactor, protocol
import time


async def run_blocking_tasks(executor, func, args):
    log = logging.getLogger('run_blocking_tasks')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(executor, func, *args)
    ]
    log.info('waiting for executor tasks')
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')


class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        recv_data = loads(data)
        func = recv_data['func']
        args = recv_data['args']
        executor = ProcessPoolExecutor(
            max_workers=3,
        )

        event_loop = asyncio.get_event_loop()
        try:
            event_loop.run_until_complete(
                run_blocking_tasks(executor, func, args)
            )
        finally:
            event_loop.close()
        self.transport.write(data)


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000, factory)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()