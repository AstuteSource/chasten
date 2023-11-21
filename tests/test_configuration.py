"""Pytest test suite for the configuration module."""

import logging

import pytest
from hypothesis import given
from hypothesis import strategies

from chasten import configuration


@given(applicationname=strategies.text(), applicationauthor=strategies.text())
@pytest.mark.fuzz
def test_fuzz_create_use_config_dir(
    applicationname: str, applicationauthor: str
) -> None:
    """Use Hypothesis to confirm that the function does not crash and produces directory with the application name."""
    user_config_dir_str = configuration.user_config_dir(
        applicationname, applicationauthor
    )
    assert user_config_dir_str
    assert applicationname in user_config_dir_str


@given(
    debug_level=strategies.sampled_from(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    ),
    debug_dest=strategies.sampled_from(["CONSOLE", "SYSLOG"]),
)
@pytest.mark.fuzz
def test_fuzz_configure_logging(debug_level, debug_dest):
    """Use Hypothesis to confirm that the function does not crash and always produces logger with valid data."""
    logger, created = configuration.configure_logging(debug_level, debug_dest)
    assert logger
    assert created
    assert isinstance(logger, logging.Logger)


@given(
    debug_level=strategies.sampled_from(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    ),
    debug_dest=strategies.sampled_from(["CONSOLE-WRONG", "SYSLOG-WRONG"]),
)
@pytest.mark.fuzz
def test_fuzz_configure_logging_incorrect_inputs(debug_level, debug_dest):
    """Use Hypothesis to confirm that the function does not crash and always produces logger with valid data."""
    logger, created = configuration.configure_logging(debug_level, debug_dest)
    assert logger
    assert not created
    assert isinstance(logger, logging.Logger)
