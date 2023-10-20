import pytest
from hypothesis import given
from hypothesis import strategies as st
from pathlib import Path
import os

from chasten.createchecks import generate_key, encrypt_key, decrypt_key, is_valid_api_key, get_user_api_key, load_user_api_key

# Define a valid API key for testing
VALID_API_KEY = "your_api_key_here"  # Replace with a valid API key for testing

@pytest.fixture
def key():
    return generate_key()

@pytest.fixture
def invalid_key():
    return "invalid_key"  # A known invalid key for testing

@given(st.text())
def test_encrypt_decrypt_key(key, text):
    encrypted_key = encrypt_key(VALID_API_KEY, key)
    decrypted_key = decrypt_key(encrypted_key, key)
    assert decrypted_key == VALID_API_KEY

def test_generate_key(key):
    assert key is not None

def test_is_valid_api_key():
    assert is_valid_api_key(VALID_API_KEY) is True
    assert is_valid_api_key("invalid_key") is False

def test_get_user_api_key(key):
    get_user_api_key(VALID_API_KEY)
    loaded_api_key = load_user_api_key("userapikey.txt")
    assert loaded_api_key == VALID_API_KEY

def test_files_exist():
    assert os.path.exists("userapikey.txt")
    assert os.path.exists("checks.yml")
    # Clean up files after testing
    os.remove("userapikey.txt")
    os.remove("checks.yml")
