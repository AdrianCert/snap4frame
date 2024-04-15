from typing import Any, Dict


class BuiltinsFilter:
    """
    A class that filters out dictionary items containing built-in variable names.

    Attributes:
        variables (set): A set of built-in variable names.
    """

    variables = {
        "__builtins__",
        *__builtins__,
        "__file__",
        "__cached__",
        "__annotations__",
    }

    @classmethod
    def filter_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filters a dictionary by removing items with keys that match built-in variable names.

        Args:
            data (dict): The dictionary to be filtered.

        Returns:
            dict: The filtered dictionary.
        """
        return {k: v for k, v in data.items() if k not in cls.variables}
