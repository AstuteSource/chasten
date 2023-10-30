"""Pytest test suite for the util module."""

import shutil

import pytest
from hypothesis import given, strategies

from chasten import constants, util


def test_human_readable_boolean() -> None:
    """Use Hypothesis to confirm that the function does not crash."""
    assert util.get_human_readable_boolean(answer=True) == "Yes"
    assert util.get_human_readable_boolean(answer=False) == "No"


@given(answer=strategies.booleans())
@pytest.mark.fuzz
def test_fuzz_human_readable_boolean(answer: bool) -> None:
    """Use Hypothesis to confirm that the function does not crash."""
    util.get_human_readable_boolean(answer=answer)


@given(answer=strategies.booleans())
@pytest.mark.fuzz
def test_fuzz_human_readable_boolean_correct_string(answer: bool) -> None:
    """Use Hypothesis to confirm that the conversion to human-readable works."""
    str_answer = util.get_human_readable_boolean(answer=answer)
    if answer:
        assert str_answer == "Yes"
    else:
        assert str_answer == "No"


OpSystem = util.get_OS()
datasette_exec = constants.datasette.Datasette_Executable


def test_executable_name() -> None:
    """Test if executable name gets correct file name"""
    # makes sure the executable is where expected
    assert shutil.which(util.executable_name(datasette_exec, OpSystem))
    # makes sure the executable is where expected
    assert shutil.which(util.executable_name("frogmouth", OpSystem))
