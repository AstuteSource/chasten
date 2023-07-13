"""Chasten checks the AST of a Python program."""

from pathlib import Path
from typing import List

import typer
from pyastgrep import search as pyastgrepsearch  # type: ignore
from rich.console import Console
from trogon import Trogon  # type: ignore
from typer.main import get_group

from chasten import filesystem

# create a Typer object to support the command-line interface
cli = typer.Typer()


@cli.command()
def tui(ctx: typer.Context):
    """Interatively define command-line arguments through a terminal user interface."""
    Trogon(get_group(cli), click_context=ctx).run()


@cli.command()
def search(
    directory: List[Path] = typer.Option(
        filesystem.get_default_directory_list(),
        "--directory",
        "-d",
        help="One or more directories with Python code",
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
