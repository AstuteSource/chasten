import pathlib

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from chasten import configApp, constants

# Define an alphabet of characters for generating random test data
ALPHABET = "0123456789!@#$%^&*()_+-=[]|:;'<>.?/~`AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"

# Define a constant for app storage
CHECK_STORAGE = constants.chasten.App_Storage

# Define a list of CSV data for testing
CSV_CHECK_LIST = [
    ["for loop", "2", "True"],
    ["while loop", "3", "False"],
    ["function", "1", "False"],
    ["assert statement", "1", "True"],
]

# Define a string with default check data
CHECK_TEST_DEFAULT = """
for loop,2,True
while loop,3,False
function,1,False
assert statement,1,True
"""


# Test to check if the 'write_checks' function correctly converts CSV data to a formatted string
def test_write_checks():
    """Test the write_checks function by converting CSV data to a formatted string."""
    expected_check = "Make a YAML file that checks for:\n - exactly 2 for loop\n - at minimum 3 while loop\n - at minimum 1 function\n - exactly 1 assert statement"
    assert configApp.write_checks(CSV_CHECK_LIST) == expected_check


# Test to check the handling of an empty input list by the 'write_checks' function
def test_write_checks_empty_file():
    """Test the write_checks function when list is empty"""
    assert configApp.write_checks([]) == "[red][ERROR][/red] No checks were supplied"


# Test to check if the 'split_file' function correctly parses a file with check data
def test_split_file(tmpdir):
    """Test the split_file function by parsing check data from a file."""
    tmp_dir = pathlib.Path(tmpdir)
    file = tmp_dir / "check_test.txt"
    file.touch()
    file.write_text(CHECK_TEST_DEFAULT)
    assert configApp.split_file(file) == CSV_CHECK_LIST


# Property-based test to check if the 'store_in_file' function correctly stores generated data in a file
@given(
    Pattern=st.text(alphabet=ALPHABET, min_size=3, max_size=150),
    Matches=st.integers(min_value=1, max_value=500),
    Exact=st.booleans(),
)
@pytest.mark.fuzz
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_store_in_file(Pattern, Matches, Exact, tmpdir):
    """Tests if the store_in_file function correctly stores data in a file."""
    tmp_dir = pathlib.Path(tmpdir)
    file = tmp_dir / "check_test.txt"
    file.touch()
    # Call the 'store_in_file' function with generated data and check if it's stored in the file
    configApp.store_in_file(file, Pattern, Matches, Exact)
    assert f"\n{Pattern},{Matches},{Exact}" in file.read_text("utf-8")
