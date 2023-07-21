"""Pytest test suite for the analyze module."""

from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pyastgrep import search as pyastgrepsearch

from chasten import analyze


@given(
    match_list=st.lists(
        st.one_of(
            st.just(
                pyastgrepsearch.Match(
                    path=Path("."),
                    file_lines=None,  # type: ignore
                    xml_element=None,
                    position=None,  # type: ignore
                    ast_node=None,  # type: ignore
                )
            ),
            st.none(),
        )
    ),
    data_type=st.just(pyastgrepsearch.Match),
)
@pytest.mark.fuzz
def test_filter_matches(match_list, data_type):
    """Use Hypothesis to confirm that filtering always gets the Match objects."""
    filtered = analyze.filter_matches(match_list, data_type)
    assert all(isinstance(m, pyastgrepsearch.Match) for m in filtered)
    assert set(filtered) == set(
        m for m in match_list if isinstance(m, pyastgrepsearch.Match)
    )


@given(match_list=st.lists(st.integers()))
@pytest.mark.fuzz
def test_filter_matches_no_matches(match_list):
    """Use Hypothesis to confirm that filtering does not select a Match when there are none."""
    data_type = pyastgrepsearch.Match
    filtered = analyze.filter_matches(match_list, data_type)
    assert filtered == []


@given(match_list=st.lists(st.integers()), data_type=st.just(int))
@pytest.mark.fuzz
def test_filter_matches_only_int_matches(match_list, data_type):
    """Use Hypothesis to confirm that filtering works for integers."""
    filtered = analyze.filter_matches(match_list, data_type)
    if match_list == []:
        assert filtered == []
    else:
        assert filtered != []
