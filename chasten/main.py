"""Chasten checks the AST of a Python program."""

from enum import Enum
from pathlib import Path
from typing import List

import typer
import yaml
from pyastgrep import search as pyastgrepsearch  # type: ignore
from rich.console import Console
from trogon import Trogon  # type: ignore
from typer.main import get_group

from chasten import (
    configuration,
    constants,
    debug,
    filesystem,
    output,
    server,
    util,
    validate,
)

# create a Typer object to support the command-line interface
cli = typer.Typer()


class ConfigureTask(str, Enum):
    """Define the different task possibilities."""

    CREATE = "create"
    VALIDATE = "validate"


@cli.command()
def interact(ctx: typer.Context) -> None:
    """Interactively configure and run."""
    Trogon(get_group(cli), click_context=ctx).run()


@cli.command()
def configure(
    task: ConfigureTask = typer.Argument(ConfigureTask.VALIDATE.value),
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
    """Manage tool configuration."""
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
    if task == ConfigureTask.VALIDATE:
        output.console.print(
            ":sparkles: Configuration directory:" + constants.markers.Newline
        )
        # detect and store the platform-specific user
        # configuration directory
        chasten_user_config_dir_str = configuration.user_config_dir(
            application_name=constants.chasten.Application_Name,
            application_author=constants.chasten.Application_Author,
        )
        # create a visualization of the user's configuration directory
        chasten_user_config_dir_path = Path(chasten_user_config_dir_str)
        rich_path_tree = filesystem.create_directory_tree_visualization(
            chasten_user_config_dir_path
        )
        # display the configuration directory
        output.console.print(rich_path_tree)
        output.console.print()
        configuration_file_str = f"{chasten_user_config_dir_str}/config.yml"
        configuration_file_path = Path(configuration_file_str)
        configuration_file_yml = configuration_file_path.read_text()
        data = None
        with open(configuration_file_str) as user_configuration_file:
            data = yaml.safe_load(user_configuration_file)
        # validate the user's configuration and display the results
        (validated, errors) = validate.validate_configuration(data)
        output.console.print(
            f":sparkles: Validated configuration? {util.get_human_readable_boolean(validated)}"
        )
        if not validated:
            output.console.print(f":person_shrugging: Validation errors:\n\n{errors}")
        else:
            output.console.print()
            output.console.print(f"Contents of {configuration_file_str}:\n")
            output.console.print(configuration_file_yml)
    # create the configuration directory and a starting version of the configuration file
    if task == ConfigureTask.CREATE:
        # attempt to create the configuration directory
        try:
            created_directory_path = filesystem.create_configuration_directory(force)
            output.console.print(
                f":sparkles: Created configuration directory and file(s) in {created_directory_path}"
            )
        # cannot re-create the configuration directory, so display
        # a message and suggest the use of --force the next time
        except FileExistsError:
            if not force:
                output.console.print(
                    ":person_shrugging: Configuration directory already exists."
                )
                output.console.print(
                    "Use --force to recreate configuration directory and its containing files."
                )


@cli.command()
def search(
    directory: List[Path] = typer.Option(
        filesystem.get_default_directory_list(),
        "--search-directory",
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
