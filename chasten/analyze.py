"""Analyze the abstract syntax and/or the search results."""

from typing import Any, List, Union

from pyastgrep import search as pyastgrepsearch


def filter_matches(
    match_list: List[Union[pyastgrepsearch.Match, Any]],
    data_type,
) -> List[pyastgrepsearch.Match]:
    """Filter the list of matches based on the provided data type."""
    subset_match_list = []
    for match in match_list:
        if isinstance(match, data_type):
            subset_match_list.append(match)
    return subset_match_list
