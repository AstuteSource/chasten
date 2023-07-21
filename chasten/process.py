"""Analyze the abstract syntax and/or the search results."""

from typing import Any, List, Tuple, Union

from pyastgrep import search as pyastgrepsearch  # type: ignore


def filter_matches(
    match_list: List[Union[pyastgrepsearch.Match, Any]],
    data_type,
) -> Tuple[List[pyastgrepsearch.Match], List[Any]]:
    """Filter the list of matches based on the provided data type."""
    subset_match_list = []
    did_not_match_list = []
    for match in match_list:
        if isinstance(match, data_type):
            subset_match_list.append(match)
        else:
            did_not_match_list.append(match)
    return (subset_match_list, did_not_match_list)
