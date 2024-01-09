from typing import Any, Dict

import importlib_metadata


class PackagesReporter:
    """
    A class that generates a report of installed package distributions.
    """

    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Dict[str, str]:
        """
        Generates a report of installed package distributions.

        Returns:
            A dictionary mapping package names to their versions.
        """
        return {i.name: i.version for i in importlib_metadata.distributions()}
