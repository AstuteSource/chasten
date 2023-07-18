"""Chasten checks the AST of a Python program."""

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Tuple

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


def output_preamble(
    verbose: bool,
    debug_level: debug.DebugLevel = debug.DebugLevel.ERROR,
    debug_destination: debug.DebugDestination = debug.DebugDestination.CONSOLE,
    **kwargs,
) -> None:
    """Output all of the preamble content."""
    # setup the console and the logger through the output module
    output.setup(debug_level, debug_destination)
    output.logger.debug(f"Display verbose output? {verbose}")
    output.logger.debug(f"Debug level? {debug_level.value}")
    output.logger.debug(f"Debug destination? {debug_destination.value}")
    # display the header
    output.print_header()
    # display details about configuration as
    # long as verbose output was requested;
    # note that passing **kwargs to this function
    # will pass along all of the extra keyword
    # arguments that were input to the function
    output.print_diagnostics(
        verbose,
        debug_level=debug_level.value,
        debug_destination=debug_destination.value,
        **kwargs,
    )


def display_configuration_directory(chasten_user_config_dir_str: str):
    # create a visualization of the configuration directory
    chasten_user_config_dir_path = Path(chasten_user_config_dir_str)
    rich_path_tree = filesystem.create_directory_tree_visualization(
        chasten_user_config_dir_path
    )
    # display the visualization of the configuration directory
    output.console.print(rich_path_tree)
    output.console.print()



def extract_configuration_details(
    chasten_user_config_dir_str: str,
    configuration_file: str = constants.filesystem.Main_Configuration_File,
) -> Tuple[str, str, Dict[str, Dict[str, Any]]]:
    """Display details about the configuration."""
    # display_configuration_directory(chasten_user_config_dir_str)
    # create the name of the main configuration file
    configuration_file_str = f"{chasten_user_config_dir_str}/{configuration_file}"
    # load the text of the main configuration file
    configuration_file_path = Path(configuration_file_str)
    configuration_file_yml = configuration_file_path.read_text()
    # load the contents of the main configuration file
    yaml_data = None
    with open(configuration_file_str) as user_configuration_file:
        yaml_data = yaml.safe_load(user_configuration_file)
    # return the file name, the textual contents of the configuration file, and
    # a dict-based representation of the configuration file
    return configuration_file_str, configuration_file_yml, yaml_data


def validate_file(
    configuration_file_str: str,
    configuration_file_yml: str,
    yml_data_dict: Dict[str, Dict[str, Any]],
) -> None:
    """Validate the provided file."""
    # perform the validation of the configuration file
    (validated, errors) = validate.validate_configuration(yml_data_dict)
    output.console.print(
        f":sparkles: Validated file? {util.get_human_readable_boolean(validated)}"
    )
    # there was a validation error, so display the error report
    if not validated:
        output.console.print(f":person_shrugging: Validation errors:\n\n{errors}")
    # validation worked correctly, so display the configuration file
    else:
        output.console.print()
        output.console.print(f":sparkles: Contents of {configuration_file_str}:\n")
        output.console.print(configuration_file_yml)


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
    # output the preamble, including extra parameters specific to this function
    output_preamble(
        verbose, debug_level, debug_destination, task=task.value, force=force
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
        # display details about the configuration directory
        display_configuration_directory(chasten_user_config_dir_str)
        (
            configuration_file_str,
            configuration_file_yml,
            yml_data_dict,
        ) = extract_configuration_details(chasten_user_config_dir_str)
        # validate the user's configuration and display the results
        validate_file(configuration_file_str, configuration_file_yml, yml_data_dict)
        # if one or more exist, retrieve the name of the checks files
        (found_checks_file, checks_file_name_list) = validate.extract_checks_file_name(
            yml_data_dict
        )
        output.console.print(found_checks_file)
        # iteratively extract the contents of each checks file
        # and then validate the contents of that checks file
        for checks_file_name in checks_file_name_list:
            output.console.print(checks_file_name)
            (
                configuration_file_str,
                configuration_file_yml,
                yml_data_dict,
            ) = extract_configuration_details(chasten_user_config_dir_str, checks_file_name)
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
def analyze(
    directory: List[Path] = typer.Option(
        filesystem.get_default_directory_list(),
        "--search-directory",
        "-d",
        help="One or more directories with Python code",
    ),
    verbose: bool = typer.Option(False),
    debug_level: debug.DebugLevel = typer.Option(debug.DebugLevel.ERROR.value),
    debug_destination: debug.DebugDestination = typer.Option(
        debug.DebugDestination.CONSOLE.value, "--debug-dest"
    ),
) -> None:
    """Analyze the AST of Python source code."""
    # output the preamble, including extra parameters specific to this function
    output_preamble(verbose, debug_level, debug_destination, directory=directory)
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
    output.console.print(
        f":sparkles: Analyzing Python source code in:\n {', '.join(str(d) for d in valid_directories)}\n"
    )
    # search for the XML contents of an AST that match the provided
    # XPATH query using the search_python_file in search module of pyastgrep
    match_generator = pyastgrepsearch.search_python_files(
        paths=valid_directories,
        expression='.//FunctionDef[@name="classify"]/body//If[ancestor::If and not(parent::orelse)]',
    )
    # materialize a list out of the generator and then count
    # and display the number of matches inside of the list
    match_generator_list = list(match_generator)
    output.console.print(f"Analyze a total of {len(match_generator_list)} files")
    # display debugging information about the contents of the match generator,
    # note that this only produces output when --verbose is enabled
    output.print_diagnostics(verbose, match_generator_list=match_generator_list)
    for search_output in match_generator:
        output.print_diagnostics(verbose, search_output=search_output)


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
