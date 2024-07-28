import typing
from logging import Logger

from snap4frame.core.log import logger as lib_logger
from snap4frame.core.metaclass import Singleton
from snap4frame.types import (
    EventProcessorDirective,
    Parameters,
    ProcessorMetaField,
    SnapFrameEvent,
    SnapFrameReport,
    SnapFrameResult,
)

__all__ = [
    "Parameters",
    "SnapFrameReport",
    "SnapFrameEvent",
    "ProcessorMetaField",
    "SnapFrameResult",
    "EventProcessorDirective",
    "BaseEventProcessor",
]


class EventProcessorFactory(metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        self.data = {}

    def register(self, vault, key, value):
        if vault not in self.data:
            self.data[vault] = {}
        self.data[vault][key] = value


class EventProcessorRegistry(type):
    def __init__(cls, name, bases, attrs):
        factory = EventProcessorFactory()
        for name, value in cls.__annotations__.items():
            if value != ProcessorMetaField:
                continue
            item_value = attrs.get(name, ProcessorMetaField)
            if item_value == ProcessorMetaField:
                continue
            factory.register(name, item_value, cls)
            lib_logger.debug("Registered %s as %s with %s", cls, name, item_value)
        super().__init__(name, bases, attrs)


class BaseEventProcessor(metaclass=EventProcessorRegistry):
    config: Parameters
    logger: Logger

    def __init__(self, logger: typing.Optional[Logger] = None, **kwargs):
        self.config = Parameters(kwargs)
        self.logger = logger or lib_logger

        setup_method = getattr(self, "setup", None)
        if callable(setup_method):
            setup_method()

    def process_event(self, event: SnapFrameEvent, **kwargs) -> SnapFrameResult:
        raise NotImplementedError

    def __call__(self, *args, **kwargs) -> SnapFrameResult:
        return self.process_event(*args, **kwargs)
