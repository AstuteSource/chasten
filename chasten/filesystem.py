"""Check and access contents of the filesystem."""

import shutil
from pathlib import Path
from typing import List, NoReturn, Union

from platformdirs import user_config_dir
from rich.tree import Tree

from chasten import configuration, constants


def create_configuration_directory(force: bool = False) -> Union[Path, NoReturn]:
    """Create the configuration directory."""
    # use the configuration package to detect what is the
    # platform-specific user configuration directory; provide
    # the function with the default name of the application
    # and the default name of the application's author
    chasten_user_config_dir_str = configuration.user_config_dir(
        application_name=constants.chasten.Application_Name,
        application_author=constants.chasten.Application_Author,
    )
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
