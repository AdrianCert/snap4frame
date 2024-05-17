import typing

from snap4frame.core.decoder import TracebackTypeDecoder
from snap4frame.core.handlers.event import EventHandler
from snap4frame.core.metaclass import Singleton
from snap4frame.core.reports.context import ContextDetailsReporter
from snap4frame.types import SnapFrameReport


class ExceptionHandler(metaclass=Singleton):
    """
    Handles exceptions and emits reports.

    This class provides methods to handle exceptions and emit reports containing
    stack traces, context details, and exception values.
    """

    def __init__(self, *args, **kwargs):
        self.event_handler = EventHandler()
        self.context_reporter = ContextDetailsReporter()
        self.traceback_decoder = TracebackTypeDecoder()

    def handle_exception(
        self,
        exception: Exception,
        kind: typing.Optional[str] = None,
    ) -> typing.Any:
        """
        Handles an exception and emits a report.

        Args:
            exception (Exception): The exception object to be handled.
            kind (str, optional): The kind of the exception.

        Returns:
            None
        """
        traceback = exception.__traceback__
        stacktrace = list(self.traceback_decoder.decode(traceback))
        report = SnapFrameReport(
            stacktrace=stacktrace,
            context=self.context_reporter(),
            value=str(exception),
        )

        return self.event_handler.emit(report, kind=kind)

    def exception_hook(self, type, value, traceback):
        """
        Handles an exception and emits a report.

        Args:
            type (type): The type of the exception.
            value (Exception): The exception object.
            traceback (traceback): The traceback object.
        """
        return self.handle_exception(value)

    def exception(self, exception: Exception, kind=None):
        """
        Handles an exception and emits a report.

        Args:
            exception (Exception): The exception object.
            kind (str, optional): The kind of exception. Defaults to None.
        """
        return self.handle_exception(exception, kind=kind)
