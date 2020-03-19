import cloudpickle


class Serializer:
    def __init__(self):
        pass

    @staticmethod
    def serialize(obj: object) -> str:
        return cloudpickle.dumps(obj)

    @staticmethod
    def deserialize(serialized: str) -> object:
        return cloudpickle.loads(serialized)
