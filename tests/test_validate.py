"""Pytest test suite for the validate module."""

import pytest
from hypothesis import given, strategies
from hypothesis_jsonschema import from_schema

from chasten.validate import JSON_SCHEMA, validate_main_configuration


def test_validate_config_valid_simple():
    """Confirm that validation with built-in schema works for a simple valid example."""
    valid_config_correct_schema = {"chasten": {"verbose": True, "debug-level": "ERROR"}}
    is_valid, errors = validate_main_configuration(valid_config_correct_schema)
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
    is_valid, errors = validate_main_configuration(valid_config_correct_schema)
    assert is_valid
    assert not errors


def test_validate_config_invalid_simple():
    """Confirm that validation with built-in schema does not work for a simple invalid example."""
    invalid_config_correct_schema = {"chasten": {"verbose": "yes"}}
    is_valid, errors = validate_main_configuration(invalid_config_correct_schema)
    assert not is_valid
    assert errors
    assert "is not of type" in errors


def test_validate_config_invalid_realistic():
    """Confirm that validation with built-in schema works for a realistic valid example."""
    valid_config_correct_schema = {
        "chasten": {
            "verbose": "yes",
            "debug-level": "ERROR",
            "debug-destination": "CONSOLE",
            "search-directory": [
                "/path/to/dir/f1",
                "/path/to/dir/f2",
                "/path/to/dir/f3",
            ],
        }
    }
    is_valid, errors = validate_main_configuration(valid_config_correct_schema)
    assert not is_valid
    assert errors
    assert "is not of type" in errors


@given(
    config=strategies.fixed_dictionaries({"chasten": strategies.fixed_dictionaries({})})
)
@pytest.mark.fuzz
def test_validate_empty_config(config):
    """Use Hypothesis to confirm that an empty configuration will validate."""
    is_valid, errors = validate_main_configuration(config)
    assert is_valid
    assert not errors


@given(
    config=strategies.fixed_dictionaries(
        {
            "chasten": strategies.fixed_dictionaries(
                {
                    "verbose": strategies.booleans(),
                }
            )
        }
    )
)
@pytest.mark.fuzz
def test_validate_config_with_verbose(config):
    """Use Hypothesis to confirm that a very simple valid schema will validate correctly."""
    is_valid, errors = validate_main_configuration(config)
    assert is_valid
    assert not errors


@given(
    config=strategies.fixed_dictionaries(
        {
            "chasten": strategies.fixed_dictionaries(
                {
                    "debug-level": strategies.sampled_from(["INFO", "WARNING"]),
                }
            )
        }
    )
)
@pytest.mark.fuzz
def test_validate_config_with_debug_level(config):
    """Use Hypothesis to confirm that a simple valid schema will validate correctly."""
    is_valid, errors = validate_main_configuration(config)
    assert is_valid
    assert not errors


@given(from_schema(JSON_SCHEMA))
@pytest.mark.fuzz
def test_integers(config):
    """Use Hypothesis and the JSON schema plugin to confirm validation works for all possible valid instances."""
    is_valid, errors = validate_main_configuration(config)
    assert is_valid
    assert not errors
