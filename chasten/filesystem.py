"""Check and access contents of the filesystem."""

import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, NoReturn, Optional, Union

import flatterer  # type: ignore
from rich.tree import Tree

from chasten import configuration, constants, database, results

CONFIGURATION_FILE_DEFAULT_CONTENTS = """
# chasten configuration
# automatically created
chasten:
  # point to a checks file
  checks-file:
    - checks.yml
"""

CHECKS_FILE_DEFAULT_CONTENTS = """
checks:
  - name: "class-definition"
    code: "CDF"
    id: "C001"
    pattern: './/ClassDef'
    count:
      min: 1
      max: 10
  - name: "all-function-definition"
    code: "AFD"
    id: "F001"
    pattern: './/FunctionDef'
    count:
      min: 1
      max: 10
  - name: "non-test-function-definition"
    code: "NTF"
    id: "F002"
    pattern: './/FunctionDef[not(contains(@name, "test_"))]'
    count:
      min: 1
      max: 10
  - name: "single-nested-if"
    code: "SNI"
    id: "CL001"
    pattern: './/FunctionDef/body//If'
    count:
      min: 1
      max: 10
  - name: "double-nested-if"
    code: "DNI"
    id: "CL002"
    pattern: './/FunctionDef/body//If[ancestor::If and not(parent::orelse)]'
    count:
      min: 1
      max: 10
"""

FILE_CONTENTS_LOOKUP = {
    "config.yml": CONFIGURATION_FILE_DEFAULT_CONTENTS,
    "checks.yml": CHECKS_FILE_DEFAULT_CONTENTS,
}


def detect_configuration(config: Optional[Path]) -> str:
    """Detect the configuration."""
    # there is a specified configuration directory path and thus
    # this overrides the use of the platform-specific configuration
    if config is not None:
        chasten_user_config_dir_str = str(config)
    # there is no configuration directory specified and thus
    # this function should access the platform-specific
    # configuration directory detected by platformdirs
    else:
        # detect and store the platform-specific user
        # configuration directory
        chasten_user_config_dir_str = configuration.user_config_dir(
            application_name=constants.chasten.Application_Name,
            application_author=constants.chasten.Application_Author,
        )
    # return in string form the detected configuration directory
    return chasten_user_config_dir_str


def create_configuration_directory(
    config: Optional[Path] = None, force: bool = False
) -> Union[Path, NoReturn]:
    """Create the configuration directory."""
    # detect the configuration directory
    chasten_user_config_dir_str = detect_configuration(config)
    # create a path out of the configuration directory
    chasten_user_config_dir_path = Path(chasten_user_config_dir_str)
    # recursively delete the configuration directory and all of its
    # contents because the force parameter permits deletion
    if force:
        shutil.rmtree(chasten_user_config_dir_path)
    # create the configuration directory, a step that
    # may fail if the directory already exists; in this
    # case the FileExistsError will be passed to caller
    chasten_user_config_dir_path.mkdir(parents=True)
    return chasten_user_config_dir_path


def create_configuration_file(
    config: Path, config_file_name: str = constants.filesystem.Main_Configuration_File
) -> None:
    """Create the main configuration file in the configuration directory."""
    # detect the configuration directory
    chasten_user_config_dir_str = detect_configuration(config)
    # create the final path to the configuration directory
    chasten_user_config_dir_path = Path(chasten_user_config_dir_str)
    # create a path to the configuration file
    chasten_user_config_main_file = chasten_user_config_dir_path / config_file_name
    # create the file (if it does not exist)
    chasten_user_config_main_file.touch()
    # write the default contents of the file
    file_contents = FILE_CONTENTS_LOOKUP[config_file_name]
    chasten_user_config_main_file.write_text(file_contents)


def create_directory_tree_visualization(directory: Path) -> Tree:
    """Create a directory tree visualization using the Rich tree."""
    # display the fully-qualified name of provided directory
    tree = Tree(f":open_file_folder: {directory.as_posix()}")
    # iterate through all directories and file in specified directory
    for p in directory.iterdir():
        # display a folder icon when dealing with a directory
        if p.is_dir():
            style = ":open_file_folder:"
        # display a file icon when dealing with a file
        else:
            style = ":page_facing_up:"
        # create the current object and add it to tree
        label = f"{style} {p.name}"
        tree.add(label)
    # return the completely created tree
    return tree


def confirm_valid_file(file: Path) -> bool:
    """Confirm that the provided file is a valid path that is a file."""
    # determine if the file is not None and if it is a file
    if file is not None:
        # the file is valid
        if file.is_file() and file.exists():
            return True
    # the file was either none or not valid
    return False


def confirm_valid_directory(directory: Path) -> bool:
    """Confirm that the provided directory is a valid path that is a directory."""
    # determine if the file is not None and if it is a file
    if directory is not None:
        # the file is valid
        if directory.is_dir() and directory.exists():
            return True
    # the directory was either none or not valid
    return False


def get_default_directory_list() -> List[Path]:
    """Return the default directory list that is the current working directory by itself."""
    default_directory_list = [Path(constants.filesystem.Current_Directory)]
    return default_directory_list


def write_chasten_results(
    results_path: Path,
    projectname: str,
    results_content: results.Chasten,
    save: bool = False,
) -> str:
    """Write the results of a Chasten subclass of Pydantic BaseModel to the specified directory."""
    if save:
        # extract the unique hexadecimal code that will ensure that
        # this file name is unique when it is being saved
        results_file_uuid = results_content.configuration.fileuuid
        # extract the current date and time when results were created
        formatted_datetime = results_content.configuration.datetime
        # create a file name so that it includes:
        # a) the name of the project
        # b) the date on which analysis was completed
        # c) a unique identifier to handle cased when
        #    two result files are created at "same time"
        complete_results_file_name = f"{constants.filesystem.Main_Results_File_Name}-{projectname}-{formatted_datetime}-{results_file_uuid}.{constants.filesystem.Results_Extension}"
        # create the file and then write the text,
        # using indentation to ensure that JSON file is readable
        results_path_with_file = results_path / complete_results_file_name
        results_json = results_content.model_dump_json(indent=2)
        # use the built-in method with pathlib Path to write the JSON contents
        results_path_with_file.write_text(results_json)
        # return the name of the created file for diagnostic purposes
        return complete_results_file_name
    # saving was not enabled and thus this function cannot
    # return the name of the file that was created during saving
    return constants.markers.Empty_String


def write_dict_results(
    results_json: str,
    results_path: Path,
    projectname: str,
) -> str:
    """Write a JSON file with results to the specified directory."""
    # generate a unique hexadecimal code that will ensure that
    # this file name is unique when it is being saved
    results_file_uuid = uuid.uuid4().hex
    # create a formatted datetime
    formatted_datetime = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    # create a file name so that it includes:
    # a) the name of the project
    # b) the date on which analysis was completed
    # c) a unique identifier to handle cased when
    #    two result files are created at "same time"
    # d) Clear indiciator in the name that this is a combined result
    complete_results_file_name = f"{constants.filesystem.Main_Results_Combined_File_Name}-{projectname}-{formatted_datetime}-{results_file_uuid}.{constants.filesystem.Results_Extension}"
    # create the file and then write the text,
    # using indentation to ensure that JSON file is readable
    results_path_with_file = results_path / complete_results_file_name
    # use the built-in method from pathlib Path to write the JSON contents
    results_path_with_file.write_text(results_json)
    # return the name of the file that contains the JSON dictionary contents
    return complete_results_file_name


def write_flattened_csv_and_database(
    combined_results_json: str,
    results_path: Path,
    projectname: str,
) -> str:
    """Write flattened CSV files with results to the specified directory and create the database."""
    # generate a unique hexadecimal code that will ensure that
    # this file name is unique when it is being saved
    results_file_uuid = uuid.uuid4().hex
    # create a formatted datetime
    formatted_datetime = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    # create a string-based name for the JSON file that contains
    # the combined results, suitable for input to the flatten function
    combined_results_json_file = results_path / Path(combined_results_json)
    combined_results_json_file_str = str(combined_results_json_file)
    # create a final part of the directory name so that it includes:
    # a) the name of the project
    # b) the date on which analysis was completed
    # c) a unique identifier to handle cased when
    #    two directories are created at "same time"
    complete_flattened_results_directory_name = f"{constants.filesystem.Main_Results_Flattened_Directory_Name}-{projectname}-{formatted_datetime}-{results_file_uuid}"
    # the output directory is contained inside of the results_path
    flattened_output_directory = (
        results_path / complete_flattened_results_directory_name
    )
    # the flatten function expects a string-based directory name
    flattened_output_directory_str = str(flattened_output_directory)
    # the SQLite3 database file exists in the directory that will
    # store all of the flattened results in the csv/ directory
    database_file_name = flattened_output_directory / "chasten.db"
    database_file_name_str = str(database_file_name)
    # perform the flattening, creating a directory called csv/ that
    # contains all of the CSV files and a SQLite3 database called chasten.db
    # that contains all of the contents of the CSV files; this chasten.db
    # file is ready for browsing through the use of a tool like datasette
    flatterer.flatten(
        combined_results_json_file_str,
        flattened_output_directory_str,
        csv=True,
        sqlite=True,
        sqlite_path=database_file_name_str,
    )
    # create a view that combines all of the data
    database.create_chasten_view(database_file_name_str)
    # enable full-text search in the SQLite3 database
    database.enable_full_text_search(database_file_name_str)
    # return the name of the directory that contains the flattened CSV files
    return flattened_output_directory_str


def get_json_results(json_paths: List[Path]) -> List[Dict[Any, Any]]:
    """Get a list of dictionaries, one the contents of each JSON file path."""
    # create an empty list of dictionaries
    json_dicts_list: List[Dict[Any, Any]] = []
    # iterate through each of the provided paths to a JSON file
    for json_path in json_paths:
        # turn the contents of the current JSON file into a dictionary
        json_dict = json.loads(json_path.read_text())
        # add the current dictionary to the list of dictionaries
        json_dicts_list.append(json_dict)
    # return the list of JSON dictionaries
    return json_dicts_list
