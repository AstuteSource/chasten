"""Pytest test suite for the debug module."""

import pytest

from chasten.debug import DebugDestination, DebugLevel


def test_debug_level_values():
    """Confirm that all of the enumeration values are correct."""
    assert DebugLevel.DEBUG == "DEBUG"
    assert DebugLevel.INFO == "INFO"
    assert DebugLevel.WARNING == "WARNING"
    assert DebugLevel.ERROR == "ERROR"
    assert DebugLevel.CRITICAL == "CRITICAL"


def test_debug_level_isinstance():
    """Confirm that all of the individual levels are of the correct type."""
    assert isinstance(DebugLevel.DEBUG, DebugLevel)
    assert isinstance(DebugLevel.INFO, DebugLevel)
    assert isinstance(DebugLevel.WARNING, DebugLevel)
    assert isinstance(DebugLevel.ERROR, DebugLevel)
    assert isinstance(DebugLevel.CRITICAL, DebugLevel)


def test_debug_level_iteration():
    """Confirm that it is possible to list all of the possible values."""
    assert list(DebugLevel) == ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def test_debug_destination_values():
    """Confirm that all of the enumeration values are correct."""
    assert DebugDestination.CONSOLE == "CONSOLE"
    assert DebugDestination.SYSLOG == "SYSLOG"


def test_debug_destination_isinstance():
    """Confirm that all of the individual levels are of the correct type."""
    assert isinstance(DebugDestination.CONSOLE, DebugDestination)
    assert isinstance(DebugDestination.SYSLOG, DebugDestination)


def test_debug_destination_iteration():
    """Confirm that it is possible to list all of the possible valuers."""
    assert list(DebugDestination) == ["CONSOLE", "SYSLOG"]


def test_level_destination_invalid():
    """Confirm that invalid values raise a ValueError."""
    with pytest.raises(ValueError):
        DebugLevel("INVALID")


def test_debug_destination_invalid():
    """Confirm that invalid values raise a ValueError."""
    with pytest.raises(ValueError):
        DebugDestination("INVALID")
