import typing

from snap4frame.core import log
from snap4frame.core.metaclass import Singleton
from snap4frame.core.store import Store
from snap4frame.processor import kit
from snap4frame.processor.base import BaseEventProcessor, EventProcessorDirective
from snap4frame.types import SnapFrameReport


class EventHandler(metaclass=Singleton):
    """Handles events and processes them using event processors."""

    handlers_dict: typing.Dict[str, typing.List[BaseEventProcessor]] = Store().handlers

    # TODO: add others processors to the default list
    #  labels: enhancement
    default_processors: typing.List[BaseEventProcessor] = [
        kit.FileSaveProcessor(filepath="snap4frame.json"),
    ]

    def lookup_processors(self, kind: str) -> typing.List[BaseEventProcessor]:
        """Lookup event processors based on the given kind.

        Args:
            kind (str): The kind of event.

        Returns:
            List[BaseEventProcessor]: A list of event processors.
        """

        return self.handlers_dict.get(kind, self.default_processors)

    def emit(
        self,
        event: typing.Union[SnapFrameReport, typing.Any],
        kind: typing.Optional[str] = None,
        *args,
        **kwds,
    ) -> typing.Any:
        """Emits an event and processes it using event processors.

        Args:
            event (Union[SnapFrameReport, Any]): The event to emit.
            kind (Optional[str]): The kind of event. Defaults to None.
            *args: Additional positional arguments.
            **kwds: Additional keyword arguments.
        """
        if not isinstance(event, SnapFrameReport):
            log.warning(f"Unhandled event: {event} ({args=}, {kwds=})")
            return

        event_kind = kind or "default"
        current_event = event
        event_processors = self.lookup_processors(event_kind)

        if callable(event_processors):
            event_processors = event_processors()

        for filter in event_processors:
            result = filter(current_event, *args, **kwds)

            if isinstance(result, EventProcessorDirective):
                if result == EventProcessorDirective.STOP:
                    return
                continue
            current_event = result
        return result
