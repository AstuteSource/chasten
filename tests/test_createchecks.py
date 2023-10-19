import openai
import pytest
from hypothesis import given, settings, strategies as st
from chasten.createchecks import generate_key, encrypt_key, decrypt_key, is_valid_api_key, get_user_api_key, load_user_api_key, generate_yaml_config
from pathlib import Path


API_KEY_FILE = "userapikey.txt"

valid_api_key = "your_valid_api_key_here"
invalid_api_key = "your_invalid_api_key_here"

@pytest.fixture
def setup_api_key_file():
    get_user_api_key(valid_api_key)
    yield

    with open(API_KEY_FILE, "w") as f:
        f.write("")

def test_generate_key():
    key = generate_key()
    assert key is not None
    assert isinstance(key, bytes)

def test_encrypt_decrypt_key():
    user_api_key = "your_api_key_here"
    key = generate_key()
    encrypted_key = encrypt_key(user_api_key, key)
    decrypted_key = decrypt_key(encrypted_key, key)
    assert user_api_key == decrypted_key

def test_is_valid_api_key():
    assert is_valid_api_key(valid_api_key)
    assert not is_valid_api_key(invalid_api_key)

@given(st.text())
@settings(max_examples=10)
def test_generate_key_property(input_string):
    key = generate_key()
    assert len(key) == 32

def test_load_user_api_key(setup_api_key_file):
    loaded_user_api_key = load_user_api_key(API_KEY_FILE)
    assert loaded_user_api_key == valid_api_key

def test_generate_yaml_config_creates_file():
    user_api_key = "your_valid_api_key_here"
    user_input = "Your test user input"

    generated_yaml = generate_yaml_config(user_api_key, user_input)

    assert Path("checks.yml").exists()
