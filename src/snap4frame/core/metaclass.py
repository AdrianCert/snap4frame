class Singleton(type):
    """
    Metaclass that allows only one instance of a class to be created.

    Usage:
    class MyClass(metaclass=Singleton):
        pass

    This metaclass ensures that only one instance of MyClass can be created.
    Subsequent calls to create an instance of MyClass will return the same instance.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
