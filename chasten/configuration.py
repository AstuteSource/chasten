"""Configuration for Chasten."""

import logging
import logging.config
import logging.handlers
import os
import sys
from enum import Enum
from pathlib import Path
from typing import List

from pydantic import BaseModel
from rich.logging import RichHandler
from rich.traceback import install

from chasten import constants


class Configuration(str, Enum):
    """The predefined values for the configuration file."""

    HOME = Path.home()
    SEPARATOR = os.sep


def configure_tracebacks() -> None:
    """Configure stack tracebacks arising from a crash to use rich."""
    install()


def configure_logging(
    debug_level: str = constants.logging.Default_Logging_Level,
    debug_dest: str = constants.logging.Default_Logging_Destination,
) -> logging.Logger:
    """Configure standard Python logging package."""
    # use the specified logger with the specified destination
    # by dynamically constructing the function to call and then
    # invoking it with the provided debug_dest parameter
    function_name = constants.logger.Function_Prefix + debug_dest
    configure_module = sys.modules[__name__]
    return getattr(configure_module, function_name)(debug_level)


def configure_logging_console(
    debug_level: str = constants.logging.Default_Logging_Level,
) -> logging.Logger:
    """Configure standard Python logging package to use rich."""
    # use the RichHandler to provide formatted
    # debugging output in the console
    logging.basicConfig(
        level=debug_level,
        format=constants.logging.Format,
        datefmt="[%X]",
        handlers=[RichHandler()],
    )
    # create a logger and then return it
    logger = logging.getLogger()
    return logger


def configure_logging_syslog(
    debug_level: str = constants.logging.Default_Logging_Level,
) -> logging.Logger:
    """Configure standard Python logging package to use syslog."""
    # use the SysLogHandler to send output to a localhost on a port
    syslog_handler = logging.handlers.SysLogHandler(
        address=(constants.server.Localhost, constants.server.Port)
    )
    logging.basicConfig(
        level=debug_level,
        format=constants.logging.Format,
        datefmt="[%X]",
        handlers=[syslog_handler],
    )
    # create a logger and then return it
    logger = logging.getLogger()
    return logger


class ChastenConfiguration(BaseModel):
    """Configuration of Chasten."""

    directory: List[Path]
