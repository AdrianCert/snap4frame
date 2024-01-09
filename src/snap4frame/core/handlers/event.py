import json
import sys
from dataclasses import asdict
from typing import Any, Union

from snap4frame.core import log
from snap4frame.types import SnapFrameReport


class EventHandler:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def process_snap_frame_report(self, event: SnapFrameReport, *args: Any, **kwds: Any) -> bool:
        pass
        x = event.as_dict()
        json.dump(x, sys.stdout, indent=2)
        return True

    def report(self, event : Union[SnapFrameReport, Any], *args: Any, **kwds: Any) -> None:

        if isinstance(event, SnapFrameReport):
            handled = self.process_snap_frame_report(event, *args, **kwds)
            if handled:
                return

        # SourceLookupHandler().process(event)

        log.warning(f"Unhandled event: {event} ({args=}, {kwds=})")
        return

        # todo: this is a temporary solution
        # todo: implement a proper event handler
        # todo: call chain of handlers
        
        pass
