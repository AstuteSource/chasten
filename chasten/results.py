"""Store results from performing an analysis."""

import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Union

from pyastgrep import search as pyastgrepsearch  # type: ignore
from pydantic import BaseModel

from chasten import debug

# Note: the nesting of the class definitions is from the
# bottom of this file to the top because the top-level
# object can only refer to others that already exist

# Nesting structure:

# Chasten
# --> Configuration
#     --> chastenversion
#     --> projectname
#     --> configdirectory
#     --> searchpath
#     --> debuglevel
#     --> debugdestination
#     --> checkinclude --> CheckCriterion
#     --> checkexclude --> CheckCriterion
#           --> attribute
#           --> value
#           --> confidence
# --> Source
#     --> filename
#     --> check
#         --> Check
#             --> id
#             --> name
#             --> min
#             --> max
#             --> pattern
#             --> passed
#             --> _matches
#                 --> pyastgrepsearch.Match [*]
#             --> matches
#                 --> Match
#                     --> lineno
#                     --> coloffset
#
# [*] Designates a "private" attribute that is not a part
# of the Pydantic BaseModel and is not saved to the JSON.
# This is used to record results so that the tool can
# display them if the --verbose flag is active.


class Match(BaseModel):
    """Define a Pydantic model for a Match."""

    lineno: int
    coloffset: int
    linematch: str = ""


class Check(BaseModel):
    """Define a Pydantic model for a Check."""

    id: str
    name: str
    description: str = ""
    min: Union[None, int] = 0
    max: Union[None, int] = 0
    pattern: str
    passed: bool
    matches: list[Match] = []
    _matches: list[pyastgrepsearch.Match] = []


class Source(BaseModel):
    """Define a Pydantic model for a Source."""

    filename: str
    filelines: List[str] = []
    check: Union[None, Check] = None


class CheckCriterion(BaseModel):
    """Define a Pydantic model for a CheckIncludeOrExclude."""

    attribute: Union[None, str] = ""
    value: Union[None, str] = ""
    confidence: int = 0


class Configuration(BaseModel):
    """Define a Pydantic model for a Configuration."""

    chastenversion: str
    debuglevel: debug.DebugLevel
    debugdestination: debug.DebugDestination
    projectname: str
    configdirectory: Path
    searchpath: Path
    fileuuid: str = str(uuid.uuid4().hex)
    datetime: str = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    checkinclude: Union[None, CheckCriterion] = None
    checkexclude: Union[None, CheckCriterion] = None


class Chasten(BaseModel):
    """Define a Pydantic model for a Chasten result."""

    configuration: Configuration
    sources: list[Source] = []
