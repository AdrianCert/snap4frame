import typing

from snap4frame.core import log
from snap4frame.core.metaclass import Singleton
from snap4frame.processor.base import BaseEventProcessor, EventProcessorDirective
from snap4frame.types import SnapFrameReport


class EventHandler(metaclass=Singleton):
    """Handles events and processes them using event processors."""

    def lookup_processors(self, kind: str) -> typing.List[BaseEventProcessor]:
        """Lookup event processors based on the given kind.

        Args:
            kind (str): The kind of event.

        Returns:
            List[BaseEventProcessor]: A list of event processors.
        """

        # TODO: Implement a proper way to lookup event processors based on configuration.
        from snap4frame.processor import kit

        return [
            kit.FileSaveProcessor(filepath="snap4frame.json"),
        ]

    def emit(
        self,
        event: typing.Union[SnapFrameReport, typing.Any],
        kind: typing.Optional[str] = None,
        *args,
        **kwds,
    ) -> None:
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
        for filter in event_processors:
            result = filter(current_event, *args, **kwds)

            if isinstance(result, EventProcessorDirective):
                if result == EventProcessorDirective.STOP:
                    return
                continue
            current_event = result
