import pytest
import os

def test_load_user_api_key():
    key_file_path = "userapikey.txt"
    assert os.path.exists(key_file_path)  # Check if the key file exists

    with open(key_file_path, "w") as f:
        f.write("example_api_key")  # Create a sample key for the test

    # Verify that the load_user_api_key function can correctly load the key
    loaded_key = load_user_api_key(key_file_path)
    assert loaded_key == "example_api_key"  # Replace with the expected API key

def test_check_yml_exist():
    yml_file_path = "checks.yml"
    assert os.path.exists(yml_file_path)  # Check if the YAML file exists

    # You can add further checks here if needed, such as validating the content of the YAML file
