"""Pytest test suite for the main module."""

import typing
from pathlib import Path

import pytest
from hypothesis import given, strategies

from chasten import main


@given(directory=strategies.lists(strategies.builds(Path), min_size=1, max_size=5))
@pytest.mark.hypothesis
def test_fuzz_search(directory: typing.List[Path]) -> None:
    """Confirm that the function does not crash."""
    main.search(directory=directory)
