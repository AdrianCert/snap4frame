from snap4frame.core.reports.additional import AdditionalContextDetailsReporter
from snap4frame.core.reports.interpreter import InterpreterReporter
from snap4frame.core.reports.machine import MachineReporter
from snap4frame.core.reports.packages import PackagesReporter
from snap4frame.types import ContextDetails


class ContextDetailsReporter:
    """
    A class that generates context details by calling various reporters.

    The context details include information about the interpreter, additional context details,
    machine details, and packages.

    Usage:
    reporter = ContextDetailsReporter()
    context_details = reporter()

    Returns:
    ContextDetails: An object containing the generated context details.
    """

    def __init__(self) -> None:
        self.machine_reporter = MachineReporter()
        self.interpreter_reporter = InterpreterReporter()
        self.additional_reporter = AdditionalContextDetailsReporter()
        self.package_reporter = PackagesReporter()

    def __call__(self, *args, **kwargs) -> ContextDetails:
        return ContextDetails(
            interpreter=self.interpreter_reporter(),
            additional=self.additional_reporter(),
            machine=self.machine_reporter(),
            packages=self.package_reporter(),
        )
