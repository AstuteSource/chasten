"""Pytest test suite for the main module."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from hypothesis import HealthCheck, given, settings, strategies
from typer.testing import CliRunner

from chasten import main

runner = CliRunner()


@pytest.fixture
def cwd():
    """Define a test fixture for the current working directory."""
    return os.getcwd()


def test_cli_analyze_correct_arguments(cwd, tmpdir):
    """Confirm that using the command-line interface does not crash: analyze command with correct arguments."""
    # create some temporary directories
    test_one = tmpdir.mkdir("test_one")
    # call the analyze command
    project_name = "testing"
    # create a reference to the internal
    # .chasten directory that supports testing
    configuration_directory = str(cwd) + "/.chasten"
    result = runner.invoke(
        main.cli,
        [
            "analyze",
            "--search-directory",
            test_one,
            "--project-name",
            project_name,
            "--config",
            configuration_directory,
            "--verbose",
        ],
    )
    assert result.exit_code == 0


def test_cli_analyze_incorrect_arguments_no_project(cwd, tmpdir):
    """Confirm that using the command-line interface does not crash: analyze command incorrect arguments."""
    # create some temporary directories
    test_one = tmpdir.mkdir("test_one")
    # create a reference to the internal
    # .chasten directory that supports testing
    configuration_directory = str(cwd) + "/.chasten"
    # call the analyze command
    result = runner.invoke(
        main.cli,
        [
            "analyze",
            "--search-directory",
            test_one,
            "--config",
            configuration_directory,
            "--verbose",
        ],
    )
    # crashes because the command-line arguments are wrong
    print(result.output)
    assert result.exit_code != 0
    assert "Missing option" in result.output
    assert "--project-name" in result.output


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
    assert "Cannot perform analysis due to configuration" in result.output


def test_cli_analyze_incorrect_arguments_wrong_source_directory(tmpdir):
    """Confirm that using the command-line interface does return non-zero: analyze command incorrect arguments."""
    # create some temporary directories
    _ = tmpdir.mkdir("test_one")
    test_one_incorrect_name = "test_oneFF"
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
            test_one_incorrect_name,
            "--config",
            wrong_config_dir,
            "--verbose",
        ],
    )
    assert result.exit_code == 1
    assert "Cannot perform analysis due to configuration" in result.output


def test_cli_analyze_incorrect_arguments_correct_config(tmpdir):
    """Confirm that using the command-line interface does return non-zero due to no config files: analyze command correct arguments."""
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
    assert "Cannot perform analysis due to configuration" in result.output


@patch("chasten.configuration.user_config_dir")
def test_cli_configure_create_config_when_does_not_exist(
    mock_user_config_dir, tmp_path
):
    """Confirm that using the command-line interface does create .config directory when it does not exist."""
    # monkeypatch the platformdirs user_config_dir to always return
    # the tmpdir test fixture that is controlled by Pytest; the
    # directory inside of that will be ".chasten" by default
    mock_user_config_dir.return_value = str(tmp_path / ".chasten")
    # call the configure command
    result = runner.invoke(
        main.cli,
        [
            "configure",
            "create",
            "--verbose",
        ],
    )
    assert result.exit_code == 0


@patch("chasten.configuration.user_config_dir")
def test_cli_configure_cannot_create_config_when_does_exist(
    mock_user_config_dir, tmp_path
):
    """Confirm that using the command-line interface does create .config directory when it does exist."""
    # monkeypatch the platformdirs user_config_dir to always return
    # the tmpdir test fixture that is controlled by Pytest; the
    # directory inside of that will be ".chasten" by default
    mock_user_config_dir.return_value = str(tmp_path / ".chasten")
    config_directory = Path(tmp_path / ".chasten")
    config_directory.mkdir()
    assert config_directory.exists()
    # call the configure command
    result = runner.invoke(
        main.cli,
        [
            "configure",
            "create",
            "--verbose",
        ],
    )
    assert result.exit_code == 1


@given(directory=strategies.builds(Path))
@settings(deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@pytest.mark.fuzz
def test_fuzz_cli_analyze_single_directory(cwd, directory):
    """Confirm that the function does not crash when called through the command-line interface."""
    project_name = "testing"
    # create a reference to the internal
    # .chasten directory that supports testing
    configuration_directory = str(cwd) + "/.chasten"
    result = runner.invoke(
        main.cli,
        [
            "analyze",
            "--project-name",
            project_name,
            "--config",
            configuration_directory,
            "--search-directory",
            str(directory),
        ],
    )
    assert result.exit_code == 0
