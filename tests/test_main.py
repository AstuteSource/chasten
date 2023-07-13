"""Pytest test suite for the main module."""

import pathlib
import typing

from hypothesis import given
from hypothesis import strategies as st

import chasten.main


@given(directory=st.from_type(pathlib.Path))
def test_fuzz_confirm_valid_directory(directory: pathlib.Path) -> None:
    """Confirm that the function does not crash."""
    chasten.main.confirm_valid_directory(directory=directory)


@given(file=st.from_type(pathlib.Path))
def test_fuzz_confirm_valid_file(file: pathlib.Path) -> None:
    """Confirm that the function does not crash."""
    chasten.main.confirm_valid_file(file=file)


@given(answer=st.booleans())
def test_fuzz_human_readable_boolean(answer: bool) -> None:
    """Confirm that the function does not crash."""
    chasten.main.human_readable_boolean(answer=answer)


@given(directory=st.from_type(typing.List[pathlib.Path]))
def test_fuzz_search(directory: typing.List[pathlib.Path]) -> None:
    """Confirm that the function does not crash."""
    chasten.main.search(directory=directory)
