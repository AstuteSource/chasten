import os
import pytest
from hypothesis import given, strategies as st
from chasten.createchecks import (
    save_user_api_key,
    load_user_api_key,
    is_valid_api_key,
    generate_yaml_config,
)

api_key_strategy = st.text(min_size=1, max_size=51)


@given(api_key=api_key_strategy)
def test_save_and_load_user_api_key(api_key):
    api_key_file = "userapikey.txt"

    # Save the API key
    save_user_api_key(api_key)

    # Check if the file exists
    assert os.path.exists(api_key_file)

    # Load the API key
    loaded_api_key = load_user_api_key(api_key_file)

    # Check if the loaded key matches the original key
    assert loaded_api_key == api_key


@given(api_key=api_key_strategy)
def test_is_valid_api_key(api_key):
    assert is_valid_api_key(api_key) is True


@given(
    api_key=load_user_api_key("userapikey.txt"),
    user_input=st.text(min_size=1, max_size=100),
)
def test_generate_yaml_config(api_key, user_input):
    generate_yaml_config(api_key, user_input)

    # Ensure the file was created
    generated_yaml_file = "generated_checks.yml"
    assert os.path.exists(generated_yaml_file)
