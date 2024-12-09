"""
Logging utilities for Amati.
"""

from contextlib import contextmanager
from dataclasses import dataclass
from typing import ClassVar, Generator, List, Optional, Type

from pydantic import AnyUrl

LogType = Exception | Warning

@dataclass(frozen=True)
class Log:
    message: str
    type: Type[LogType]
    reference: Optional[AnyUrl] = None


class LogMixin(object):
    """
    A mixin class that provides logging functionality.

    This class maintains a list of Log messages that are added.
    It is NOT thread-safe. State is maintained at a global level.
    """
    logs: ClassVar[List[Log]] = []

    @classmethod
    def log(cls, message: Log) -> None:
        """Add a new message to the logs list.

        Args:
            message: A Log object containing the message to be logged.

        Returns:
            The current list of logs after adding the new message.
        """
        cls.logs.append(message)

    @classmethod
    @contextmanager
    def context(cls) -> Generator[List[Log], None, None]:
        """Create a context manager for handling logs.

        Yields:
            The current list of logs.

        Notes:
            Automatically clears the logs when exiting the context.
        """
        try:
            yield cls.logs
        finally:
            cls.logs.clear()
