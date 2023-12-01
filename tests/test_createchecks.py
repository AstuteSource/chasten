import os
from pathlib import Path

import pytest

from chasten.createchecks import generate_yaml_config
from chasten.createchecks import is_valid_api_key


def get_valid_api_key():
    """Retrive and return api key from env variable"""
    return os.getenv("API_KEY")


@pytest.mark.api
def test_valid_api_key():
    """Test is_valid_api_key function with a valid api key."""
    valid_api_key = get_valid_api_key()
    if not valid_api_key:
        pytest.skip("No valid API key found in the environment variables")

    result = is_valid_api_key(valid_api_key)
    assert result is True


@pytest.mark.api
def test_invalid_api_key():
    """Test is_valid_api_key function with an invalid api key."""
    invalid_api_key = "fk-561sf56a1sf561as5f1asf165as1"
    result = is_valid_api_key(invalid_api_key)
    assert result is False


@pytest.mark.api
def test_generate_yaml_config():
    valid_api_key = get_valid_api_key()
    test_genscript = "Write: 'Hello, World'"
    file_path = "test_checks.yml"

    if not valid_api_key:
        pytest.skip("No valid API key found in the environment variables")

    file_path = Path(file_path)

    result = generate_yaml_config(file_path, valid_api_key, test_genscript)

    assert result is not None
    assert file_path.is_file()

    # Check the content of the generated file
    with open(file_path, "r") as f:
        content = f.read()
        assert "Hello, World" in content
