"""Chasten checks the AST of a Python program."""

from enum import Enum
from pathlib import Path
from typing import List

import typer
from platformdirs import user_config_dir
from pyastgrep import search as pyastgrepsearch  # type: ignore
from rich.console import Console
from trogon import Trogon  # type: ignore
from typer.main import get_group

from chasten import constants, debug, filesystem, output, server

# create a Typer object to support the command-line interface
cli = typer.Typer()


class ConfigureTask(str, Enum):
    """Define the different task possibilities."""

    CREATE = "create"
    DISPLAY = "display"


@cli.command()
def interact(ctx: typer.Context) -> None:
    """Interactively configure and run."""
    Trogon(get_group(cli), click_context=ctx).run()


@cli.command()
def configure(
    task: ConfigureTask = typer.Argument(ConfigureTask.DISPLAY.value),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Create configuration directory and files even if they exist",
    ),
    verbose: bool = typer.Option(False),
    debug_level: debug.DebugLevel = typer.Option(debug.DebugLevel.ERROR.value),
    debug_destination: debug.DebugDestination = typer.Option(
        debug.DebugDestination.CONSOLE.value, "--debug-dest"
    ),
) -> None:
    """Create a configuration."""
    # setup the console and the logger through the output module
    output.setup(debug_level, debug_destination)
    output.logger.debug(f"Task? {task}")
    output.logger.debug(f"Display verbose output? {verbose}")
    output.logger.debug(f"Debug level? {debug_level.value}")
    output.logger.debug(f"Debug destination? {debug_destination.value}")
    # display the header
    output.print_header()
    # display details about configuration as
    # long as verbose output was requested
    output.print_diagnostics(
        verbose,
        task=task.value,
        debug_level=debug_level.value,
        debug_destination=debug_destination.value,
    )
    # display the configuration directory and its contents
    if task == ConfigureTask.DISPLAY:
        output.console.print(
            ":sparkles: Configuration directory:" + constants.markers.Newline
        )
        chasten_user_config_dir_str = user_config_dir(
            appname=constants.chasten.Application_Name,
            appauthor=constants.chasten.Application_Author,
        )
        chasten_user_config_dir_path = Path(chasten_user_config_dir_str)
        rich_path_tree = filesystem.create_directory_tree(chasten_user_config_dir_path)
        output.console.print(rich_path_tree)
        output.console.print()

    # # create the configuration directory
    # if create:
    #     chasten_user_config_dir_str = user_config_dir(
    #         appname=constants.chasten.Application_Name,
    #         appauthor=constants.chasten.Application_Author,
    #     )
    #     chasten_user_config_dir_path = Path(chasten_user_config_dir_str)
    #     chasten_user_config_dir_path.mkdir(parents=True)


@cli.command()
def search(
    directory: List[Path] = typer.Option(
        filesystem.get_default_directory_list(),
        "--directory",
        "-d",
        help="One or more directories with Python code",
    ),
) -> None:
    """Check the AST of Python source code."""
    # create a console for rich text output
    console = Console()
    # add extra space after the command to run the program
    console.print()
    # collect all of the directories that are invalid
    invalid_directories = []
    for current_directory in directory:
        if not filesystem.confirm_valid_directory(current_directory):
            invalid_directories.append(current_directory)
    # create the list of valid directories by removing the invalid ones
    valid_directories = list(set(directory) - set(invalid_directories))
    console.print(valid_directories)
    # search for the XML contents of an AST that match the provided
    # XPATH query using the search_python_file in search module of pyastgrep
    match_generator = pyastgrepsearch.search_python_files(
        paths=valid_directories,
        expression='.//FunctionDef[@name="classify"]/body//If[ancestor::If and not(parent::orelse)]',
    )
    # display debugging information about the contents of the match generator
    console.print(match_generator)
    for search_output in match_generator:
        console.print(search_output)


@cli.command()
def log() -> None:
    """Start the logging server."""
    # display the header
    output.print_header()
    # display details about the server
    output.print_server()
    # run the server; note that this
    # syslog server receives debugging
    # information from chasten.
    # It must be started in a separate process
    # before running any sub-command
    # of the chasten tool
    server.start_syslog_server()
