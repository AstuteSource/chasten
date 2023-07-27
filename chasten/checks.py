"""Extract and analyze details about specific checks."""

from typing import Dict, List, Tuple, Union

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


def create_attribute_label(attribute: Union[str, int, None], label: str) -> str:
    """Create an attribute label string for display as long as it is not null."""
    # define an empty attribute string, which is
    # the default in the case when attribute is None
    labeled_attribute = ""
    # the attribute is not None and thus the function
    # should create the labelled attribute out of it
    if attribute:
        labeled_attribute = f"{label} = {attribute}"
    return labeled_attribute


def join_attribute_labels(attribute_labels: List[str]) -> str:
    """Join all of the attribute labels in a comma-separated list."""
    # start the joined attribute labels with the empty string,
    # which is what it will be by default as well
    joined_attribute_labels = constants.markers.Empty_String
    # incrementally create the list of labelled attributes,
    # separating each one with a comma and a space and
    # ensuring that the last one does not have a trailing
    # comma and space after it
    for i, attribute_label in enumerate(attribute_labels):
        # only add the comma and the space when the for loop
        # is not dealing with the final value in the list of labels
        if i > 0:
            joined_attribute_labels += constants.markers.Comma_Space
        # append the new attribute label to the running list
        joined_attribute_labels += attribute_label  # type: ignore
    return joined_attribute_labels


def __is_in_closed_interval(value, min_value, max_value):
    """Help to see if the value is in the closed interval."""
    return min(max_value, value) == value and max(min_value, value) == value


def check_match_count(
    count: int, min_value: Union[int, None] = None, max_value: Union[int, None] = None
) -> bool:
    """Confirm that the count is between min_value and max_value."""
    # Overall description: if min_value is not None then count must be >= min_value.
    # If max_value is not None then count must be <= max_value
    # both of the values are None and thus the comparision is vacuously true
    if min_value is None and max_value is None:
        return True
    # both are not None and thus the count must be in the closed interval
    if min_value is not None and max_value is not None:
        return __is_in_closed_interval(count, min_value, max_value)
    # at this point, only one of the values might not be None
    # if min_value is not None, then confirm that it is less than or equal
    if min_value is not None:
        if count <= min_value:
            return True
    # if max_value is not None, then confirm that it is greater than or equal
    if max_value is not None:
        if count >= max_value:
            return True
    # if none of those conditions were true, then the count is not
    # between the minimum and the maximum value, inclusively
    return False
