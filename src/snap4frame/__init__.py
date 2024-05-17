from typing import TYPE_CHECKING

from snap4frame.main import emit, setup_handler
from snap4frame.processor.base import BaseEventProcessor, EventProcessorDirective

__all__ = ["emit", "setup_handler", "init"]

if TYPE_CHECKING:
    from snap4frame.const import ClientConstructor

    class init(ClientConstructor):  # noqa: N801
        """
        A class representing the library constructor.

        Args:
            event_processors (Optional[List[BaseEventProcessor]]): A list of event processors.
                Defaults to None.
            ep_converter (Optional[Dict[str, Any]]): Options for the converter event processor.
                Defaults to None.
            ep_stream (Optional[Dict[str, Any]]): Options for the stream event processor.
                Defaults to None.
            ep_file (Optional[Dict[str, Any]]): Options for the file event processor.
                Defaults to None.
            ep_webhook (Optional[Dict[str, Any]]): Options for the webhook event processor.
                Defaults to None.
            ep_converter_order (Optional[int]): The order of the converter event processor.
                Defaults to None.
            ep_stream_order (Optional[int]): The order of the stream event processor.
                Defaults to None.
            ep_file_order (Optional[int]): The order of the file event processor.
                Defaults to None.
            ep_webhook_order (Optional[int]): The order of the webhook event processor.
                Defaults to None.
            ep_stream_indent (Optional[int]): The indentation level for the stream event processor.
                Defaults to 2.
            ep_stream_fd (Optional[TextIO]): The file descriptor for the stream event processor.
                Defaults to None.
            ep_file_indent (Optional[int]): The indentation level for the file event processor.
                Defaults to 2.
            ep_file_exists_ok (Optional[bool]): Whether to allow the file event processor to create
                the file if it doesn't exist. Defaults to True.
            ep_file_create_path (Optional[bool]): Whether to create the file path if it doesn't exist
                for the file event processor. Defaults to True.
            ep_webhook_method (Optional[str]): The HTTP method for the webhook event processor.
                Defaults to "POST".
            ep_webhook_url (Optional[str]): The URL for the webhook event processor.
                Defaults to None.
        """

        pass


else:
    from snap4frame.main import init
