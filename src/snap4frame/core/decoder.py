from abc import ABC, abstractmethod
from fnmatch import fnmatch
from pathlib import Path
from types import TracebackType
from typing import Any, Iterator, Optional

import snap4frame.config as cfg
import snap4frame.types as t
from snap4frame.core.filters import BuiltinsFilter


class TracebackDecoder(ABC):
    config: t.Parameters

    def __init__(self, config: Optional[t.Parameters] = None):
        if config is not None:
            self.config = t.Parameters(config)

    @abstractmethod
    def decode(self, data: Any) -> Any:
        raise NotImplementedError()


class TracebackFrameDecoder(TracebackDecoder):
    config: t.Parameters = t.Parameters(cfg.FRAME_DECODER)

    def decode(self, data: TracebackType):
        frame_name = data.tb_frame.f_code.co_qualname
        frame_file = Path(data.tb_frame.f_code.co_filename)

        frame_locals = data.tb_frame.f_locals
        frame_locals = BuiltinsFilter.filter_dict(data=frame_locals)
        frame_locals = {
            k: t.VariableCell.from_value(v) for k, v in frame_locals.items()
        }

        lineno = t.LineNumber(data.tb_lineno)  # Convert int to LineNumber object

        return t.CallFrame(
            file=frame_file, name=frame_name, lineno=lineno, vars=frame_locals
        )


class TracebackTypeDecoder(TracebackDecoder):
    config: t.Parameters = t.Parameters(cfg.TRACEBACK_TYPE_DECODER)
    frame_decoder = TracebackFrameDecoder()

    @classmethod
    def decode(cls, data: Optional[TracebackType]):
        raw_stack = []
        while data is not None:
            raw_stack.append(data)
            data = data.tb_next

        iter_stack: Iterator[TracebackType] = reversed(raw_stack)
        for tb_obj in iter_stack:
            frame_name = tb_obj.tb_frame.f_code.co_qualname

            if cls.config.exclude_frames and any(
                fnmatch(frame_name, pth) for pth in cls.config.exclude_frames
            ):
                continue

            yield cls.frame_decoder.decode(tb_obj)
            if frame_name == "<module>":
                # Todo: check if this is the correct condition to break the loop
                break
