import typing
from collections import UserDict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from types import TracebackType

from snap4frame.core.types import TypedBase


def path2str(
    data: Path,
    cwd: typing.Optional[str] = None,
    replace: typing.Optional[str] = "./",
) -> str:
    cwd = cwd or Path.cwd().as_posix().lower()
    cwd_len = len(cwd)
    result: str = data.resolve().as_posix()
    if replace is None:
        return result
    if result[:cwd_len].lower() != cwd:
        return result
    return replace + result[cwd_len:]


LineNumber = int


class Parameters(UserDict):
    def __getattr__(self, name) -> typing.Any:
        return self.get(name, None)


@dataclass
class VariableCell(TypedBase):
    value: str
    type: str

    @staticmethod
    def from_value(value: typing.Any):
        return VariableCell(repr(value), type(value).__name__)

    def as_dict(self):
        return f"!{self.type} {self.value}"


@dataclass
class CallFrame(TypedBase):
    """
    Represents a call frame in a program execution.

    Attributes:
        file (Path): The path to the source file where the call frame is located.
        name (str): The name of the call frame.
        lineno (LineNumber): The line number in the source file where the call frame is located.
        vars (Dict[str, VariableCell]): A dictionary of variable cells associated with the call frame.
    """

    class SerializeMeta:
        @staticmethod
        def filter(key: str):
            return key not in ["dt"]

        @staticmethod
        def file(_data: "CallFrame", value: Path):
            return path2str(value)

    file: Path
    name: str
    lineno: LineNumber
    vars: typing.Dict[str, VariableCell] = field(default_factory=dict)
    extra: typing.Dict[str, typing.Any] = field(default_factory=dict)


@dataclass
class InterpreterDetails(TypedBase):
    """
    Represents details about an interpreter.

    Attributes:
        name (str): The name of the interpreter.
        version (str): The version of the interpreter.
        path (str): The path to the interpreter.
        runtime (str): The runtime of the interpreter.
    """

    name: str
    version: str
    path: str
    runtime: str


@dataclass
class MachineDetails(TypedBase):
    name: str
    platform: str


@dataclass
class AdditionalContextDetails(TypedBase):
    argv: typing.List[str]


@dataclass
class ContextDetails(TypedBase):
    interpreter: InterpreterDetails
    additional: AdditionalContextDetails
    machine: MachineDetails
    packages: typing.Dict[str, str]
    extra: typing.Dict[str, typing.Any] = field(default_factory=dict)


@dataclass
class SnapFrameReport(TypedBase):
    stacktrace: typing.List[CallFrame]
    value: str
    context: ContextDetails
    dt: datetime = field(default_factory=datetime.utcnow)

    class SerializeMeta:
        @staticmethod
        def filter(key: str):
            return key not in ["dt"]

        @staticmethod
        def datetime(data: "SnapFrameReport", *args):
            return data.dt.isoformat()


class EventProcessorDirective(Enum):
    CONTINUE = 0
    STOP = 1


ProcessorMetaField = typing.Union[int, float, str, bool]
SnapFrameEvent = typing.Union[
    SnapFrameReport,
    typing.Dict[str, typing.Dict[typing.Any, typing.Any]],
    typing.Any,
]
SnapFrameResult = typing.Union[
    EventProcessorDirective,
    SnapFrameReport,
    typing.Dict[str, typing.Dict[typing.Any, typing.Any]],
    typing.Any,
]

ExceptionHookCallback = typing.Callable[
    [typing.Type[BaseException], BaseException, typing.Optional[TracebackType]],
    typing.Any,
]
