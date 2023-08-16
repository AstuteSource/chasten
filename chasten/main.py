"""Chasten checks the AST of a Python program."""

import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import typer
import yaml
from pyastgrep import search as pyastgrepsearch  # type: ignore
from trogon import Trogon  # type: ignore
from typer.main import get_group

from chasten import (
    checks,
    configuration,
    constants,
    debug,
    enumerations,
    filesystem,
    output,
    process,
    results,
    server,
    util,
    validate,
)

# create a Typer object to support the command-line interface
cli = typer.Typer()

small_bullet_unicode = "\u2022"

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
    """🚀 Interactively configure and run."""
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
    force: bool = typer.Option(
        False,
        help="Create configuration directory and files even if they exist",
    ),
    verbose: bool = typer.Option(False, help="Display verbose debugging output"),
) -> None:
    """🪂 Manage chasten's configuration."""
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
        # exit early and signal an error with a non-zero exist code
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
    # extract the current version of the program
    chasten_version = util.get_chasten_version()
    # create the include and exclude criteria
    include = results.CheckCriterion(
        attribute=str(checks.fix_check_criterion(check_include[0])),
        value=str(checks.fix_check_criterion(check_include[1])),
        confidence=int(checks.fix_check_criterion(check_include[2])),
    )
    exclude = results.CheckCriterion(
        attribute=str(checks.fix_check_criterion(check_exclude[0])),
        value=str(checks.fix_check_criterion(check_exclude[1])),
        confidence=int(checks.fix_check_criterion(check_exclude[2])),
    )
    # create a configuration that is the same for all results
    chasten_configuration = results.Configuration(
        chastenversion=chasten_version,
        projectname=project,
        configdirectory=config,
        searchpath=input_path,
        debuglevel=debug_level,
        debugdestination=debug_destination,
        checkinclude=include,
        checkexclude=exclude,
    )
    # connect the configuration to the top-level chasten object for results saving
    # note: this is the final object that contains all of the data
    chasten_results_save = results.Chasten(configuration=chasten_configuration)
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
    output.console.print()
    output.console.print(f":sparkles: Analyzing Python source code in: {input_path}")
    # output the number of checks that will be performed
    output.console.print()
    output.console.print(f":tada: Performing {len(check_list)} check(s):")
    output.console.print()
    # create a check_status list for all of the checks
    check_status_list: List[bool] = []
    # iterate through and perform each of the checks
    for current_check in check_list:
        # extract the pattern for the current check
        current_xpath_pattern = str(current_check[constants.checks.Check_Pattern])  # type: ignore
        # extract the minimum and maximum values for the checks, if they exist
        # note that this function will return None for a min or a max if
        # that attribute does not exist inside of the current_check; importantly,
        # having a count or a min or a max is all optional in a checks file
        (min_count, max_count) = checks.extract_min_max(current_check)
        # extract details about the check to display in the header
        # of the syntax box for this specific check
        check_id = current_check[constants.checks.Check_Id]  # type: ignore
        check_name = current_check[constants.checks.Check_Name]  # type: ignore
        check_description = checks.extract_description(current_check)
        # search for the XML contents of an AST that match the provided
        # XPATH query using the search_python_file in search module of pyastgrep;
        # this looks for matches across all path(s) in the specified source path
        match_generator = pyastgrepsearch.search_python_files(
            paths=valid_directories, expression=current_xpath_pattern, xpath2=True
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
        # organize the matches according to the file to which they
        # correspond so that processing of matches takes place per-file
        match_dict = process.organize_matches(match_generator_list)
        # perform an enforceable check if it is warranted for this check
        current_check_save = None
        if checks.is_checkable(min_count, max_count):
            # determine whether or not the number of found matches is within mix and max
            check_status = checks.check_match_count(
                len(match_generator_list), min_count, max_count
            )
            # keep track of the outcome for this check
            check_status_list.append(check_status)
        # this is not an enforceable check and thus the tool always
        # records that the checked passed as a default
        else:
            check_status = True
        # convert the status of the check to a visible symbol for display
        check_status_symbol = util.get_symbol_boolean(check_status)
        # escape the open bracket symbol that may be in an XPATH expression
        # and will prevent it from displaying correctly
        current_xpath_pattern_escape = current_xpath_pattern.replace("[", "\\[")
        # display minimal diagnostic output
        output.console.print(
            f"  {check_status_symbol} id: '{check_id}', name: '{check_name}'"
            + f", pattern: '{current_xpath_pattern_escape}', min={min_count}, max={max_count}"
        )
        # for each potential match, log and, if verbose model is enabled,
        # display details about each of the matches
        current_result_source = results.Source(
            filename=str(str(vd) for vd in valid_directories)
        )
        # there were no matches and thus the current_check_save of None
        # should be recorded inside of the source of the results
        if len(match_generator_list) == 0:
            current_result_source.check = current_check_save
        # iteratively analyze:
        # a) A specific file name
        # b) All of the matches for that file name
        # Note: the goal is to only process matches for a
        # specific file, ensuring that matches for different files
        # are not mixed together, which would contaminate the results
        # Note: this is needed because using pyastgrepsearch will
        # return results for all of the files that matched the check
        for file_name, matches_list in match_dict.items():
            # create the current check
            current_check_save = results.Check(
                id=check_id,  # type: ignore
                name=check_name,  # type: ignore
                description=check_description,  # type: ignore
                min=min_count,  # type: ignore
                max=max_count,  # type: ignore
                pattern=current_xpath_pattern,
                passed=check_status,
            )
            # create a source that is solely for this file name
            current_result_source = results.Source(filename=file_name)
            # put the current check into the list of checks in the current source
            current_result_source.check = current_check_save
            # display minimal diagnostic output
            output.console.print(
                f"    {small_bullet_unicode} {file_name} - {len(matches_list)} matches"
            )
            # extract the lines of source code for this file; note that all of
            # these matches are organized for the same file and thus it is
            # acceptable to extract the lines of the file from the first match
            # a long as there are matches available for analysis
            if len(matches_list) > 0:
                current_result_source.filelines = matches_list[0].file_lines
            # iterate through all of the matches that are specifically
            # connected to this source that is connected to a specific file name
            for current_match in matches_list:
                if isinstance(current_match, pyastgrepsearch.Match):
                    current_result_source.filelines = current_match.file_lines
                    # extract the direct line number for this match
                    position_end = current_match.position.lineno
                    # extract the column offset for this match
                    column_offset = current_match.position.col_offset
                    # create a match specifically for this file;
                    # note that the AST starts line numbering at 1 and
                    # this means that storing the matching line requires
                    # the indexing of file_lines with position_end - 1;
                    # note also that linematch is the result of using
                    # lstrip to remove any blank spaces before the code
                    current_match_for_current_check_save = results.Match(
                        lineno=position_end,
                        coloffset=column_offset,
                        linematch=current_match.file_lines[position_end - 1].lstrip(constants.markers.Space),
                    )
                    # save the entire current_match that is an instance of
                    # pyastgrepsearch.Match for verbose debugging output as needed
                    current_check_save._matches.append(current_match)
                    # add the match to the listing of matches for the current check
                    current_check_save.matches.append(current_match_for_current_check_save)  # type: ignore
            # add the current source to main object that contains a list of source
            chasten_results_save.sources.append(current_result_source)
    # display all of the analysis results if verbose output is requested
    output.print_analysis_details(chasten_results_save, verbose=verbose)
    # save all of the results from this analysis
    filesystem.write_results(output_directory, project, chasten_results_save, save)
    # confirm whether or not all of the checks passed
    # and then display the appropriate diagnostic message
    all_checks_passed = all(check_status_list)
    if not all_checks_passed:
        output.console.print("\n:sweat: At least one check did not pass.")
        sys.exit(constants.markers.Non_Zero_Exit)
    output.console.print("\n:joy: All checks passed.")


@cli.command()
def convert(
    json_path: List[Path] = typer.Argument(
        help="Directories, files, or globs for chasten's JSON result file(s).",
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
    force: bool = typer.Option(
        False,
        help="Create converted results files even if they exist",
    ),
    verbose: bool = typer.Option(False, help="Display verbose debugging output"),
) -> None:
    """🚧 Convert files to different formats."""
    # output the preamble, including extra parameters specific to this function
    output_preamble(
        verbose,
        debug_level,
        debug_destination,
        json_paths=json_path,
        force=force,
    )
    # output the list of directories subject to checking
    output.console.print()
    output.console.print(f":sparkles: Converting data file(s) in: {json_path}")
    filesystem.get_json_results(json_path)



@cli.command()
def log() -> None:
    """🦚 Start the logging server."""
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
    # db = "chasten.db"
    # metadata = "metadata.json"
    # cmd = ["datasette", db, "-m", metadata]
    # proc = subprocess.Popen(cmd)
    # proc.wait()
