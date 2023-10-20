import pytest
from hypothesis import given
from hypothesis import strategies as st
from pathlib import Path
import os

def test_load_user_api_key(key):
    assert os.path.exists("userapikey.txt")

def test_check_yml_exist():
    assert os.path.exists("checks.yml")
