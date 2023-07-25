"""Pytest test suite for the filesystem module."""

import pathlib
from unittest.mock import patch

import pytest
from hypothesis import given, strategies
from rich.tree import Tree

from chasten import constants, filesystem


def test_valid_directory() -> None:
    """Confirm that a valid directory is found."""
    directory_str = "./tests/"
    directory = pathlib.Path(directory_str)
    confirmation = filesystem.confirm_valid_directory(directory)
    assert confirmation is True


def test_invalid_directory() -> None:
    """Confirm that a valid directory is found."""
    directory_str = "./testsNOT/"
    directory = pathlib.Path(directory_str)
    confirmation = filesystem.confirm_valid_directory(directory)
    assert confirmation is False


def test_valid_file() -> None:
    """Confirm that a valid directory is found."""
    file_str = "./tests/test_filesystem.py"
    this_file = pathlib.Path(file_str)
    confirmation = filesystem.confirm_valid_file(this_file)
    assert confirmation is True


def test_invalid_file() -> None:
    """Confirm that a valid directory is found."""
    file_str = "./tests/test_filesystemNOT.py"
    this_file_not = pathlib.Path(file_str)
    confirmation = filesystem.confirm_valid_file(this_file_not)
    assert confirmation is False


@given(directory=strategies.builds(pathlib.Path))
@pytest.mark.fuzz
def test_fuzz_confirm_valid_directory_using_builds(directory: pathlib.Path) -> None:
    """Confirm that the function does not crash."""
    filesystem.confirm_valid_directory(directory=directory)


@given(file=strategies.builds(pathlib.Path))
@pytest.mark.fuzz
def test_fuzz_confirm_valid_file_using_builds(file: pathlib.Path) -> None:
    """Confirm that the function does not crash."""
    filesystem.confirm_valid_file(file=file)


def test_create_directory_tree(tmpdir):
    """Confirm that creation of the textual directory tree works."""
    # create a temporary directory
    tmp_dir = pathlib.Path(tmpdir)
    # create some files and directories
    (tmp_dir / "file1.txt").touch()
    (tmp_dir / "subdir1").mkdir()
    (tmp_dir / "subdir2").mkdir()
    (tmp_dir / "subdir2" / "file2.txt").touch()
    # call the function under test
    tree = filesystem.create_directory_tree_visualization(tmp_dir)
    # confirm that the output is a rich tree object
    assert isinstance(tree, Tree)
    # confirm the directory name in root node
    assert tree.label == f":open_file_folder: {tmp_dir.as_posix()}"
    # confirm that the child nodes contain the expected dirs and files
    dirs = [node.label for node in tree.children if ":open_file_folder:" in node.label]  # type: ignore
    files = [node.label for node in tree.children if ":page_facing_up:" in node.label]  # type: ignore
    assert set(dirs) == {
        f":open_file_folder: {p.name}" for p in tmp_dir.iterdir() if p.is_dir()
    }
    assert set(files) == {
        f":page_facing_up: {p.name}" for p in tmp_dir.iterdir() if p.is_file()
    }


@given(directory=strategies.builds(pathlib.Path))
@pytest.mark.fuzz
def test_fuzz_create_directory_tree(directory):
    """Using Hypothesis to confirm that the file system directory tree creation works."""
    tree = filesystem.create_directory_tree_visualization(directory)
    # confirm that it is a rich tree object
    assert isinstance(tree, Tree)
    # confirm that it has the fully-qualified name as the main label
    assert tree.label == f":open_file_folder: {directory.as_posix()}"
    dirs = []
    files = []
    # build up a list of all of the directories and files
    for node in tree.children:
        if ":open_file_folder:" in node.label:  # type: ignore
            dirs.append(node.label[19:])  # type: ignore
        else:
            files.append(node.label[17:])  # type: ignore
    # confirm that it contains all of the directory and file names
    assert set(dirs) == set(p.name for p in directory.iterdir() if p.is_dir())
    assert set(files) == set(p.name for p in directory.iterdir() if p.is_file())


@patch("chasten.configuration.user_config_dir")
def test_create_config_dir_does_not_exist(mock_user_config_dir, tmp_path):
    """Confirm possible to create the user configuration directory when it does not exist."""
    # monkeypatch the platformdirs user_config_dir to always return
    # the tmpdir test fixture that is controlled by Pytest; the
    # directory inside of that will be ".chasten" by default
    mock_user_config_dir.return_value = str(tmp_path / ".chasten")
    dir_path = tmp_path / ".chasten"
    result = filesystem.create_configuration_directory()
    assert result == dir_path
    assert dir_path.exists()


@patch("chasten.configuration.user_config_dir")
def test_create_config_dir_already_exist_throw_exception(
    mock_user_config_dir, tmp_path
):
    """Confirm not possible to create the user configuration directory when it does exist."""
    # monkeypatch the platformdirs user_config_dir to always return
    # the tmpdir test fixture that is controlled by Pytest; the
    # directory inside of that will be ".chasten" by default
    mock_user_config_dir.return_value = str(tmp_path / ".chasten")
    dir_path = tmp_path / ".chasten"
    result = filesystem.create_configuration_directory()
    assert result == dir_path
    assert dir_path.exists()
    # confirm fails if called again without force
    with pytest.raises(FileExistsError):
        filesystem.create_configuration_directory(force=False)


@patch("chasten.configuration.user_config_dir")
def test_create_config_dir_already_exist_no_exception_when_no_force(
    mock_user_config_dir, tmp_path
):
    """Confirm possible to create the user configuration directory when it does not exist."""
    # monkeypatch the platformdirs user_config_dir to always return
    # the tmpdir test fixture that is controlled by Pytest; the
    # directory inside of that will be ".chasten" by default
    mock_user_config_dir.return_value = str(tmp_path / ".chasten")
    dir_path = tmp_path / ".chasten"
    result = filesystem.create_configuration_directory()
    assert result == dir_path
    assert dir_path.exists()
    # confirm that it fails if called again without force
    with pytest.raises(FileExistsError):
        filesystem.create_configuration_directory(force=False)


@patch("chasten.configuration.user_config_dir")
def test_create_config_dir_already_exist_no_exception_when_force(
    mock_user_config_dir, tmp_path
):
    """Confirm possible to create the user configuration directory when it does not exist."""
    # monkeypatch the platformdirs user_config_dir to always return
    # the tmpdir test fixture that is controlled by Pytest; the
    # directory inside of that will be ".chasten" by default
    mock_user_config_dir.return_value = str(tmp_path / ".chasten")
    dir_path = tmp_path / ".chasten"
    result = filesystem.create_configuration_directory()
    assert result == dir_path
    assert dir_path.exists()
    # confirm that it does not fail if called again with force
    filesystem.create_configuration_directory(force=True)


def test_detect_configuration_with_input_config_directory(tmp_path):
    """Confirm that it is possible to detect the configuration directory when it exists."""
    # detecting a configuration directory should happen with
    # the provided configuration directory over the platform-specific one
    config = tmp_path / "config"
    config.mkdir()
    assert filesystem.detect_configuration(config) == str(config)


@patch("chasten.configuration.user_config_dir")
def test_detect_configuration_with_input_config_directory_use_default(
    mock_user_config_dir, tmp_path
):
    """Confirm that it is possible to detect the configuration directory when none provided."""
    # monkeypatch the platformdirs user_config_dir to always return
    # the tmpdir test fixture that is controlled by Pytest; the
    # directory inside of that will be ".chasten" by default
    mock_user_config_dir.return_value = str(tmp_path / ".chasten")
    dir_path = tmp_path / ".chasten"
    result = filesystem.create_configuration_directory()
    assert result == dir_path
    assert dir_path.exists()
    detected_directory = filesystem.detect_configuration(None)
    assert detected_directory == str(dir_path)


@patch("chasten.configuration.user_config_dir")
def test_create_main_configuration_file(mock_user_config_dir, tmp_path):
    """Confirm that it is possible to create the main configuration file if it does not exist."""
    # monkeypatch the platformdirs user_config_dir to always return
    # the tmpdir test fixture that is controlled by Pytest; the
    # directory inside of that will be ".chasten" by default
    mock_user_config_dir.return_value = str(tmp_path / ".chasten")
    dir_path = tmp_path / ".chasten"
    result = filesystem.create_configuration_directory()
    assert result == dir_path
    assert dir_path.exists()
    # create the main configuration file
    filesystem.create_configuration_file(config=None, config_file_name=constants.filesystem.Main_Configuration_File)  # type: ignore
    # create the path to the main configuration file
    # and then assert that it exists and has correct content
    main_configuation_file = dir_path / "config.yml"
    assert main_configuation_file.exists()
    # confirm that the configuration file has correct text
    assert (
        main_configuation_file.read_text()
        == filesystem.CONFIGURATION_FILE_DEFAULT_CONTENTS
    )


@patch("chasten.configuration.user_config_dir")
def test_create_checks_configuration_file(mock_user_config_dir, tmp_path):
    """Confirm that it is possible to create the checks configuration file if it does not exist."""
    # monkeypatch the platformdirs user_config_dir to always return
    # the tmpdir test fixture that is controlled by Pytest; the
    # directory inside of that will be ".chasten" by default
    mock_user_config_dir.return_value = str(tmp_path / ".chasten")
    dir_path = tmp_path / ".chasten"
    result = filesystem.create_configuration_directory()
    assert result == dir_path
    assert dir_path.exists()
    # create the main configuration file
    filesystem.create_configuration_file(config=None, config_file_name=constants.filesystem.Main_Checks_File)  # type: ignore
    # create the path to the main configuration file
    # and then assert that it exists and has correct content
    main_configuation_file = dir_path / "checks.yml"
    assert main_configuation_file.exists()
    # confirm that the configuration file has correct text
    assert main_configuation_file.read_text() == filesystem.CHECKS_FILE_DEFAULT_CONTENTS
