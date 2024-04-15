import functools
import sys
from logging import Logger
from pathlib import Path
from typing import Optional

from snap4frame.processor.base import (
    BaseEventProcessor,
    EventProcessorDirective,
    ProcessorMetaField,
)
from snap4frame.types import Parameters, SnapFrameReport

try:
    import msgspec

    USE_MSGSPEC = True
except ImportError:
    USE_MSGSPEC = False
    import json


def json_encode(data, indent: Optional[int] = None) -> str:
    if USE_MSGSPEC:
        if indent:
            return msgspec.json.format(
                msgspec.json.encode(data),
                indent=indent,
            ).decode("utf-8")
        return msgspec.json.encode(data).decode("utf-8")
    return json.dumps(data, indent=indent)


class ConvertToDictProcessor(BaseEventProcessor):
    short_name: ProcessorMetaField = "converter"

    def process_event(self, event: SnapFrameReport) -> dict:
        if not isinstance(event, SnapFrameReport):
            self.logger.warning(
                "ConvertToDictFilter received unexpected event: %s", event
            )
            raise ValueError("Unexpected event type")
        return event.as_dict()


class StreamProcessor(ConvertToDictProcessor):
    short_name: ProcessorMetaField = "stream"

    def process_event(self, event: SnapFrameReport) -> EventProcessorDirective:
        _result = super().process_event(event)
        print(
            json_encode(
                _result,
                indent=self.config.get("indent", 2),
            ),
            file=self.config.fd or sys.stdout,
        )
        return EventProcessorDirective.CONTINUE


class FileSaveProcessor(StreamProcessor):
    config: Parameters
    logger: Logger
    short_name: ProcessorMetaField = "file"

    def process_event(self, event: SnapFrameReport) -> EventProcessorDirective:
        filepath = Path(self.config.filepath)

        if not self.config.exists_ok and filepath.exists():
            raise FileExistsError(filepath)

        if self.config.create_path:
            filepath.parent.mkdir(parents=True, exist_ok=True)

        with filepath.open("w") as fd:
            self.config["fd"] = fd
            super().process_event(event)

        return EventProcessorDirective.CONTINUE


class WebHookProcessor(ConvertToDictProcessor):
    config: Parameters
    short_name: ProcessorMetaField = "webhook"

    def setup(self):
        request_method = self.config.get("method", "POST")
        request_url = self.config.get("url", "")
        if not request_url:
            raise ValueError("url is required")
        try:
            # requests is an optional dependency
            # so we import it here to avoid ImportError
            import requests

            self.request_method = functools.partial(
                requests.request,
                method=request_method,
                url=request_url,
            )
        except ImportError:
            raise ImportError("requests library is required to run WebHookFilter")

    def make_request(self, data: dict) -> None:
        result = self.request_method(json=data)
        self.logger.info("WebHookFilter response: %s", result.status_code)

    def process_event(self, event: SnapFrameReport) -> EventProcessorDirective:
        self.make_request(super().process_event(event))
        return EventProcessorDirective.CONTINUE
