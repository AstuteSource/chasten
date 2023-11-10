import os
import pytest
from pathlib import Path
from chasten.createchecks import is_valid_api_key, generate_yaml_config

valid_api_key = os.getenv("API_KEY")
test_genscript = "Write: 'Hello, World'"
file_path = "test_checks.yml"