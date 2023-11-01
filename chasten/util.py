"""Utilities for use within chasten."""

import importlib.metadata
import platform

from chasten import constants

checkmark_unicode = "\u2713"
xmark_unicode = "\u2717"
default_chasten_semver = "0.0.0"


def get_human_readable_boolean(answer: bool) -> str:
    """Produce a human-readable Yes or No for a boolean value of True or False."""
    # the provided answer is true
    if answer:
        return constants.humanreadable.Yes
    # the provided answer is false
    return constants.humanreadable.No


def get_OS() -> str:
    """Gets the Operating system of the user."""
    OpSystem = platform.system()
    return OpSystem


def get_symbol_boolean(answer: bool) -> str:
    """Produce a symbol-formatted version of a boolean value of True or False."""
    if answer:
        return f"[green]{checkmark_unicode}[/green]"
    return f"[red]{xmark_unicode}[/red]"


def get_chasten_version() -> str:
    """Use importlib to extract the version of the package."""
    # attempt to determine the current version of the entire package,
    # bearing in mind that this program appears on PyPI with the name "chasten";
    # this will then return the version string specified with the version attribute
    # in the [tool.poetry] section of the pyproject.toml file
    try:
        version_string_of_foo = importlib.metadata.version(
            constants.chasten.Application_Name
        )
    # note that using the version function does not work when chasten is run
    # through a 'poetry shell' and/or a 'poetry run' command because at that stage
    # there is not a working package that importlib.metadata can access with a version;
    # in this situation the function should return the default value of 0.0.0
    except importlib.metadata.PackageNotFoundError:
        version_string_of_foo = default_chasten_semver
    return version_string_of_foo


def join_and_preserve(data, start, end):
    """Join and preserve lines inside of a list."""
    return constants.markers.Newline.join(data[start:end])


def total_amount_passed(analyze_result) -> tuple[int, int, float]:
    """Calculate amount of checks passed in analyze"""
    # iterate through check sources to find checks passed
    list_checks = [x.check.passed for x in analyze_result.sources]
    # set variables to count true checks and total counts
    count_true, count_total = list_checks.count(True), len(list_checks) / 2
    # return tuple of checks passed, total checks, percentage of checks passed
    return (count_true, int(count_total), (count_true / count_total) * 100)
