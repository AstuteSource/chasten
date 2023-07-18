"""Pytest test suite for the validate module."""

import pytest

from chasten.validate import validate_configuration


def test_validate_config_valid_simple():
    """Confirm that validation with built-in schema works for a simple valid example."""
    valid_config_correct_schema = {"chasten": {"verbose": True, "debug-level": "ERROR"}}
    is_valid, errors = validate_configuration(valid_config_correct_schema)
    assert is_valid
    assert not errors


def test_validate_config_valid_realistic():
    """Confirm that validation with built-in schema works for a realistic valid example."""
    valid_config_correct_schema = {
        "chasten": {
            "verbose": True,
            "debug-level": "ERROR",
            "debug-destination": "CONSOLE",
            "search-directory": [
                "/path/to/dir/f1",
                "/path/to/dir/f2",
                "/path/to/dir/f3",
            ],
        }
    }
    is_valid, errors = validate_configuration(valid_config_correct_schema)
    assert is_valid
    assert not errors


def test_validate_config_invalid_simple():
    """Confirm that validation with built-in schema does not work for a simple invalid example."""
    invalid_config_correct_schema = {"chasten": {"verbose": "yes"}}
    is_valid, errors = validate_configuration(invalid_config_correct_schema)
    assert not is_valid
    assert "is not of type" in errors
