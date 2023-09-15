"""Mange the SQLite database containing results from chasten analyses."""

import subprocess
import sys
from pathlib import Path

from sqlite_utils import Database

from chasten import constants, enumerations, filesystem, output

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
  sources_check_matches.linematch,
  sources_check_matches.linematch_context
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
    database.create_view(
        constants.chasten.Chasten_Database_View, CHASTEN_SQL_SELECT_QUERY
    )


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


def display_final_diagnostic_message(datasette_platform: str, publish: bool):
    """Output the final diagnostic message before control is given to a different tool."""
    # output a "final" prompt about either the publication platform of a reminder
    # that the remainder of the output comes from running a local datasette instance
    # the database will be published to an external platform
    if publish:
        output.console.print(
            f":sparkles: Debugging output from publishing datasette to '{datasette_platform}':"
        )
    # the database will be displayed through a localhost-based server
    else:
        output.console.print(
            ":sparkles: Debugging output from the local datasette server:"
        )
    output.console.print()


def display_datasette_details(
    label: str,
    virtual_env_location: str,
    executable_path: str,
    full_executable_name: str,
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


def executable_name(OpSystem: str = "Linux") -> str:
    """Get the executable directory depending on OS"""
    exe_directory = "/bin/"
    executable_name = constants.datasette.Datasette_Executable
    # Checks if the OS is windows and changed where to search if true
    if OpSystem == "Windows":
        exe_directory = "/Scripts/"
        executable_name += ".exe"
    virtual_env_location = sys.prefix
    return virtual_env_location + exe_directory + executable_name


def start_datasette_server(  # noqa: PLR0912
    database_path: Path,
    datasette_metadata: Path,
    datasette_platform: str = enumerations.DatasettePublicationPlatform.FLY.value,
    datasette_port: int = 8001,
    publish: bool = False,
    OpSystem: str = "Linux",
) -> None:
    """Start a local datasette server."""
    # define the name of the executable needed to run the server
    # define the name of the file that contains datasette metadata;
    # note that by default the metadata could be None and thus it
    # will not be passed as a -m argument to the datasette program
    metadata = datasette_metadata
    # identify the location at which the virtual environment exists;
    # note that this is the location where executable dependencies of
    # chasten will exist in a bin directory. For instance, the "datasette"
    # executable that is a dependency of chasten can be found by starting
    # the search from this location for the virtual environment.
    full_executable_name = executable_name(OpSystem)
    (found_executable, executable_path) = filesystem.can_find_executable(
        full_executable_name
    )
    # output diagnostic information about the datasette instance; note
    # that the output must appear here and not from the calling function
    # because once the datasette instance starts the chasten tool can
    # no longer produce output in the console
    if publish:
        label = ":sparkles: Details for datasette publishing:"
    else:
        label = ":sparkles: Details for datasette startup:"
    display_datasette_details(
        label,
        sys.prefix,
        str(executable_path),
        full_executable_name,
    )
    # since it was not possible to find the executable for datasette, display and
    # error message and then exit this function since no further steps are possible
    if not found_executable:
        output.console.print(
            f":person_shrugging: Was not able to find {constants.datasette.Datasette_Executable}"
        )
        return None
    # run the localhost server because the
    # function was not asked to publish a database
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
    # publish the datasette instance to the chosen datasette platform
    elif publish:
        # get information about the datasette executable, confirming that
        # it is available in the virtual environment created by chasten
        (
            found_publish_platform_executable,
            publish_platform_executable,
        ) = filesystem.can_find_executable(datasette_platform)
        # was not able to find the fly or vercel executable (the person using this
        # program has to install separately, following the instructions for the
        # datasette-publish-fly plugin) and thus need to exit and not proceed
        if not found_publish_platform_executable:
            output.console.print(
                ":person_shrugging: Was not able to find '{datasette_platform}'"
            )
            return None
        # was able to find the fly or vercel executable that will support the
        # publication of this datasette instance to the platform
        else:
            output.console.print(
                f":sparkles: Using '{publish_platform_executable}' to publish a datasette"
            )
            output.console.print()
        display_final_diagnostic_message(datasette_platform, publish)
        # create the customized running argument for either fly or vercel; note
        # that these programs take different arguments for specifying the name
        # of the application as it will be deployed on the platform
        running_argument = ""
        if datasette_platform == constants.chasten.Executable_Fly:
            running_argument = "--app=chasten"
        elif datasette_platform == constants.chasten.Executable_Vercel:
            running_argument = "--project=chasten"
        # the metadata parameter should not be passed to the datasette
        # program if it was not specified as an option
        # there was a metadata parameter, so include it
        if metadata is not None:
            cmd = [
                str(full_executable_name),
                "publish",
                datasette_platform,
                str(database_path),
                running_argument,
                constants.datasette.Datasette_Copyable_Install,
                constants.datasette.Datasette_Export_Notebook,
                constants.datasette.Datasette_Search_All,
                "-m",
                str(metadata),
            ]
        # there was not a metadata parameter, so include it
        else:
            cmd = [
                str(full_executable_name),
                "publish",
                datasette_platform,
                str(database_path),
                running_argument,
                constants.datasette.Datasette_Copyable_Install,
                constants.datasette.Datasette_Export_Notebook,
                constants.datasette.Datasette_Search_All,
            ]
        # run the datasette server as a subprocess of chasten;
        # note that the only way to stop the server is to press CTRL-C;
        # there is debugging output in the console to indicate this option.
        proc = subprocess.Popen(cmd)
        proc.wait()
