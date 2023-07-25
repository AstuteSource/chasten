"""Pytest test suite for the main module."""

from pathlib import Path

import pytest
from hypothesis import given, settings, strategies
from typer.testing import CliRunner

from chasten import main

runner = CliRunner()


def test_cli_analyze_correct_arguments(tmpdir):
    """Confirm that using the command-line interface does not crash: analyze command correct arguments."""
    # create some temporary directories
    test_one = tmpdir.mkdir("test_one")
    # call the analyze command
    project_name = "testing"
    result = runner.invoke(
        main.cli,
        [
            "analyze",
            "--search-directory",
            test_one,
            "--project-name",
            project_name,
            "--verbose",
        ],
    )
    assert result.exit_code == 0


def test_cli_analyze_incorrect_arguments_no_project(tmpdir):
    """Confirm that using the command-line interface does not crash: analyze command incorrect arguments."""
    # create some temporary directories
    test_one = tmpdir.mkdir("test_one")
    # call the analyze command
    result = runner.invoke(
        main.cli,
        [
            "analyze",
            "--search-directory",
            test_one,
            "--verbose",
        ],
    )
    # crashes because the command-line arguments are wrong
    assert result.exit_code != 0


def test_cli_analyze_incorrect_arguments_wrong_config(tmpdir):
    """Confirm that using the command-line interface does return non-zero: analyze command incorrect arguments."""
    # create some temporary directories
    test_one = tmpdir.mkdir("test_one")
    project_name = "test"
    # create a configuration directory
    # that does not currently exist
    wrong_config_dir = "config"
    # call the analyze command
    result = runner.invoke(
        main.cli,
        [
            "analyze",
            "--project-name",
            project_name,
            "--search-directory",
            test_one,
            "--config",
            wrong_config_dir,
            "--verbose",
        ],
    )
    assert result.exit_code == 1


def test_cli_analyze_incorrect_arguments_correct_config(tmpdir):
    """Confirm that using the command-line interface does return non-zero due to no files: analyze command correct arguments."""
    # create some temporary directories
    test_one = tmpdir.mkdir("test_one")
    project_name = "test"
    # create a configuration directory
    # that does currently exist
    correct_config_dir = tmpdir.mkdir("config")
    # call the analyze command
    result = runner.invoke(
        main.cli,
        [
            "analyze",
            "--project-name",
            project_name,
            "--search-directory",
            test_one,
            "--config",
            correct_config_dir,
            "--verbose",
        ],
    )
    assert result.exit_code == 1


@given(directory=strategies.builds(Path))
@settings(deadline=None)
@pytest.mark.fuzz
def test_fuzz_cli_analyze_single_directory(directory):
    """Confirm that the function does not crash when called through the command-line interface."""
    project_name = "testing"
    result = runner.invoke(
        main.cli,
        [
            "analyze",
            "--project-name",
            project_name,
            "--search-directory",
            str(directory),
        ],
    )
    assert result.exit_code == 0
