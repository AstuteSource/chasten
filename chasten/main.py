"""Chasten checks the AST of a Python program."""

import sys
from copy import deepcopy
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import typer
import yaml
from pyastgrep import search as pyastgrepsearch  # type: ignore
from rich.panel import Panel
from rich.syntax import Syntax
from trogon import Trogon  # type: ignore
from typer.main import get_group

from chasten import checks
from chasten import configuration
from chasten import constants
from chasten import debug
from chasten import enumerations
from chasten import filesystem
from chasten import output
from chasten import process
from chasten import results
from chasten import server
from chasten import util
from chasten import validate

# create a Typer object to support the command-line interface
cli = typer.Typer()


# ---
# Region: helper functions
# ---


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


def display_configuration_directory(
    chasten_user_config_dir_str: str, verbose: bool = False
) -> None:
    """Display information about the configuration in the console."""
    # create a visualization of the configuration directory
    chasten_user_config_dir_path = Path(chasten_user_config_dir_str)
    rich_path_tree = filesystem.create_directory_tree_visualization(
        chasten_user_config_dir_path
    )
    # display the visualization of the configuration directory
    output.opt_print_log(verbose, tree=rich_path_tree)
    output.opt_print_log(verbose, empty="")


def extract_configuration_details(
    chasten_user_config_dir_str: str,
    configuration_file: str = constants.filesystem.Main_Configuration_File,
) -> Tuple[bool, str, str, Dict[str, Dict[str, Any]]]:
    """Display details about the configuration."""
    # create the name of the main configuration file
    configuration_file_str = f"{chasten_user_config_dir_str}/{configuration_file}"
    # load the text of the main configuration file
    configuration_file_path = Path(configuration_file_str)
    # the configuration file does not exist and thus
    # the extraction process cannot continue, the use of
    # these return values indicates that the extraction
    # failed and any future steps cannot continue
    if not configuration_file_path.exists():
        return (False, None, None, None)  # type: ignore
    configuration_file_yml = configuration_file_path.read_text()
    # load the contents of the main configuration file
    yaml_data = None
    with open(configuration_file_str) as user_configuration_file:
        yaml_data = yaml.safe_load(user_configuration_file)
    # return the file name, the textual contents of the configuration file, and
    # a dict-based representation of the configuration file
    return (True, configuration_file_str, configuration_file_yml, yaml_data)


def validate_file(
    configuration_file_str: str,
    configuration_file_yml: str,
    yml_data_dict: Dict[str, Dict[str, Any]],
    json_schema: Dict[str, Any] = validate.JSON_SCHEMA_CONFIG,
    verbose: bool = False,
) -> bool:
    """Validate the provided file according to the provided JSON schema."""
    # perform the validation of the configuration file
    (validated, errors) = validate.validate_configuration(yml_data_dict, json_schema)
    output.console.print(
        f":sparkles: Validated {configuration_file_str}? {util.get_human_readable_boolean(validated)}"
    )
    # there was a validation error, so display the error report
    if not validated:
        output.console.print(f":person_shrugging: Validation errors:\n\n{errors}")
    # validation worked correctly, so display the configuration file
    else:
        output.opt_print_log(verbose, newline="")
        output.opt_print_log(
            verbose, label=f":sparkles: Contents of {configuration_file_str}:\n"
        )
        output.opt_print_log(verbose, config_file=configuration_file_yml)
    return validated


def validate_configuration_files(
    config: Path,
    verbose: bool = False,
) -> Tuple[
    bool, Union[Dict[str, List[Dict[str, Union[str, Dict[str, int]]]]], Dict[Any, Any]]
]:
    """Validate the configuration."""
    # there is a specified configuration directory path;
    # this overrides the use of the configuration files that
    # may exist inside of the platform-specific directory
    if config:
        # the configuration file exists and thus it should
        # be used instead of the platform-specific directory
        if config.exists():
            chasten_user_config_dir_str = str(config)
        # the configuration file does not exist and thus,
        # since config was explicit, it is not possible
        # to validate the configuration file
        else:
            return (False, {})
    # there is no configuration file specified and thus
    # this function should access the platform-specific
    # configuration directory detected by platformdirs
    else:
        # detect and store the platform-specific user
        # configuration directory
        chasten_user_config_dir_str = configuration.user_config_dir(
            application_name=constants.chasten.Application_Name,
            application_author=constants.chasten.Application_Author,
        )
    output.console.print(
        ":sparkles: Configuration directory:"
        + constants.markers.Space
        + chasten_user_config_dir_str
        + constants.markers.Newline
    )
    # extract the configuration details
    (
        configuration_valid,
        configuration_file_str,
        configuration_file_yml,
        yml_data_dict,
    ) = extract_configuration_details(chasten_user_config_dir_str)
    # it was not possible to extract the configuration details and
    # thus this function should return immediately with False
    # to indicate the failure and an empty configuration dictionary
    if not configuration_valid:
        return (False, {})
    # create a visualization of the user's configuration directory;
    # display details about the configuration directory in console
    display_configuration_directory(chasten_user_config_dir_str, verbose)
    # Summary of the remaining steps:
    # --> Step 1: Validate the main configuration file
    # --> Step 2: Validate the one or more checks files
    # --> Step 3: If all files are valid, return overall validity
    # --> Step 3: Otherwise, return an invalid configuration
    # validate the user's configuration and display the results
    config_file_validated = validate_file(
        configuration_file_str,
        configuration_file_yml,
        yml_data_dict,
        validate.JSON_SCHEMA_CONFIG,
        verbose,
    )
    # if one or more exist, retrieve the name of the checks files
    (_, checks_file_name_list) = validate.extract_checks_file_name(yml_data_dict)
    # iteratively extract the contents of each checks file
    # and then validate the contents of that checks file
    checks_files_validated_list = []
    check_files_validated = False
    # create an empty dictionary that will store the list of checks
    overall_checks_dict: Union[
        Dict[str, List[Dict[str, Union[str, Dict[str, int]]]]], Dict[Any, Any]
    ] = {}
    # create abn empty list that will store the dicts of checks
    overall_checks_list: List[Dict[str, Union[str, Dict[str, int]]]] = []
    # initialize the dictionary to contain the empty list
    overall_checks_dict[constants.checks.Checks_Label] = overall_checks_list
    for checks_file_name in checks_file_name_list:
        (
            checks_file_extracted_valid,
            configuration_file_str,
            configuration_file_yml,
            yml_data_dict,
        ) = extract_configuration_details(chasten_user_config_dir_str, checks_file_name)
        # the checks file could not be extracted in a valid
        # fashion and thus there is no need to continue the
        # validation of this file or any of the other check file
        if not checks_file_extracted_valid:
            check_file_validated = False
        # the checks file could be extract and thus the
        # function should proceed to validate a checks configuration file
        else:
            check_file_validated = validate_file(
                configuration_file_str,
                configuration_file_yml,
                yml_data_dict,
                validate.JSON_SCHEMA_CHECKS,
                verbose,
            )
        # keep track of the validation of all of validation
        # records for each of the check files
        checks_files_validated_list.append(check_file_validated)
        # add the listing of checks from the current yml_data_dict to
        # the overall listing of checks in the main dictionary
        overall_checks_dict[constants.checks.Checks_Label].extend(yml_data_dict[constants.checks.Checks_Label])  # type: ignore
    # the check files are only validated if all of them are valid
    check_files_validated = all(checks_files_validated_list)
    # the files validated correctly; return an indicator to
    # show that validation worked and then return the overall
    # dictionary that contains the listing of valid checks
    if config_file_validated and check_files_validated:
        return (True, overall_checks_dict)
    # there was at least one validation error
    return (False, {})


# ---
# Region: command-line interface functions
# ---


@cli.command()
def interact(ctx: typer.Context) -> None:
    """Interactively configure and run."""
    # construct a Trogon object; this will create a
    # terminal-user interface that will allow the
    # person using chasten to pick a mode and then
    # fill-in command-line arguments and then
    # run the tool; note that this line of code
    # cannot be easily tested in an automated fashion
    Trogon(get_group(cli), click_context=ctx).run()


@cli.command()
def configure(  # noqa: PLR0913
    task: enumerations.ConfigureTask = typer.Argument(
        enumerations.ConfigureTask.VALIDATE.value
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Create configuration directory and files even if they exist",
    ),
    config: Path = typer.Option(
        None,
        "--config",
        "-c",
        help="A directory with configuration file(s).",
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
        verbose,
        debug_level,
        debug_destination,
        task=task.value,
        config=config,
        force=force,
    )
    # display the configuration directory and its contents
    if task == enumerations.ConfigureTask.VALIDATE:
        # validate the configuration files:
        # --> config.yml
        # --> checks.yml (or whatever file is reference in config.yml)
        (validated, _) = validate_configuration_files(config, verbose)
        # some aspect of the configuration was not
        # valid, so exit early and signal an error
        if not validated:
            output.console.print(
                "\n:person_shrugging: Cannot perform analysis due to configuration error(s).\n"
            )
            sys.exit(constants.markers.Non_Zero_Exit)
    # create the configuration directory and a starting version of the configuration file
    if task == enumerations.ConfigureTask.CREATE:
        # attempt to create the configuration directory
        try:
            # create the configuration directory, which will either be the one
            # specified by the config parameter (if it exists) or it will be
            # the one in the platform-specific directory given by platformdirs
            created_directory_path = filesystem.create_configuration_directory(
                config, force
            )
            # write the configuration file for the chasten tool in the created directory
            filesystem.create_configuration_file(
                created_directory_path, constants.filesystem.Main_Configuration_File
            )
            # write the check file for the chasten tool in the created directory
            filesystem.create_configuration_file(
                created_directory_path, constants.filesystem.Main_Checks_File
            )
            # display diagnostic information about the completed process
            output.console.print(
                f":sparkles: Created configuration directory and file(s) in {created_directory_path}"
            )
        # cannot re-create the configuration directory, so display
        # a message and suggest the use of --force the next time;
        # exit early and signal an error
        except FileExistsError:
            if not force:
                output.console.print(
                    "\n:person_shrugging: Configuration directory already exists."
                )
                output.console.print(
                    "Use --force to recreate configuration directory and its containing files."
                )
            sys.exit(constants.markers.Non_Zero_Exit)


@cli.command()
def analyze(  # noqa: PLR0913, PLR0915
    project: str = typer.Option(
        ..., "--project-name", "-p", help="Name of the project."
    ),
    check_include: Tuple[enumerations.FilterableAttribute, str, int] = typer.Option(
        (None, None, 0),
        "--check-include",
        "-i",
        help="Attribute name, value, and match confidence level for inclusion.",
    ),
    check_exclude: Tuple[enumerations.FilterableAttribute, str, int] = typer.Option(
        (None, None, 0),
        "--check-exclude",
        "-e",
        help="Attribute name, value, and match confidence level for exclusion.",
    ),
    input_path: Path = typer.Option(
        filesystem.get_default_directory_list(),
        "--search-path",
        "-d",
        help="A path (i.e., directory or file) with Python source code(s).",
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    output_directory: Path = typer.Option(
        None,
        "--save-directory",
        "-s",
        help="A directory for saving output file(s).",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=True,
        resolve_path=True,
    ),
    config: Path = typer.Option(
        None,
        "--config",
        "-c",
        help="A directory with configuration file(s).",
    ),
    debug_level: debug.DebugLevel = typer.Option(
        debug.DebugLevel.ERROR.value,
        "--debug-level",
        "-l",
        help="Specify the level of debugging output.",
    ),
    debug_destination: debug.DebugDestination = typer.Option(
        debug.DebugDestination.CONSOLE.value,
        "--debug-dest",
        "-t",
        help="Specify the destination for debugging output.",
    ),
    verbose: bool = typer.Option(False, help="Enable verbose mode output."),
    save: bool = typer.Option(False, help="Enable saving of output file(s)."),
) -> None:
    """💫 Analyze the AST of Python source code."""
    # output the preamble, including extra parameters specific to this function
    output_preamble(
        verbose,
        debug_level,
        debug_destination,
        project=project,
        directory=input_path,
    )
    # create and store a configuration object for the result
    configuration = results.Configuration(
        projectname=project,
        configdirectory=config,
        searchpath=input_path,
        debuglevel=debug_level,
        debugdestination=debug_destination,
    )
    results.components[results.ComponentTypes.Configuration] = configuration
    output.console.print(results.components)
    # add extra space after the command to run the program
    output.console.print()
    # validate the configuration
    (validated, checks_dict) = validate_configuration_files(config, verbose)
    # some aspect of the configuration was not
    # valid, so exit early and signal an error
    if not validated:
        output.console.print(
            "\n:person_shrugging: Cannot perform analysis due to configuration error(s).\n"
        )
        sys.exit(constants.markers.Non_Zero_Exit)
    # extract the list of the specific patterns (i.e., the XPATH expressions)
    # that will be used to analyze all of the XML-based representations of
    # the Python source code found in the valid directories
    check_list: List[Dict[str, Union[str, Dict[str, int]]]] = checks_dict[
        constants.checks.Checks_Label
    ]
    # filter the list of checks based on the include and exclude parameters
    # --> only run those checks that were included
    check_list = process.include_or_exclude_checks(  # type: ignore
        check_list, include=True, *check_include
    )
    # --> remove those checks that were excluded
    check_list = process.include_or_exclude_checks(  # type: ignore
        check_list, include=False, *check_exclude
    )
    # the specified search path is not valid and thus it is
    # not possible to analyze the Python source files in this directory
    # OR
    # the specified search path is not valid and thus it is
    # not possible to analyze the specific Python source code file
    if not filesystem.confirm_valid_directory(
        input_path
    ) and not filesystem.confirm_valid_file(input_path):
        output.console.print(
            "\n:person_shrugging: Cannot perform analysis due to invalid search directory.\n"
        )
        sys.exit(constants.markers.Non_Zero_Exit)
    # create the list of directories
    valid_directories = [input_path]
    # output the list of directories subject to checking
    output.console.print(f":sparkles: Analyzing Python source code in:\n{input_path}")
    # output the number of checks that will be performed
    output.console.print()
    output.console.print(
        f":tada: Running a total of {len(check_list)} matching check(s):"
    )
    # create a check_status list for all of the checks
    check_status_list: List[bool] = []
    # iterate through and perform each of the checks
    for current_check in check_list:
        # extract the pattern for the current check
        current_xpath_pattern = str(current_check[constants.checks.Check_Pattern])  # type: ignore
        # display the XPATH expression for the current check
        output.console.print("\n:tada: Performing check:")
        xpath_syntax = Syntax(
            current_xpath_pattern,
            constants.markers.Xml,
            theme=constants.chasten.Theme_Colors,
        )
        # extract the minimum and maximum values for the checks, if they exist
        # note that this function will return None for a min or a max if
        # that attribute does not exist inside of the current_check; importantly,
        # having a count or a min or a max is all optional in a checks file
        (min_count, max_count) = checks.extract_min_max(current_check)
        min_label = checks.create_attribute_label(min_count, constants.checks.Check_Min)
        max_label = checks.create_attribute_label(max_count, constants.checks.Check_Max)
        # extract details about the check to display in the header
        # of the syntax box for this specific check
        check_id = current_check[constants.checks.Check_Id]  # type: ignore
        check_id_label = checks.create_attribute_label(check_id, constants.checks.Check_Id)  # type: ignore
        check_name = current_check[constants.checks.Check_Name]  # type: ignore
        check_name_label = checks.create_attribute_label(check_name, constants.checks.Check_Name)  # type: ignore
        # create the combined attribute label that displays all details for the check
        combined_attribute_label = checks.join_attribute_labels(
            [check_id_label, check_name_label, min_label, max_label]
        )
        # display the check with additional details about its configuration
        output.console.print(
            Panel(
                xpath_syntax,
                expand=False,
                title=f"{combined_attribute_label}",
            )
        )
        # search for the XML contents of an AST that match the provided
        # XPATH query using the search_python_file in search module of pyastgrep
        match_generator = pyastgrepsearch.search_python_files(
            paths=valid_directories,
            expression=current_xpath_pattern,
        )
        # materialize a list from the generator of (potential) matches;
        # note that this list will also contain an object that will
        # indicate that the analysis completed for each located file
        match_generator_list = list(match_generator)
        # filter the list of matches so that it only includes
        # those that are a Match object that will contain source code
        (match_generator_list, _) = process.filter_matches(
            match_generator_list, pyastgrepsearch.Match
        )
        output.console.print()
        output.console.print(
            f":sparkles: Found a total of {len(match_generator_list)} matches"
        )
        # perform an enforceable check if it is warranted for this check
        if checks.is_checkable(min_count, max_count):
            # determine whether or not the number of found matches is within mix and max
            check_status = checks.check_match_count(
                len(match_generator_list), min_count, max_count
            )
            # produce and display a status message about the check
            check_status_message = checks.make_checks_status_message(check_status)
            output.console.print(check_status_message)
            # keep track of the outcome for this check
            check_status_list.append(check_status)
        # for each potential match, log and, if verbose model is enabled,
        # display details about each of the matches
        for search_output in match_generator_list:
            if isinstance(search_output, pyastgrepsearch.Match):
                # display a label for matching output information
                output.opt_print_log(verbose, blank=constants.markers.Empty_String)
                output.opt_print_log(verbose, label=":sparkles: Matching source code:")
                # extract the direct line number for this match
                position_end = search_output.position.lineno
                # extract the column offset for this match
                column_offset = search_output.position.col_offset
                # get a pre-defined number of the lines both
                # before and after the line that is the closest match;
                # note that the use of "*" is an indicator of the
                # specific line that is the focus of the search
                all_lines = search_output.file_lines
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
                output.opt_print_log(
                    verbose,
                    panel=Panel(
                        code_syntax,
                        expand=False,
                        title=f"{search_output.path}:{position_end}:{column_offset}",
                    ),
                )
    # confirm whether or not all of the checks passed
    # and then display the appropriate diagnostic message
    all_checks_passed = all(check_status_list)
    if not all_checks_passed:
        output.console.print("\n:sweat: At least one check did not pass.")
        sys.exit(constants.markers.Non_Zero_Exit)
    output.console.print("\n:joy: All checks passed.")


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
