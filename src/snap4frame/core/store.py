import typing

from snap4frame.core.metaclass import Singleton


class Store(metaclass=Singleton):
    """A singleton store for storing data."""

    handlers: typing.Dict[typing.Any, typing.Any] = {}
