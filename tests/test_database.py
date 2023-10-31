"""Pytest test suite for the database module."""

from chasten import database
from chasten import filesystem
from chasten import util


def test_executable_name() -> None:
    assert filesystem.can_find_executable(
        database.executable_name(OpSystem=util.get_OS())
    )
