"""Mange the SQLite database containing results from chasten analyses."""

import shutil
import subprocess
import sys
from pathlib import Path

from sqlite_utils import Database

from chasten import constants
from chasten import output

CHASTEN_SQL_SELECT_QUERY = """
SELECT
  main.configuration_chastenversion as chastenversion,
  main.configuration_projectname as projectname,
  main.configuration_datetime as datetime,
  sources.filename,
  sources.check_id,
  sources.check_name,
  sources.check_description,
  sources.check_pattern,
  sources.check_min,
  sources.check_max,
  sources.check_passed,
  sources_check_matches.lineno,
  sources_check_matches.coloffset,
  sources_check_matches.linematch
FROM
  sources
  JOIN sources_check_matches ON sources._link = sources_check_matches._link_sources
  JOIN main ON sources._link_main = main._link
ORDER BY
  datetime desc;
"""

# create a small bullet for display in the output
small_bullet_unicode = constants.markers.Small_Bullet_Unicode


def create_chasten_view(chasten_database_name: str) -> None:
    """Create a view that combines results in the database tables."""
    database = Database(chasten_database_name)
    # create a "virtual table" (i.e., a view) that is the result
    # of running the pre-defined query; note that this query
    # organizes all of chasten's results into a single table.
    # When using datasette each of the columns in this view
    # are "facetable" which means that they can be enabled or disabled
    # inside of the web-based user interface
    database.create_view("chasten_complete", CHASTEN_SQL_SELECT_QUERY)


def enable_full_text_search(chasten_database_name: str) -> None:
    """Enable full-text search in the specific SQLite3 database."""
    database = Database(chasten_database_name)
    # enable full-text search on the main database table
    database["main"].enable_fts(
        [
            "configuration_chastenversion",
            "configuration_projectname",
            "configuration_datetime",
        ]
    )
    # enable full-text search on the sources database table
    database["sources"].enable_fts(
        [
            "filename",
            "filelines",
            "check_id",
            "check_name",
            "check_description",
            "check_pattern",
        ]
    )
    # enable full-text search on the sources database table
    database["sources_check_matches"].enable_fts(
        [
            "lineno",
            "coloffset",
            "linematch",
        ]
    )
    # note that sqlite-utils does not support the enabling of
    # full-text search on the view called chasten_complete


def display_datasette_details(
    label: str,
    virtual_env_location: str,
    executable_path: str,
    full_executable_name: str,
    publish: bool
) -> None:
    """Display details about the current datasette configuration."""
    # output diagnostic information about the datasette instance; note
    # that the output must appear here and not from the calling function
    # because once the datasette instance starts the chasten tool can
    # no longer produce output in the console
    output.console.print()
    output.console.print(label)
    output.console.print(
        f"{constants.markers.Indent}{small_bullet_unicode} Venv: '{output.shorten_file_name(str(virtual_env_location), 120)}'"
    )
    if executable_path:
        output.console.print(
            f"{constants.markers.Indent}{small_bullet_unicode} Program: '{output.shorten_file_name(executable_path, 120)}'"
        )
    else:
        output.console.print(
            f"{constants.markers.Indent}{small_bullet_unicode} Cannot find: '{output.shorten_file_name(full_executable_name, 120)}'"
        )
    output.console.print()
    if publish:
        output.console.print(
            ":sparkles: Debugging output from publishing datasette to fly.io:"
        )
    else:
        output.console.print(
            ":sparkles: Debugging output from the local datasette instance:"
        )
    output.console.print()


def start_local_datasette_server(
    database_path: Path,
    datasette_metadata: Path,
    datasette_port: int = 8001,
    publish: bool = False,
) -> None:
    """Start a local datasette server."""
    # define the name of the executable needed to run the server
    executable_name = constants.datasette.Datasette_Executable
    # define the name of the file that contains datasette metadata;
    # note that by default the metadata could be None and thus it
    # will not be passed as a -m argument to the datasette program
    metadata = datasette_metadata
    # identify the location at which the virtual environment exists;
    # note that this is the location where executable dependencies of
    # chasten will exist in a bin directory. For instance, the "datasette"
    # executable that is a dependency of chasten can be found by starting
    # the search from this location for the virtual environment.
    virtual_env_location = sys.prefix
    full_executable_name = virtual_env_location + "/bin/" + executable_name
    executable_path = shutil.which(full_executable_name)
    # output diagnostic information about the datasette instance; note
    # that the output must appear here and not from the calling function
    # because once the datasette instance starts the chasten tool can
    # no longer produce output in the console
    if publish:
        label = ":sparkles: Details for datasette publishing:"
    else:
        label = ":sparkles: Details for datasette startup:"
    display_datasette_details(label, virtual_env_location, str(executable_path), full_executable_name, publish)
    # run the localhost server
    if not publish:
        # the metadata parameter should not be passed to the datasette
        # program if it was not specified as an option
        if metadata is not None:
            cmd = [
                str(full_executable_name),
                str(database_path),
                "-m",
                str(metadata),
                "-p",
                str(datasette_port),
            ]
        else:
            cmd = [
                str(full_executable_name),
                str(database_path),
                "-p",
                str(datasette_port),
            ]
        # run the datasette server as a subprocess of chasten;
        # note that the only way to stop the server is to press CTRL-C;
        # there is debugging output in the console to indicate this option.
        proc = subprocess.Popen(cmd)
        proc.wait()
    # publish the datasette instance to fly.io
    elif publish:
        # the metadata parameter should not be passed to the datasette
        # program if it was not specified as an option
        if metadata is not None:
            cmd = [
                str(full_executable_name),
                "publish",
                "fly",
                str(database_path),
                "--app=chasten",
                "-m",
                str(metadata),
            ]
        else:
            cmd = [
                str(full_executable_name),
                "publish",
                "fly",
                str(database_path),
                "--app=chasten",
            ]
        # run the datasette server as a subprocess of chasten;
        # note that the only way to stop the server is to press CTRL-C;
        # there is debugging output in the console to indicate this option.
        proc = subprocess.Popen(cmd)
        proc.wait()
