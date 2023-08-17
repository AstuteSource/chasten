"""Mange the SQLite database containing results from chasten analyses."""

from sqlite_utils import Database

CHASTEN_SQL_SELECT_QUERY = """
SELECT
  main.configuration_projectname as projectname,
  main.configuration_chastenversion as chastenversion,
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
  JOIN main ON sources._link_main = main._link;
"""

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
