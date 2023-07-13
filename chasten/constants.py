"""Define constants with dataclasses for use in chasten."""

from dataclasses import dataclass


# filesystem constant
@dataclass(frozen=True)
class Filesystem:
    Current_Directory: str

filesystem = Filesystem(".")


# humanreadable constant
@dataclass(frozen=True)
class Humanreadable:
    Yes: str
    No: str

humanreadable = Humanreadable("Yes", "No")
