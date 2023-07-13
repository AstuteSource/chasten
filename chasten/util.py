"""Utilities for use within chasten."""

from chasten import constants


def get_human_readable_boolean(answer: bool) -> str:
    """Produce a human-readable Yes or No for a boolean value of True or False."""
    # the provided answer is true
    if answer:
        return constants.humanreadable.Yes
    # the provided answer is false
    return constants.humanreadable.No
