"""Analyze the abstract syntax tree, its XML-based representation, and/or the search results."""

from typing import Any, Dict, List, Tuple, Union

from pyastgrep import search as pyastgrepsearch  # type: ignore
from thefuzz import fuzz  # type: ignore

from chasten import constants, enumerations


def include_or_exclude_checks(
    checks: List[Dict[str, Union[str, Dict[str, int]]]],
    check_attribute: enumerations.FilterableAttribute,
    check_match: str,
    check_confidence: int = constants.checks.Check_Confidence,
    include: bool = True,
) -> List[Dict[str, Union[str, Dict[str, int]]]]:
    """Perform all of the includes and excludes for the list of checks."""
    filtered_checks = []
    # at least one aspect of the inputs was not specified (likely due to
    # the fact that the command-line argument(s) were not used) and thus
    # there is no filtering that should take place; return the input
    if check_attribute is None or check_match is None:
        return checks
    # the function's inputs are valid and so perform the filtering
    for check in checks:
        # extract the contents of the requested attribute for inclusion
        check_requested_include_attribute = check[check_attribute]
        # compute the fuzzy match value for the specific:
        # --> requested include attribute
        # --> specified match string
        fuzzy_value = fuzz.ratio(check_match, check_requested_include_attribute)
        # include the check if the fuzzy inclusion value is above (or equal to) threshold
        # and the purpose of the function call is to include values
        if (fuzzy_value >= check_confidence) and include:
            filtered_checks.append(check)
        # include the check if the fuzzy inclusion value is below threshold
        # and the purpose of the function call is to exclude values;
        # note that not including a value means that it excludes
        elif (fuzzy_value < check_confidence) and not include:
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
