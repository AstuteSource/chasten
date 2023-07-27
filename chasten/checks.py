"""Extract and analyze details about specific checks."""


from typing import Dict, Tuple, Union

from chasten import constants


def extract_min_max(
    check: Dict[str, Union[str, Dict[str, int]]]
) -> Tuple[Union[int, None], Union[int, None]]:
    """Extract the minimum and maximum values from the checks dictionary."""
    # extract information about the count attribute
    # and the min and max values if they exist
    min_count = check.get(constants.checks.Check_Count, {}).get(constants.checks.Check_Min)  # type: ignore
    max_count = check.get("count", {}).get("max")  # type: ignore
    return (min_count, max_count)
