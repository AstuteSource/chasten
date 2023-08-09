"""Perform logging and/or console output."""

import logging
from copy import deepcopy
from typing import Any

from pyastgrep import search as pyastgrepsearch  # type: ignore
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from chasten import (
    checks,
    configuration,
    constants,
    debug,
    results,
)

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
    global console  # noqa: disable=PLW0603
    console.print()
    console.print(
        constants.chasten.Emoji + constants.markers.Space + constants.chasten.Tagline
    )
    console.print(constants.chasten.Website)


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


def print_analysis_details(chasten: results.Chasten, verbose: bool = False) -> None:
    """Print all of the verbose debugging details for the results of an analysis."""
    # 1) Note: see the BaseModel definitions in results.py for more details
    # about the objects and their relationships
    # 2) Note: the _match object that is inside of a Match BaseModel subclass
    # is an instance of pyastgrepsearch.Match and contains the entire details
    # about the specific match, including the entire source code. This object
    # is not saved to the JSON file by default, as evidenced by the underscore
    if not verbose:
        return None
    opt_print_log(verbose, label="\n:tada: Results from the analysis!")
    # iterate through the the list of sources inside of the resulting analysis
    for current_source in chasten.sources:
        # extract the current check from this source
        current_check: results.Check = current_source.check  # type: ignore
        current_xpath_pattern = current_check.pattern
        console.print("\n:tada: Check:")
        xpath_syntax = Syntax(
            current_xpath_pattern,
            constants.markers.Xml,
            theme=constants.chasten.Theme_Colors,
        )
        # extract the minimum and maximum values for the checks, if they exist
        # note that this function will return None for a min or a max if
        # that attribute does not exist inside of the current_check; importantly,
        # having a count or a min or a max is all optional in a checks file
        min_count = current_check.min
        max_count = current_check.max
        min_label = checks.create_attribute_label(min_count, constants.checks.Check_Min)
        max_label = checks.create_attribute_label(max_count, constants.checks.Check_Max)
        # extract details about the check to display in the header
        # of the syntax box for this specific check
        check_id = current_check.id
        check_id_label = checks.create_attribute_label(check_id, constants.checks.Check_Id)  # type: ignore
        check_name = current_check.name
        check_name_label = checks.create_attribute_label(check_name, constants.checks.Check_Name)  # type: ignore
        # create the combined attribute label that displays all details for the check
        combined_attribute_label = checks.join_attribute_labels(
            [check_id_label, check_name_label, min_label, max_label]
        )
        # display the check with additional details about its configuration
        console.print(
            Panel(
                xpath_syntax,
                expand=False,
                title=f"{combined_attribute_label}",
            )
        )
        if current_check.matches:  # type: ignore
            for current_match in current_check._matches:  # type: ignore
                if isinstance(current_match, pyastgrepsearch.Match):  # type: ignore
                    # display a label for matching output information
                    opt_print_log(verbose, blank=constants.markers.Empty_String)
                    opt_print_log(verbose, label=":sparkles: Matching source code:")
                    # extract the direct line number for this match
                    position_end = current_match.position.lineno
                    # extract the column offset for this match
                    column_offset = current_match.position.col_offset
                    # get a pre-defined number of the lines both
                    # before and after the line that is the closest match;
                    # note that the use of "*" is an indicator of the
                    # specific line that is the focus of the search
                    all_lines = current_match.file_lines
                    # create a deepcopy of the listing of lines so that
                    # the annotated version of the lines for this specific
                    # match does not appear in annotated version of other matches
                    all_lines_for_marking = deepcopy(all_lines)
                    lines = all_lines_for_marking[
                        max(0, position_end - constants.markers.Code_Context) : position_end
                        + constants.markers.Code_Context
                    ]
                    # create a rich panel to display the results:
                    # key features:
                    # --> descriptive label
                    # --> syntax highlighting
                    # --> line numbers
                    # --> highlight for the matching position
                    # --> suitable theme (could be customized)
                    code_syntax = Syntax(
                        "\n".join(str(line) for line in lines),
                        constants.chasten.Programming_Language,
                        theme=constants.chasten.Theme_Colors,
                        background_color=constants.chasten.Theme_Background,
                        line_numbers=True,
                        start_line=(
                            max(1, position_end - constants.markers.Code_Context + 1)
                        ),
                        highlight_lines={position_end},
                    )
                    # display the results in a rich panel
                    opt_print_log(
                        verbose,
                        panel=Panel(
                            code_syntax,
                            expand=False,
                            title=f"{current_match.path}:{position_end}:{column_offset}",
                        ),
                    )
