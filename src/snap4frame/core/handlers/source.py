from pathlib import Path
from typing import Dict, List, Optional, Tuple

from snap4frame.types import LineNumber


class SourceLookupHandler:
    """
    Class responsible for looking up source code based on file paths and line numbers.

    Attributes:
        lines_view (Optional[LineNumber]): The number of lines to include before and after the specified line.
    """

    class Default:
        lines_view: LineNumber = LineNumber(5)

    def __init__(self, lines_view: Optional[LineNumber] = None):
        self.lines_view: int = lines_view or self.Default.lines_view

    def groups4lines(
        self, data: List[Tuple[Path, LineNumber]]
    ) -> Dict[Path, List[LineNumber]]:
        """
        Groups the file paths and line numbers into a dictionary.

        Args:
            data (List[Tuple[Path, LineNumber]]): A list of tuples containing file paths and line numbers.

        Returns:
            Dict[Path, List[LineNumber]]: A dictionary where the keys are file paths and the values are lists of line numbers.
        """
        result = {}
        for file, line in data:
            if file not in result:
                result[file] = []
            result[file].append(line)
        return result

    def process(self, data: List[Tuple[Path, LineNumber]]):
        """
        Processes the file paths and line numbers to generate a mapping of source code.

        Args:
            data (List[Tuple[Path, LineNumber]]): A list of tuples containing file paths and line numbers.

        Returns:
            Dict[Path, Dict[int, str]]: A dictionary where the keys are file paths and the values are dictionaries
            representing the source code mapping, where the keys are line numbers and the values are the corresponding lines of code.
        """
        groups_of_files = self.groups4lines(data)
        result = {}
        for file, lines in groups_of_files.items():
            source_map = dict(enumerate(file.read_text().splitlines(), start=1))
            source_max = max(source_map)
            source_scope = {}
            for line in lines:
                for i in range(
                    max(1, line - self.lines_view),
                    min(source_max, line + self.lines_view) + 1,
                ):
                    source_scope[i] = source_map[i]
            result[file] = source_scope
        return result
