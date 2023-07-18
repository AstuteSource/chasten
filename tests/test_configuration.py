"""Pytest test suite for the configuration module."""

import pytest
from hypothesis import given, strategies

from chasten import configuration


@given(applicationname=strategies.text(), applicationauthor=strategies.text())
@pytest.mark.fuzz
def test_fuzz_create_use_config_dir(applicationname: str, applicationauthor: str) -> None:
    """Use Hypothesis to confirm that the function does not crash and produces directory with the application name."""
    user_config_dir_str = configuration.user_config_dir(applicationname, applicationauthor)
    print(user_config_dir_str)
    assert user_config_dir_str
    assert applicationname in user_config_dir_str
