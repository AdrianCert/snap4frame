from snap4frame.core.decoder import TracebackTypeDecoder
from snap4frame.core.handlers.event import EventHandler
from snap4frame.core.metaclass import Singleton
from snap4frame.core.reports.context import ContextDetailsReporter
from snap4frame.types import SnapFrameReport


class ExceptionHandler(metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        self.event_handler = EventHandler()
        self.context_reporter = ContextDetailsReporter()
        self.traceback_decoder = TracebackTypeDecoder()

    def exception_hook(self, type, value, traceback):
        stacktrace = list(self.traceback_decoder.decode(traceback))
        report = SnapFrameReport(
            stacktrace=stacktrace,
            context=self.context_reporter(),
            value=str(value),
        )

        self.event_handler.report(report)

    def exception(self, exception: Exception):
        self.exception_hook(type(exception), exception, exception.__traceback__)
