"""Pytest test suite for the database module."""

import pytest

from chasten import database, filesystem, util


@pytest.mark.fuzz
def test_executable_name() -> None:
    assert filesystem.can_find_executable(
        database.executable_name(OpSystem=util.get_OS())
    )
