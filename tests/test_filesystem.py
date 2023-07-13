"""Pytest test suite for the filesystem module."""

import pathlib

import pytest
from hypothesis import given, strategies

from chasten import filesystem


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
@pytest.mark.hypothesis
def test_fuzz_confirm_valid_directory_using_builds(directory: pathlib.Path) -> None:
    """Confirm that the function does not crash."""
    filesystem.confirm_valid_directory(directory=directory)


@given(file=strategies.builds(pathlib.Path))
@pytest.mark.hypothesis
def test_fuzz_confirm_valid_file_using_builds(file: pathlib.Path) -> None:
    """Confirm that the function does not crash."""
    filesystem.confirm_valid_file(file=file)
