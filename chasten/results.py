"""Store results from performing an analysis."""

from pathlib import Path
from typing import ClassVar, Union

from pyastgrep import search as pyastgrepsearch  # type: ignore
from pydantic import BaseModel, Field

from chasten import debug

# Note: the nesting of the class definitions is from the
# bottom of this file to the top because the top-level
# object can only refer to others that already exist

# Nesting structure:

# Chasten:
# --> Configuration --> CheckCriterion
# --> Source
#     --> name
#     --> check
#         --> Check
#             --> id
#             --> name
#             --> min
#             --> max
#             --> pattern
#             --> passed
#         --> matches
#             --> lineno
#             --> coloffset


class Match(BaseModel):
    """Define a Pydantic model for a Match."""

    lineno: int
    coloffset: int
    _match: Union[pyastgrepsearch.Match, None] = None


class Check(BaseModel):
    """Define a Pydantic model for a Check."""

    id: str
    name: str
    min: int
    max: int
    pattern: str
    passed: bool
    matches: list[Match] = []


class Source(BaseModel):
    """Define a Pydantic model for a Source."""

    name: str
    check: Union[None, Check] = None


class CheckCriterion(BaseModel):
    """Define a Pydantic model for a CheckIncludeOrExclude."""

    attribute: Union[None, str] = ""
    value: Union[None, str] = ""
    confidence: int = 0


class Configuration(BaseModel):
    """Define a Pydantic model for a Configuration."""

    projectname: str
    configdirectory: Path
    searchpath: Path
    debuglevel: debug.DebugLevel
    debugdestination: debug.DebugDestination
    checkinclude: Union[None, CheckCriterion] = None
    checkexclude: Union[None, CheckCriterion] = None


class Chasten(BaseModel):
    """Define a Pydantic model for a Chasten result."""

    configuration: Configuration
    sources: list[Source] = []
