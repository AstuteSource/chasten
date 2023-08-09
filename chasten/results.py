"""Store results from performing an analysis."""

from pathlib import Path
from typing import Union

from pydantic import BaseModel

from chasten import debug


class Match(BaseModel):
    """Define a Pydantic model for a Match."""

    lineno: int
    coloffset: int


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
