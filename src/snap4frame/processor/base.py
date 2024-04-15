from enum import Enum
from logging import Logger
from typing import Any, Optional, TypeVar, Union

from snap4frame.core.log import logger as lib_logger
from snap4frame.core.metaclass import Singleton
from snap4frame.types import Parameters, SnapFrameReport

ProcessorMetaField = Union[int, float, str, bool, TypeVar("ProcessorMetaField")]


class EventProcessorDirective(Enum):
    CONTINUE = 0
    STOP = 1


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
            lib_logger.info("Registered %s as %s with %s", cls, name, item_value)
        super().__init__(name, bases, attrs)


class BaseEventProcessor(metaclass=EventProcessorRegistry):
    config: Parameters
    logger: Logger

    def __init__(self, logger: Optional[Logger] = None, **kwargs):
        self.config = Parameters(kwargs)
        self.logger = logger or lib_logger

        setup_method = getattr(self, "setup", None)
        if callable(setup_method):
            setup_method()

    def process_event(
        self, event: Union[SnapFrameReport, Any], *args, **kwargs
    ) -> Union[EventProcessorDirective, SnapFrameReport, Any]:
        raise NotImplementedError

    def __call__(
        self, *args, **kwargs
    ) -> Union[EventProcessorDirective, SnapFrameReport, Any]:
        return self.process_event(*args, **kwargs)
