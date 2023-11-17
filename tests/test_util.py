"""Pytest test suite for the util module."""

import shutil

import pytest
from hypothesis import given, provisional
from hypothesis import strategies as st

from chasten import constants, util


def test_human_readable_boolean() -> None:
    """Use Hypothesis to confirm that the function does not crash."""
    assert util.get_human_readable_boolean(answer=True) == "Yes"
    assert util.get_human_readable_boolean(answer=False) == "No"


@given(answer=st.booleans())
@pytest.mark.fuzz
def test_fuzz_human_readable_boolean(answer: bool) -> None:
    """Use Hypothesis to confirm that the function does not crash."""
    util.get_human_readable_boolean(answer=answer)


@given(answer=st.booleans())
@pytest.mark.fuzz
def test_fuzz_human_readable_boolean_correct_string(answer: bool) -> None:
    """Use Hypothesis to confirm that the conversion to human-readable works."""
    str_answer = util.get_human_readable_boolean(answer=answer)
    if answer:
        assert str_answer == "Yes"
    else:
        assert str_answer == "No"

        
@given(url=provisional.urls())
@pytest.mark.fuzz
def test_is_url_correct(url: str) -> None:
    """Use Hypothesis to confirm that URLs are correctly recognized/unrecognized."""
    result = util.is_url(url=url)
    assert result is True

    
@given(check_status_list=st.lists(st.booleans()))
@pytest.mark.fuzz
def test_total_amount_passed(check_status_list: list[bool]):
    stats = util.total_amount_passed(check_status_list)

    assert constants.markers.Zero <= stats[2] <= constants.markers.Percent_Multiplier
    assert stats[0] <= stats[1]



OpSystem = util.get_OS()
datasette_exec = constants.datasette.Datasette_Executable


def test_executable_name() -> None:
    """Test if executable name gets correct file name"""
    # makes sure the datasette executable is where expected
    assert shutil.which(util.executable_name(datasette_exec, OpSystem))
    # makes sure the frogmouth executable is where expected
    assert shutil.which(util.executable_name("frogmouth", OpSystem))
