import yaml
from pyrapid.core.serializer import Serializer
import socket


class Config:

    def __init__(self, name, hostname, port):
        self.name = name
        self.hostname = hostname
        self.port = port

    def __repr__(self):
        return f'Config:{self.name}'


class Configurator:
    _configs_dict = dict()

    def __init__(self, path_to_config='config_client.yaml'):
        with open(path_to_config, 'r') as f:
            self._config = yaml.safe_load(f)

    def __new__(cls):
        """
        Метод создания нового объекта вызывается всегда перед конструктором __init__()
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configurator, cls).__new__(cls)
        return cls.instance

    def create_configs(self):
        for config in self._config.get('clusters'):
            for name, values in config.items():
                self._configs_dict.update({name: Config(name=name, **values)})

    def get_config(self, name):
        if not self._configs_dict.items():
            self.create_configs()
        return self._configs_dict.get(name)


class Decorators:

    def __init__(self, config: Config):
        self._config = config

    @staticmethod
    def remote(func, args, config, exec_type):

        sock = socket.socket()
        sock.connect((config.hostname, config.port))
        snd = {'func': func, 'args': args, 'exec_type': exec_type}
        sock.sendall(Serializer.serialize(snd))
        result_data = sock.recv(1024 ** 2 * 10)
        result = Serializer.deserialize(result_data)
        return result




c = Configurator()
remote = Decorators.remote


#@remote(c.get_config('cluster4'), 'PROCESS')
def srt(l):
    return sorted(l)


srt([1, 45, 65, 3, 2, 54, 7, 9865, 545345, 23, 11])

print(remote(func=srt, args=([1, 45, 65, 3, 2, 54, 7, 9865, 545345, 23],),
             config=c.get_config('cluster4'), exec_type='THREAD'))
