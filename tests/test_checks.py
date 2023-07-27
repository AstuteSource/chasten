"""Pytest test suite for the checks module."""

import hypothesis.strategies as st
import pytest
from hypothesis import given

from chasten.checks import extract_min_max


@given(st.dictionaries(st.text(), st.integers()))
@pytest.mark.fuzz
def test_extract_min_max_hypothesis(check):
    """Use Hypothesis to confirm that extract works correctly."""
    min_count, max_count = extract_min_max(check)
    assert isinstance(min_count, int) or min_count is None
    assert isinstance(max_count, int) or max_count is None


def test_extract_min_max():
    """Confirm that it is possible to extract both values from the count parmeter when it exists."""
    check = {"name": "test", "count": {"min": 1, "max": 10}}
    min_count, max_count = extract_min_max(check)
    assert min_count == 1
    assert max_count == 10  # noqa


def test_extract_max():
    """Confirm that it is possible to extract one value from the count parmeter when it exists."""
    check = {"name": "test", "count": {"max": 10}}
    min_count, max_count = extract_min_max(check)
    assert min_count is None
    assert max_count == 10  # noqa


def test_extract_min():
    """Confirm that it is possible to extract one value from the count parmeter when it exists."""
    check = {
        "name": "test",
        "count": {
            "min": 1,
        },
    }
    min_count, max_count = extract_min_max(check)
    assert min_count == 1
    assert max_count is None


def test_extract_min_max_missing():
    """Confirm that it is not possible to extract both values when they do not exist."""
    check = {"name": "test"}
    min_count, max_count = extract_min_max(check)  # type: ignore
    assert min_count is None
    assert max_count is None
