"""Configuration for Chasten."""

import logging
import logging.config
import logging.handlers
import sys
from typing import Any, Dict, List, Tuple, Union
from pathlib import Path
from urllib3.util import parse_url, Url

import platformdirs
from rich.logging import RichHandler
from rich.traceback import install
import yaml
import requests

from chasten import (
    constants,
    filesystem,
    output,
    util,
    validate,
)


def configure_tracebacks() -> None:
    """Configure stack tracebacks arising from a crash to use rich."""
    install()


def user_config_dir(application_name: str, application_author: str) -> str:
    """Return the user's configuration directory using platformdirs."""
    # access the directory and then return it based on the
    # provided name of the application and the application's author
    chasten_user_config_dir_str = platformdirs.user_config_dir(
        appname=application_name,
        appauthor=application_author,
    )
    return chasten_user_config_dir_str


def configure_logging(
    debug_level: str = constants.logging.Default_Logging_Level,
    debug_dest: str = constants.logging.Default_Logging_Destination,
) -> Tuple[logging.Logger, bool]:
    """Configure standard Python logging package."""
    # use the specified logger with the specified destination
    # by dynamically constructing the function to call and then
    # invoking it with the provided debug_dest parameter
    debug_dest = debug_dest.lower()
    function_name = constants.logger.Function_Prefix + debug_dest
    configure_module = sys.modules[__name__]
    # it was possible to create the requested logger, so return it
    try:
        return (getattr(configure_module, function_name)(debug_level), True)
    # it was not possible to create the requested logger, so
    # return the default console logger as a safe alternative
    except AttributeError:
        return (configure_logging_console(debug_level), False)


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


def validate_configuration_files(
    config: str,
    verbose: bool = False,
) -> Tuple[
    bool, Union[Dict[str, List[Dict[str, Union[str, Dict[str, int]]]]], Dict[Any, Any]]
]:
    """Validate the configuration."""
    chasten_user_config_url_str = ""
    chasten_user_config_dir_str = ""
    chasten_user_config_file_str = ""
    # there is a specified configuration directory path or url;
    # this overrides the use of the configuration files that
    # may exist inside of the platform-specific directory
    if config:
        # the configuration file or url exists and thus it should
        # be used instead of the platform-specific directory

        # input configuration is valid URL
        if util.is_url(config):
            # re-parse input config so it is of type URL
            chasten_user_config_url_str = str(parse_url(config))
        # input configuration is valid file path
        elif Path(config).exists():
            # input configuration is a directory
            if Path(config).is_dir():
                # re-parse input config so it is of type Path
                chasten_user_config_dir_str = str(Path(config))
            # input configuration is a file
            elif Path(config).is_file():
                # re-parse input config so it is of type Path
                config_as_path = Path(config)
                # get directory containing config file
                chasten_user_config_dir_str = str(Path(*config_as_path.parts[: len(config_as_path.parts) - 1]))
                # isolate config file
                chasten_user_config_file_str = str(config_as_path.parts[-1])
            else:
                output.logger.error(
                    "\nGiven configuration was a Path, but was the wrong file type.\n"
                )
        # the configuration file does not exist and thus,
        # since config was explicit, it is not possible
        # to validate the configuration file
        else:
            output.logger.error("\nGiven configuration was not a valid Path or URL.\n")
            return (False, {})
    # there is no configuration file specified and thus
    # this function should access the platform-specific
    # configuration directory detected by platformdirs
    else:
        # detect and store the platform-specific user
        # configuration directory by default
        chasten_user_config_dir_str = user_config_dir(
            application_name=constants.chasten.Application_Name,
            application_author=constants.chasten.Application_Author,
        )

    # input config is a URL
    if chasten_user_config_url_str:
        output.console.print(
            ":sparkles: Configuration URL:"
            + constants.markers.Space
            + chasten_user_config_url_str
            + constants.markers.Newline
        )
        # extract the configuration details
        (
            configuration_valid,
            configuration_file_yaml_str,
            yaml_data_dict,
        ) = extract_configuration_details_from_config_url(
            parse_url(chasten_user_config_url_str)
        )
        configuration_file_source = chasten_user_config_url_str
    # input config is a Path
    elif chasten_user_config_dir_str:
        output.console.print(
            ":sparkles: Configuration directory:"
            + constants.markers.Space
            + chasten_user_config_dir_str
            + constants.markers.Newline
        )
        # optional argument if chasten_user_config_file_str is not empty
        # argument will be supplied as unpacked dict
        chasten_user_config_file_str_argument = {}
        if chasten_user_config_file_str != "":
            chasten_user_config_file_str_argument["configuration_file"] = chasten_user_config_file_str
        # extract the configuration details
        (
            configuration_valid,
            configuration_file_path_str,
            configuration_file_yaml_str,
            yaml_data_dict,
        ) = extract_configuration_details_from_config_dir(
            Path(chasten_user_config_dir_str), **chasten_user_config_file_str_argument
        )
        # it was not possible to extract the configuration details and
        # thus this function should return immediately with False
        # to indicate the failure and an empty configuration dictionary
        if not configuration_valid:
            return (False, {})
        # create a visualization of the user's configuration directory;
        # display details about the configuration directory in console
        display_configuration_directory(chasten_user_config_dir_str, verbose)
        configuration_file_source = chasten_user_config_dir_str

    # Summary of the remaining steps:
    # --> Step 1: Validate the main configuration file
    # --> Step 2: Validate the one or more checks files
    # --> Step 3: If all files are valid, return overall validity
    # --> Step 3: Otherwise, return an invalid configuration
    # validate the user's configuration and display the results
    config_file_validated = validate.validate_file(
        configuration_file_source,
        configuration_file_yaml_str,
        yaml_data_dict,
        validate.JSON_SCHEMA_CONFIG,
        verbose,
    )

    # if one or more exist, retrieve the name of the checks files
    (_, checks_file_name_list) = validate.extract_checks_file_name(yaml_data_dict)
    # iteratively extract the contents of each checks file
    # and then validate the contents of that checks file
    checks_files_validated_list = []
    check_files_validated = False
    # create an empty dictionary that will store the list of checks
    overall_checks_dict: Union[
        Dict[str, List[Dict[str, Union[str, Dict[str, int]]]]], Dict[Any, Any]
    ] = {}
    # create an empty list that will store the dicts of checks
    overall_checks_list: List[Dict[str, Union[str, Dict[str, int]]]] = []
    # initialize the dictionary to contain the empty list
    overall_checks_dict[constants.checks.Checks_Label] = overall_checks_list
    for checks_file_name in checks_file_name_list:
        # specified check file is URL
        if util.is_url(checks_file_name):
            # extract the configuration details
            (
                checks_file_extracted_valid,
                configuration_file_yaml_str,
                yaml_data_dict,
            ) = extract_configuration_details_from_config_url(
                parse_url(checks_file_name)
            )
            # name of checks file is a url and thus can be used for logging
            checks_file_source = checks_file_name
        # assume check file name is a file path
        elif (Path(chasten_user_config_dir_str) / Path(checks_file_name)).exists():
            # will not support checks files being local paths
            # if config file is a URL
            if isinstance(config, Url):
                output.logger.error(
                    f"\nChecks file directive was a Path when config was a URL (given: '{checks_file_name}')\n"
                )
                return (False, {})
            # extract the configuration details
            (
                checks_file_extracted_valid,
                configuration_file_path_str,
                configuration_file_yaml_str,
                yaml_data_dict,
            ) = extract_configuration_details_from_config_dir(
                Path(chasten_user_config_dir_str), checks_file_name
            )
            # configuration path returned from extraction function can be used for logging
            checks_file_source = configuration_file_path_str
        else:
            # checks file was not valid
            output.logger.error(
                f"\nChecks file directive was not a valid Path or URL (given: '{checks_file_name}')\n"
            )
            return (False, {})
        # the checks file could not be extracted in a valid
        # fashion and thus there is no need to continue the
        # validation of this file or any of the other check file
        if not checks_file_extracted_valid:
            check_file_validated = False
        # the checks file could be extract and thus the
        # function should proceed to validate a checks configuration file
        else:
            # validate checks file
            check_file_validated = validate.validate_file(
                checks_file_source,
                configuration_file_yaml_str,
                yaml_data_dict,
                validate.JSON_SCHEMA_CHECKS,
                verbose,
            )
        # keep track of the validation of all of validation
        # records for each of the check files
        checks_files_validated_list.append(check_file_validated)
        # add the listing of checks from the current yaml_data_dict to
        # the overall listing of checks in the main dictionary
        overall_checks_dict[constants.checks.Checks_Label].extend(yaml_data_dict[constants.checks.Checks_Label])  # type: ignore
    # the check files are only validated if all of them are valid
    check_files_validated = all(checks_files_validated_list)
    # the files validated correctly; return an indicator to
    # show that validation worked and then return the overall
    # dictionary that contains the listing of valid checks
    if config_file_validated and check_files_validated:
        return (True, overall_checks_dict)
    # there was at least one validation error
    return (False, {})


def extract_configuration_details_from_config_dir(
    chasten_user_config_dir_str: Path,
    configuration_file: str = constants.filesystem.Main_Configuration_File,
) -> Tuple[bool, str, str, Dict[str, Dict[str, Any]]]:
    """Extract details from the configuration given a config directory.

    chasten_user_config_dir_str -- directory to search for config file
    configuration_file -- optional configuration file to specify. If not supplied, a default location will be searched
    """
    # create the name of the main configuration file
    # load the text of the main configuration file
    configuration_file_path = chasten_user_config_dir_str / configuration_file
    # the configuration file does not exist and thus
    # the extraction process cannot continue, the use of
    # these return values indicates that the extraction
    # failed and any future steps cannot continue
    if not configuration_file_path.exists():
        output.logger.error(
            f"\nFinding config or check file Path failed for {configuration_file_path}.\n"
        )
        return (False, None, None, None)  # type: ignore
    configuration_file_yaml_str = configuration_file_path.read_text()
    # load the contents of the main configuration file
    with open(str(configuration_file_path)) as user_configuration_file_text:
        (yaml_success, yaml_data) = convert_configuration_text_to_yaml(
            user_configuration_file_text.read()
        )
        # return success status, filename, file contents, and yaml parsed data upon success
        if yaml_success:
            return (
                True,
                str(configuration_file_path),
                configuration_file_yaml_str,
                yaml_data,
            )
        # return none types upon failure in yaml parsing
        else:
            output.logger.error(
                f"\nParsing YAML from config or check file Path failed for {configuration_file_path}.\n"
            )
            return (False, None, None, None)  # type: ignore


def extract_configuration_details_from_config_url(
    chasten_user_config_url: Url,
) -> Tuple[bool, str, Dict[str, Dict[str, Any]]]:
    """Extract details from the configuration given a config URL.

    chasten_user_config_url -- URL to config or checks yaml file.
    """
    # create request with given URL as source
    response = requests.get(str(chasten_user_config_url))
    # the URL response is OK
    if response.ok:
        # assume URL endpoint returns raw text
        configuration_file_yaml_str = response.text
    # the URL indicates a problem with the response
    else:
        output.logger.error(
            f"\nLoading config or check file URL failed for {chasten_user_config_url}.\n"
        )
        return (False, None, None)  # type: ignore
    (yaml_success, yaml_data) = convert_configuration_text_to_yaml(
        configuration_file_yaml_str
    )
    # return success status, filename, file contents, and yaml parsed data upon success
    if yaml_success:
        return (True, configuration_file_yaml_str, yaml_data)
    else:
        output.logger.error(
            f"\nParsing YAML from config or check file URL failed for {chasten_user_config_url}.\n"
        )
        return (False, None, None)  # type: ignore


def convert_configuration_text_to_yaml(
    configuration_file_contents_str: str,
) -> Tuple[bool, Dict[str, Dict[str, Any]]]:
    """Return details about the configuration."""
    yaml_data = None
    try:
        yaml_data = yaml.safe_load(configuration_file_contents_str)
    except Exception:
        # yaml parsing has failed and we will indicate the input is invalid
        return (False, None)  # type: ignore
    # return the file name, the textual contents of the configuration file, and
    # a dict-based representation of the configuration file
    return (True, yaml_data)
