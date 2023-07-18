"""Pytest test suite for the debug module."""

import pytest

from chasten.debug import DebugDestination, DebugLevel


def test_debug_level_values():
    assert DebugLevel.DEBUG == "DEBUG"
    assert DebugLevel.INFO == "INFO"
    assert DebugLevel.WARNING == "WARNING"
    assert DebugLevel.ERROR == "ERROR"
    assert DebugLevel.CRITICAL == "CRITICAL"


def test_debug_level_isinstance():
    assert isinstance(DebugLevel.DEBUG, DebugLevel)


def test_debug_level_iteration():
    assert list(DebugLevel) == ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def test_debug_destination_values():
    assert DebugDestination.CONSOLE == "CONSOLE"
    assert DebugDestination.SYSLOG == "SYSLOG"


def test_debug_destination_iteration():
    assert list(DebugDestination) == ["CONSOLE", "SYSLOG"]


def test_debug_destination_invalid():
    with pytest.raises(ValueError):
        DebugDestination("INVALID")
