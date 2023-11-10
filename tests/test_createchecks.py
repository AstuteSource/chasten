import os
import pytest
from pathlib import Path
from chasten.createchecks import is_valid_api_key, generate_yaml_config

valid_api_key = os.getenv("API_KEY")
test_genscript = "Write: 'Hello, World'"
file_path = "test_checks.yml"

def test_valid_api_key():
    """Test is_valid_api_key function with a valid api key."""
    global valid_api_key
    if not valid_api_key:
        pytest.skip("No valid API key found in the environment variables")

    result = is_valid_api_key(valid_api_key)
    assert result is True