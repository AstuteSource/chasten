"""Pytest test suite for the util module."""

import pytest
from hypothesis import given
from hypothesis import provisional
from hypothesis import strategies

from chasten import util


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


@given(url=provisional.urls())
@pytest.mark.fuzz
def test_is_url_correct(url: str) -> None:
    """Use Hypothesis to confirm that URLs are correctly recognized/unrecognized."""
    result = util.is_url(url=url)
    assert result == True
