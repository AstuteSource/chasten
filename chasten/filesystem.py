"""Check and access contents of the filesystem."""

import shutil
import uuid
from pathlib import Path
from typing import List, NoReturn, Optional, Union

from pydantic import BaseModel
from rich.tree import Tree

from chasten import configuration, constants

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


def write_results(
    results_path: Path, projectname: str, results_content: BaseModel
) -> None:
    """Write the results of a Pydantic BaseModel to the specified directory."""
    results_file_uuid = uuid.uuid4().hex
    complete_results_file_name = f"{constants.filesystem.Main_Results_File_Name}-{projectname}-{results_file_uuid}.{constants.filesystem.Results_Extension}"
    results_path_with_file = results_path / complete_results_file_name
    results_json = results_content.model_dump_json(indent=2)
    results_path_with_file.write_text(results_json)
