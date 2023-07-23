"""Analyze the abstract syntax tree, its XML-based representation, and/or the search results."""

from typing import Any, Dict, List, Tuple, Union

from pyastgrep import search as pyastgrepsearch  # type: ignore
from thefuzz import fuzz

from chasten import constants, enumerations, output


def include_checks(
    checks: Union[List[Dict[str, Dict[str, Any]]], Any],
    check_include_attribute: enumerations.FilterableAttribute,
    check_include_match: str,
    check_include_confidence: int = constants.checks.Check_Confidence,
) -> List[Dict[str, Dict[str, Any]]]:
    """Perform all of the includes and excludes for the list of checks."""
    filtered_checks = []
    # at least one aspect of the inputs was not specified (likely due to
    # the fact that the command-line argument(s) were not used) and thus
    # there is no filtering that should take place; return the input
    if not check_include_attribute or not check_include_match:
        return filtered_checks
    # the function's inputs are valid and so perform the filtering
    for check in checks:
        # extract the contents of the requested attribute for inclusion
        check_requested_include_attribute = check[check_include_attribute]
        # compute the fuzzy match value for the specific:
        # --> requested include attribute
        # --> specified match string
        fuzzy_include_value = fuzz.ratio(
            check_include_match, check_requested_include_attribute
        )
        output.console.print(fuzzy_include_value)
        # include the check if the fuzzy inclusion value is above the default threshold
        if fuzzy_include_value >= check_include_confidence:
            filtered_checks.append(check)
    return filtered_checks


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
