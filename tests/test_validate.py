"""Pytest test suite for the validate module."""

import pytest
from hypothesis import HealthCheck, given, settings, strategies
from hypothesis_jsonschema import from_schema

from chasten.validate import JSON_SCHEMA_CONFIG
from chasten.validate import validate_configuration


def test_validate_config_valid_realistic():
    """Confirm that validation with built-in schema works for a realistic valid example."""
    valid_config_correct_schema = {
        "chasten": {
            "checks-file": ["checks.yml"],
        }
    }
    is_valid, errors = validate_configuration(valid_config_correct_schema)
    assert is_valid
    assert not errors


def test_validate_config_invalid_realistic():
    """Confirm that validation with built-in schema works for a realistic valid example."""
    valid_config_correct_schema = {
        "chasten": {
            "checks-file": "checks.yml",
        }
    }
    is_valid, errors = validate_configuration(valid_config_correct_schema)
    assert not is_valid
    assert errors
    assert "is not of type" in errors


@given(
    config=strategies.fixed_dictionaries({"chasten": strategies.fixed_dictionaries({})})
)
@pytest.mark.fuzz
def test_validate_empty_config(config):
    """Use Hypothesis to confirm that an empty configuration will validate."""
    is_valid, errors = validate_configuration(config)
    assert is_valid
    assert not errors


@given(from_schema(JSON_SCHEMA_CONFIG))
@settings(suppress_health_check=[HealthCheck.too_slow])
@pytest.mark.fuzz
def test_integers(config):
    """Use Hypothesis and the JSON schema plugin to confirm validation works for all possible valid instances."""
    is_valid, errors = validate_configuration(config)
    assert is_valid
    assert not errors
