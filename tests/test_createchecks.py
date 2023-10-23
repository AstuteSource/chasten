import pytest
from hypothesis import given, strategies as st
from chasten.createchecks import is_valid_api_key, API_KEY_FILE

api_key_strategy = st.text(min_size=1, max_size=50)


def test_save_and_load_user_api_key():
    assert API_KEY_FILE.exists()


@given(api_key=api_key_strategy)
def test_is_valid_api_key(api_key):
    assert is_valid_api_key(api_key) is True


def test_generate_yaml_config():
    generated_yaml_file = "generated_checks.yml"
    assert generated_yaml_file.exists()
