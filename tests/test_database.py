"""Pytest test suite for the database module."""

import pytest
import os

from chasten import database
from hypothesis import strategies as st
from hypothesis import given


def test_create_chasten_view():
	"""Confirm that the function creating and viewing an example database does not crash"""
	# define the variable name for the example database
	chasten_database_name: str = ".example_database"
	# create the database with example name
	# run the view command with a set SQL query
	database.create_chasten_view(chasten_database_name)
	# remove the example variable made
	os.remove(".example_database")
