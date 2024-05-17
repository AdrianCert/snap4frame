from typing import Any, Dict, List, Optional, TextIO

from snap4frame.processor.base import BaseEventProcessor

# TODO: Add versioning to the package
#  this value should be single source of truth for the package version
#  __version__ = "0.0.1"
VERSION = "0.0.1"


class ClientConstructor:
    def __init__(  # noqa: PLR0913
        self,
        event_processors: Optional[List[BaseEventProcessor]] = None,
        ep_converter: Optional[Dict[str, Any]] = None,
        ep_stream: Optional[Dict[str, Any]] = None,
        ep_file: Optional[Dict[str, Any]] = None,
        ep_webhook: Optional[Dict[str, Any]] = None,
        ep_converter_order: Optional[int] = None,
        ep_stream_order: Optional[int] = None,
        ep_file_order: Optional[int] = None,
        ep_webhook_order: Optional[int] = None,
        ep_stream_indent: Optional[int] = 2,
        ep_stream_fd: Optional[TextIO] = None,
        ep_file_indent: Optional[int] = 2,
        ep_file_exists_ok: Optional[bool] = True,
        ep_file_create_path: Optional[bool] = True,
        ep_webhook_method: Optional[str] = "POST",
        ep_webhook_url: Optional[str] = None,
    ):
        pass
