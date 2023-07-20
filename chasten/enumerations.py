"""Define enumerations for the modules in chasten."""

from enum import Enum


class ConfigureTask(str, Enum):
    """Define the different task possibilities."""

    CREATE = "create"
    VALIDATE = "validate"
