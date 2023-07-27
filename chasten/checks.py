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
