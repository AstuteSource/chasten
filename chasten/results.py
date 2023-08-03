"""Store results from performing an analysis."""

from enum import Enum
from pathlib import Path
from typing import Dict, Union

from pydantic import BaseModel

from chasten import debug


# components: Dict[str, Union[Match, Check, Source, Configuration, Chasten]] = {}
class ComponentTypes(str, Enum):
    """The predefined types of components."""

    Match = "Match"
    Check = "Check"
    Source = "Source"
    Configuration = "Configuration"
    Chasten = "Chasten"


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

    name: list[str] = []
    results: list[Check] = []


class Configuration(BaseModel):
    """Define a Pydantic model for a Configuration."""

    projectname: str
    configdirectory: Path
    searchpath: Path
    debuglevel: debug.DebugLevel
    debugdestination: debug.DebugDestination


class Chasten(BaseModel):
    """Define a Pydantic model for a Chasten result."""

    configuration: Configuration
    source: Source


# define the component dictionary that will store the
# constituent parts of a complete result before all content exists
components: Dict[ComponentTypes, Union[Match, Check, Source, Configuration, Chasten]] = {}
