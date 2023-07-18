"""Pytest test suite for the main module."""

import typing
from pathlib import Path

import pytest
from hypothesis import given, strategies
from typer.testing import CliRunner

from chasten import debug, main

runner = CliRunner()


def test_cli_analyze(tmpdir):
    """Confirm that using the command-line interface does not crash: analyze command."""
    # create some temporary directories
    test_one = tmpdir.mkdir("test_one")
    test_two = tmpdir.mkdir("test_two")
    # call the analyze command
    result = runner.invoke(
        main.cli,
        ["analyze", "--search-directory", test_one, "--search-directory", test_two],
    )
    assert result.exit_code == 0


@given(directory=strategies.lists(strategies.builds(Path), min_size=1, max_size=5))
@pytest.mark.fuzz
def test_fuzz_analyze(directory: typing.List[Path]) -> None:
    """Confirm that the function does not crash when called directly."""
    # need to pass all of the command-line arguments because otherwise
    # the default values are set as a typer.Option and not converted to
    # the actual enums that are normally manipulated after input to the CLI
    main.analyze(
        directory=directory,
        debug_level=debug.DebugLevel.ERROR,
        debug_destination=debug.DebugDestination.CONSOLE,
    )


@given(directory=strategies.builds(Path))
@pytest.mark.fuzz
def test_fuzz_cli_analyze_single_directory(directory):
    """Confirm that the function does not crash when called through the command-line interface."""
    result = runner.invoke(main.cli, ["analyze", "--search-directory", str(directory)])
    assert result.exit_code == 0


@given(directory_one=strategies.builds(Path), directory_two=strategies.builds(Path))
@pytest.mark.fuzz
def test_fuzz_cli_analyze_multiple_directory(directory_one, directory_two):
    """Confirm that the function does not crash when called through the command-line interface."""
    result = runner.invoke(
        main.cli,
        [
            "analyze",
            "--search-directory",
            str(directory_one),
            "--search-directory",
            str(directory_two),
        ],
    )
    assert result.exit_code == 0
