"""Support and configure debugging."""

from enum import Enum


class DebugLevel(str, Enum):
    """The predefined levels for debugging."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class DebugDestination(str, Enum):
    """The destination for debugging."""

    CONSOLE = "CONSOLE"
    SYSLOG = "SYSLOG"
