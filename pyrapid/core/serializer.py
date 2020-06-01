import cloudpickle


# class Serializer:
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def serialize(obj: object) -> str:
#         return cloudpickle.dumps(obj)
#
#     @staticmethod
#     def deserialize(serialized: str) -> object:
#         return cloudpickle.loads(serialized)

class Serializer(object):
    """
    Класс сериализации
    """
    def __new__(cls):
        """
        Метод создания нового объекта вызывается всегда перед конструктором __init__()
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Serializer, cls).__new__(cls)
        return cls.instance

    def serialize(obj: object) -> str:
        """
        Сериализация объекта в байт строку
        :return:
        """
        return cloudpickle.dumps(obj)

    def deserialize(serialized: str) -> object:
        """
        Десериализация байт сроки в объект
        :return:
        """
        return cloudpickle.loads(serialized)
