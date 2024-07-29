import platform
from typing import Any

from snap4frame.types import MachineDetails


class MachineReporter:
    """
    A class that reports machine details.

    This class provides a callable object that returns a dictionary containing
    information about the machine, such as its name and platform.

    Example usage:
        reporter = MachineReporter()
        details = reporter()
        print(details)  # {'name': 'my-machine', 'platform': 'Windows-10-10.0.19041-SP0'}
    """

    def __call__(self, *args: Any, **kwds: Any) -> MachineDetails:
        """
        Returns a dictionary containing machine details.

        Args:
            *args: Variable length argument list.
            **kwds: Arbitrary keyword arguments.

        Returns:
            A dictionary with machine details, including the name and platform.

        """
        return MachineDetails(name=platform.node(), platform=platform.platform())
