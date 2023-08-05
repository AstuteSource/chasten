"""Utilities for use within chasten."""

from chasten import constants

checkmark_unicode = "\u2713"
xmark_unicode = "\u2717"


def get_human_readable_boolean(answer: bool) -> str:
    """Produce a human-readable Yes or No for a boolean value of True or False."""
    # the provided answer is true
    if answer:
        return constants.humanreadable.Yes
    # the provided answer is false
    return constants.humanreadable.No


def get_symbol_boolean(answer: bool) -> str:
    """Produce a symbol-formatted version of a boolean value of True or False."""
    if answer:
        return f"[green]{checkmark_unicode}[/green]"
    return f"[red]{xmark_unicode}[/red]"
