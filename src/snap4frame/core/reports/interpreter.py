import platform
import sys
from typing import Any

from snap4frame.types import InterpreterDetails


class InterpreterReporter:
    """
    A class that reports details about the Python interpreter.

    This class provides a callable object that returns an instance of the
    `InterpreterDetails` class, which contains information about the Python
    interpreter being used.

    Attributes:
        None

    Methods:
        __call__: Returns an instance of `InterpreterDetails` with interpreter details.
    """

    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> InterpreterDetails:
        """
        Returns an instance of `InterpreterDetails` with details about the Python interpreter.

        Args:
            *args: Variable length argument list.
            **kwds: Arbitrary keyword arguments.

        Returns:
            An instance of `InterpreterDetails` with the following attributes:
                - name: The name of the Python implementation.
                - version: The version of Python.
                - path: The path to the Python executable.
                - runtime: The runtime information of the Python interpreter.

        """
        return InterpreterDetails(
            name=platform.python_implementation(),
            version=sys.version,
            path=sys.executable,
            runtime="{implementation} {version}".format(
                implementation=platform.python_implementation(),
                version=platform.python_version(),
            ),
        )
