"""Perform logging and/or console output."""

import logging
from typing import Any

from rich.console import Console

from chasten import configuration, constants, debug

# declare a default logger
logger: logging.Logger = logging.getLogger()

# create a default console
console = Console()


def setup(
    debug_level: debug.DebugLevel, debug_destination: debug.DebugDestination
) -> None:
    """Perform the setup steps and return a Console for terminal-based display."""
    global logger
    # configure the use of rich for improved terminal output:
    # --> rich-based tracebacks to enable better debugging on program crash
    configuration.configure_tracebacks()
    # --> logging to keep track of key events during program execution;
    # pass in the actual values as strings instead of using class enums
    logger, _ = configuration.configure_logging(
        debug_level.value, debug_destination.value
    )


def print_diagnostics(verbose: bool, **configurations: Any) -> None:
    """Display all variables input to the function."""
    global console  # noqa: disable=PLW0603
    # display diagnostic information for each configuration keyword argument
    if verbose:
        console.print(":sparkles: Configured with these parameters:")
        # iterate through each of the configuration keyword arguments
        for configuration_current in configurations:
            # print the name and the value of the keyword argument
            console.print(
                f"{constants.markers.Indent}{configuration_current} = {configurations[configuration_current]}"
            )
        console.print()


def opt_print_log(verbose: bool, **contents: Any) -> None:
    """Produce logging information and only print when not verbose."""
    global console  # noqa: disable=PLW0603
    # iterate through each of the configuration keyword arguments
    for current in contents:
        # print the name and the value of the keyword argument
        # to the console if verbose mode is enabled
        if verbose:
            console.print(contents[current])
        # always log the information to the configured logger
        logger.debug(contents[current])


def print_header() -> None:
    """Display tool details in the header."""
    global console
    console.print()
    console.print(
        constants.chasten.Emoji + constants.markers.Space + constants.chasten.Tagline
    )
    console.print(constants.chasten.Website)
    # console.print()


def print_server() -> None:
    """Display server details in the header."""
    global console  # noqa: disable=PLW0603
    console.print(constants.output.Syslog)
    console.print()


def print_test_start() -> None:
    """Display details about the test run."""
    global console  # noqa: disable=PLW0603
    console.print(constants.output.Test_Start)
    console.print()


def print_test_finish() -> None:
    """Display details about the test run."""
    global console  # noqa: disable=PLW0603
    console.print()
    console.print(":sparkles: Finish running test suite for the specified program")
    console.print()


def print_footer() -> None:
    """Display concluding details in the footer."""
    global console  # noqa: disable=PLW0603
    console.print()
