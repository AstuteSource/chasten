"""Store results from performing an analysis."""

from enum import Enum
from pathlib import Path
from typing import Dict, Union

from pydantic import BaseModel

from chasten import debug


class ComponentTypes(str, Enum):
    """The predefined types of components."""

    Chasten = "Chasten"
    Check = "Check"
    CheckInclude = "CheckInclude"
    Configuration = "Configuration"
    Match = "Match"
    Source = "Source"


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
    results: list[Check] = []


class CheckCriterion(BaseModel):
    """Define a Pydantic model for a CheckIncludeOrExclude."""

    attribute: Union[None, str]
    value: Union[None, str]
    confidence: Union[None, int]


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


# define the component dictionary that will store the
# constituent parts of a complete result before all content exists
components: Dict[
    ComponentTypes, Union[Match, Check, Source, Configuration, Chasten, CheckCriterion]
] = {}
