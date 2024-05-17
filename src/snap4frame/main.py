import typing

from snap4frame.core.handlers.exception import ExceptionHandler
from snap4frame.core.hook import Snap4FrameExceptionHook
from snap4frame.core.store import Store

_except_handler = ExceptionHandler()

__all__ = ["init", "setup_handler", "emit"]


def init(**kwargs):
    # TODO: implement the kwargs interpretation logic
    Snap4FrameExceptionHook.install()


def setup_handler(kind, processor):
    Store().handlers[kind] = processor


def emit(exception: typing.Optional[Exception] = None, kind=None):
    if exception is None:
        import sys

        exception = Exception("snap4frame.emit")
        exception.__traceback__ = sys.exc_info()[2]
    return _except_handler.exception(exception, kind=kind)
