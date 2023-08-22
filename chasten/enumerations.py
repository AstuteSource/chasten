"""Define enumerations for the modules in chasten."""

from enum import Enum


class ConfigureTask(str, Enum):
    """Define the different task possibilities."""

    CREATE = "create"
    VALIDATE = "validate"


class DatasettePublicationPlatform(str, Enum):
    """Define the different platforms for publishing a datasette server."""

    FLY = "fly"
    VERCEL = "vercel"


class FilterableAttribute(str, Enum):
    """Define the names of attributes that are subject to filtering."""

    CODE = "code"
    ID = "id"
    NONE = ""
    NAME = "name"
    PATTERN = "pattern"
