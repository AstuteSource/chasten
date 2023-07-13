"""Pytest test suite for the main module."""

import typing
from pathlib import Path

import pytest
from hypothesis import given, strategies
from typer.testing import CliRunner

from chasten import main

runner = CliRunner()


def test_cli_search(tmpdir):
    """Confirm that using the command-line interface does not crash: search command."""
    # create some temporary directories
    test_one = tmpdir.mkdir("test_one")
    test_two = tmpdir.mkdir("test_two")
    # call the search command
    result = runner.invoke(
        main.cli, ["search", "--directory", test_one, "--directory", test_two]
    )
    assert result.exit_code == 0


@given(directory=strategies.lists(strategies.builds(Path), min_size=1, max_size=5))
@pytest.mark.hypothesis
def test_fuzz_search(directory: typing.List[Path]) -> None:
    """Confirm that the function does not crash when called directly."""
    main.search(directory=directory)


@given(directory=strategies.builds(Path))
@pytest.mark.hypothesis
def test_fuzz_cli_search_single_directory(directory):
    """Confirm that the function does not crash when called through the command-line interface."""
    result = runner.invoke(main.cli, ["search", "--directory", str(directory)])
    assert result.exit_code == 0


@given(directory_one=strategies.builds(Path), directory_two=strategies.builds(Path))
@pytest.mark.hypothesis
def test_fuzz_cli_search_multiple_directory(directory_one, directory_two):
    """Confirm that the function does not crash when called through the command-line interface."""
    result = runner.invoke(
        main.cli,
        [
            "search",
            "--directory",
            str(directory_one),
            "--directory",
            str(directory_two),
        ],
    )
    assert result.exit_code == 0
