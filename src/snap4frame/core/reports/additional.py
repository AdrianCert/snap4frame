import sys
from typing import Any

from snap4frame.types import AdditionalContextDetails


class AdditionalContextDetailsReporter:
    """
    This class represents a reporter for additional context details.
    """

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        Call method for the AdditionalContextDetails class.

        Args:
            *args: Variable length argument list.
            **kwds: Arbitrary keyword arguments.

        Returns:
            Any: The result of calling AdditionalContextDetails with the given arguments.
        """
        return AdditionalContextDetails(argv=sys.argv)
