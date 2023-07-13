"""Pytest test suite for the filesystem module."""

import pathlib

import pytest
from hypothesis import given, strategies

from chasten import filesystem


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
