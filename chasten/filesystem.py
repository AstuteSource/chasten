"""Check and access contents of the filesystem."""

from pathlib import Path
from typing import List

from rich.tree import Tree

from chasten import constants


def create_directory_tree(directory: Path) -> Tree:
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
