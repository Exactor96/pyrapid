import cloudpickle


class Serializer:
    def __init__(self):
        pass

    @staticmethod
    def serialize(obj):
        return cloudpickle.dumps(obj)

    @staticmethod
    def deserialize(serialized):
        return cloudpickle.loads(serialized)
