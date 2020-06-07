import socket

from cloudpickle import dumps, loads

from pyrapid.test_funcs import *

BUFF = 1024 * 10

HOST = 'localhost'
PORT = 8888


def send_func(func, args, exec_type, commands_dict=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer_dict = {
        'func': func,
        'args': args,
        'exec_type': exec_type,
        'commands': commands_dict
    }
    transfer_data = dumps(transfer_dict)
    s.connect((HOST, PORT))
    s.send(transfer_data)
    result_data = s.recv(BUFF)
    result = loads(result_data)
    print(result)
    return result

if __name__ == '__main__':
    import time
    from concurrent.futures import ThreadPoolExecutor

    tpe = ThreadPoolExecutor()
    start = time.monotonic()

    t = tpe.map(send_func,

                (factorial1 for i in range(1)),
                ((100000,) for i in range(1)),
                ('PROCESS' for i in range(1)),
            )

    tpe.shutdown(wait=True)
    print(f'duration: {time.monotonic() - start}')
