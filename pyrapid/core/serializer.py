import cloudpickle


class Serializer:
    """
    Класс Сериализации/Десериализации
    """
    def __new__(cls):
        """
        Метод создания нового объекта вызывается всегда перед конструктором __init__()
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Serializer, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def serialize(obj: object) -> bytes:
        """
        Сериализация объекта в байт строку
        :return:
        """
        return cloudpickle.dumps(obj)

    @staticmethod
    def deserialize(serialized: bytes) -> object:
        """
        Десериализация байт сроки в объект
        :return:
        """
        return cloudpickle.loads(serialized)
