"""Chasten checks the AST of a Python program."""

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

# create a Typer object to support the command-line interface
cli = typer.Typer()


def confirm_valid_file(file: Path) -> bool:
    """Confirm that the provided file is a valid path that is a file."""
    # determine if the file is not None and if it is a file
    if file is not None:
        # the file is valid
        if file.is_file():
            return True
    # the file was either none or not valid
    return False


def confirm_valid_directory(directory: Path) -> bool:
    """Confirm that the provided directory is a valid path that is a directory."""
    # determine if the file is not None and if it is a file
    if directory is not None:
        # the file is valid
        if directory.is_dir():
            return True
    # the directory was either none or not valid
    return False


def human_readable_boolean(answer: bool) -> str:
    """Produce a human-readable Yes or No for a boolean value of True or False."""
    # the provided answer is true
    if answer:
        return "Yes"
    # the provided answer is false
    return "No"


def get_default_directory_list() -> List[Path]:
    """Return the default directory list that is the current working directory by itself."""
    default_directory_list = [Path(".")]
    return default_directory_list


@cli.command()
def chasten(
    directory: List[Path] = typer.Option(
        get_default_directory_list(), "--directory", "-d", help="One or more directories with Python code"
    )
) -> None:
    """Analyze the AST of all of the Python files found through recursive traversal of directories."""
    # create a console for rich text output
    console = Console()
    # add extra space after the command to run the program
    console.print()
    # collect all of the directories that are invalid
    invalid_directories = []
    for current_directory in directory:
        if not confirm_valid_directory(current_directory):
            invalid_directories.append(current_directory)
    # create the list of valid directories by removing the invalid ones
    valid_directories = list(set(directory) - set(invalid_directories))
    console.print(valid_directories)
