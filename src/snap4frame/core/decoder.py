from abc import ABC, abstractmethod
from fnmatch import fnmatch
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, Iterator, Optional, Union

from snap4frame import config, types
from snap4frame.core.filters import BuiltinsFilter


class TracebackDecoder(ABC):
    config: types.Parameters

    def __init__(
        self, config: Optional[Union[types.Parameters, Dict[str, Any]]] = None
    ):
        self.config = types.Parameters(config or {})

    @abstractmethod
    def decode(self, data: Any) -> Any:
        raise NotImplementedError()


class TracebackFrameDecoder(TracebackDecoder):
    config: types.Parameters = types.Parameters(config.FRAME_DECODER)

    def decode(self, data: TracebackType):
        frame_name = data.tb_frame.f_code.co_qualname
        frame_file = Path(data.tb_frame.f_code.co_filename)

        frame_locals = data.tb_frame.f_locals
        frame_locals = BuiltinsFilter.filter_dict(data=frame_locals)
        frame_locals = {
            k: types.VariableCell.from_value(v) for k, v in frame_locals.items()
        }

        lineno = types.LineNumber(data.tb_lineno)  # Convert int to LineNumber object

        return types.CallFrame(
            file=frame_file, name=frame_name, lineno=lineno, vars=frame_locals
        )


class TracebackTypeDecoder(TracebackDecoder):
    config: types.Parameters
    frame_decoder = TracebackFrameDecoder()

    def decode(self, data: Optional[TracebackType]):
        raw_stack = []
        while data is not None:
            raw_stack.append(data)
            data = data.tb_next

        iter_stack: Iterator[TracebackType] = reversed(raw_stack)
        for tb_obj in iter_stack:
            frame_name = tb_obj.tb_frame.f_code.co_qualname

            if self.config.exclude_frames and any(
                fnmatch(frame_name, pth) for pth in self.config.exclude_frames
            ):
                continue

            yield self.frame_decoder.decode(tb_obj)
            if frame_name == "<module>":
                # TODO check if this is the correct condition to break the loop
                break
