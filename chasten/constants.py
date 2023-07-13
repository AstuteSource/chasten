"""Define constants with dataclasses for use in chasten."""

from dataclasses import dataclass


# filesystem constant
@dataclass(frozen=True)
class Filesystem:
    """Define the Filesystem dataclass for a constant."""

    Current_Directory: str


filesystem = Filesystem(".")


# humanreadable constant
@dataclass(frozen=True)
class Humanreadable:
    """Define the Humanreadable dataclass for a constant."""

    Yes: str
    No: str


humanreadable = Humanreadable("Yes", "No")
