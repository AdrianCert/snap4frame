import sys
import typing

from snap4frame.core.handlers.exception import ExceptionHandler
from snap4frame.types import ExceptionHookCallback


class Snap4FrameExceptionHook:
    """
    A class that installs and uninstalls an exception hook for Snap4Frame.

    The exception hook is responsible for handling uncaught exceptions and providing custom exception handling logic.

    Attributes:
        previous_hook (Optional[Callable[[Type, Exception, TracebackType], None]]): The previous exception hook, if any.
        handler (ExceptionHandler): An instance of the ExceptionHandler class used for exception handling.
    """

    previous_hook: typing.Optional[ExceptionHookCallback] = None
    handler: ExceptionHandler = ExceptionHandler()

    @classmethod
    def install(cls, **kwargs) -> None:
        """
        Installs the exception hook.

        Returns:
            None
        """
        if cls.previous_hook is not None:
            return
        cls.previous_hook = sys.excepthook
        sys.excepthook = cls.handler.exception_hook

    @classmethod
    def uninstall(cls) -> None:
        """
        Uninstalls the exception hook.

        Returns:
            None
        """
        if cls.previous_hook is None:
            return
        sys.excepthook = cls.previous_hook
        cls.previous_hook = None
