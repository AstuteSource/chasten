"""Perform logging and/or console output."""

import logging
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List

from pyastgrep import search as pyastgrepsearch  # type: ignore
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from chasten import checks, configuration, constants, debug, results

# declare a default logger
logger: logging.Logger = logging.getLogger()

# create a default console
console = Console()

# define a small bullet for display
small_bullet_unicode = "\u2022"


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
    console.print(":sparkles: Finished running test suite for the specified program")
    console.print()


def print_footer() -> None:
    """Display concluding details in the footer."""
    global console  # noqa: disable=PLW0603
    console.print()


def group_files_by_directory(file_paths: List[Path]) -> Dict[Path, List[str]]:
    """Organize the files in a list according to their base directory."""
    # create an empty dictionary
    grouped_files: Dict[Path, List[str]] = {}
    # iterate through each of the full paths
    # and extract the containing directory
    # from the name of the file that is contained
    for file_path in file_paths:
        # extract the parent (i.e., containing)
        # directory for the current file path
        directory = file_path.parent
        # extract the name of the file, excluding
        # the containing directory
        file_name = file_path.name
        # update the dictionary that uses:
        # --> a Path key for the containing directory
        # --> a list of strings for the contained files
        if directory not in grouped_files:
            grouped_files[directory] = []
        grouped_files[directory].append(file_name)
    # return the dictionary of files organized by directory
    return grouped_files


def shorten_file_name(file_name: str, max_length: int) -> str:
    """Elide part of a file name if it is longer than the maximum length."""
    # remove content from the start of the filename if it is too long
    if len(file_name) > max_length:
        return "... " + file_name[-(max_length - 3) :]
    return file_name


def print_list_contents(container: List[Path]) -> None:
    """Display the contents of the list in an easy-to-read fashion."""
    global console  # noqa: disable=PLW0603
    # group all of the files by the directory that contains them;
    # note that this is important because the contain can contain
    # paths that specify files in different directories
    grouped_files = group_files_by_directory(container)
    # iterate through each of the directories and
    # --> display the name of the directory
    # --> display the name of each file stored in this directory
    for directory, files in grouped_files.items():
        console.print(f"{small_bullet_unicode} Directory: {directory}")
        for file_name in files:
            console.print(
                f"  {small_bullet_unicode} File: '{shorten_file_name(file_name, 120)}'"
            )


def print_analysis_details(chasten: results.Chasten, verbose: bool = False) -> None:
    """Print all of the verbose debugging details for the results of an analysis."""
    global console  # noqa: disable=PLW0603
    # 1) Note: see the BaseModel definitions in results.py for more details
    # about the objects and their relationships
    # 2) Note: the _match object that is inside of a Match BaseModel subclass
    # is an instance of pyastgrepsearch.Match and contains the entire details
    # about the specific match, including the entire source code. This object
    # is not saved to the JSON file by default, as evidenced by the underscore
    if not verbose:
        return None
    opt_print_log(verbose, label="\n:tada: Results from the analysis:")
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
        if len(current_check._matches) > 0:  # type: ignore
            # display the details about the number of matches and the name of the source's file
            opt_print_log(verbose, blank=constants.markers.Empty_String)
            opt_print_log(
                verbose,
                label=f":tada: Found a total of {len(current_check._matches)} matches for '{check_name}' in {current_source.filename}",
            )
            # iterate through each of the matches and display all of their details
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
                        max(
                            0, position_end - constants.markers.Code_Context
                        ) : position_end
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
