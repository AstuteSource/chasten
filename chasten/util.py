"""Utilities for use within chasten."""

import importlib.metadata
import platform
import sys

from urllib3.util import parse_url

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


def executable_name(executable_name: str, OpSystem: str = "Linux") -> str:
    """Get the executable directory depending on OS"""
    exe_directory = "/bin/"
    # Checks if the OS is windows and changed where to search if true
    if OpSystem == "Windows":
        exe_directory = "/Scripts/"
        executable_name += ".exe"
    virtual_env_location = sys.prefix
    return virtual_env_location + exe_directory + executable_name


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


def is_url(url: str) -> bool:
    """Determine if string is valid URL."""
    # parse input url
    url_parsed = parse_url(url)
    # only allow http and https
    if url_parsed.scheme not in ["http", "https"]:
        return False
    # only input characters for initiatig query and/or fragments if necessary
    port_character = ":" if url_parsed.port is not None else ""
    query_character = "?" if url_parsed.query is not None else ""
    fragment_character = "#" if url_parsed.fragment is not None else ""
    url_pieces = [
        url_parsed.scheme,
        "://",
        url_parsed.host,
        port_character,
        url_parsed.port,
        url_parsed.path,
        query_character,
        url_parsed.query,
        fragment_character,
        url_parsed.fragment,
    ]
    # convert every item to a string and piece the url back together
    # to make sure it matches what was given
    url_reassembled = ""
    for url_piece in url_pieces:
        if url_piece is not None:
            url_reassembled += str(url_piece)
    # determine if parsed and reconstructed url matches original
    return str(parse_url(url)).lower() == url_reassembled.lower()


def total_amount_passed(analyze_result, count_total) -> tuple[int, int, float]:
    """Calculate amount of checks passed in analyze"""
    try:
        # iterate through check sources to find checks passed
        list_passed = [x.check.passed for x in analyze_result.sources]
        # set variables to count true checks and total counts
        count_true = list_passed.count(True)
        # return tuple of checks passed, total checks, percentage of checks passed
        return (count_true, count_total, (count_true / count_total) * 100)
    # return exception when dividing by zero
    except ZeroDivisionError:
        return (0, 0, 0.0)
