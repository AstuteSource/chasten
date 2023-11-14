# pylint: skip-file
from chasten.createchecks import is_valid_api_key, generate_yaml_config
from pathlib import Path
import pytest
import os


valid_api_key = os.getenv("OPEN_AI_KEY")
test_genscript = "Write: 'Hello, World'"
file_path = "test_checks.yml"


def test_valid_api_key():
    """Test is_valid_api_key function with a valid api key."""
    global valid_api_key
    if not valid_api_key:
        pytest.skip("No valid API key found in the environment variables")

    result = is_valid_api_key(valid_api_key)
    assert result is True


def test_invalid_api_key():
    """Test is_valid_api_key function with an invalid api key."""
    invalid_api_key = "fk-561sf56a1sf561as5f1asf165as1"
    result = is_valid_api_key(invalid_api_key)
    assert result is False


def test_generate_yaml_config():
    global valid_api_key, test_genscript, file_path

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
