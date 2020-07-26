class Singleton(type):

    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            ins = super().__call__(args, kwargs)
            cls._instance[cls] = ins
        return cls._instance[cls]
