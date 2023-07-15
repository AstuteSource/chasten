"""Define constants with dataclasses for use in chasten."""

from dataclasses import dataclass


# chasten constant
@dataclass(frozen=True)
class Chasten:
    """Define the Chasten dataclass for constant(s)."""

    Application_Name: str
    Application_Author: str


chasten = Chasten("Chasten", "ChastenedTeam")


# filesystem constant
@dataclass(frozen=True)
class Filesystem:
    """Define the Filesystem dataclass for constant(s)."""

    Current_Directory: str


filesystem = Filesystem(".")


# humanreadable constant
@dataclass(frozen=True)
class Humanreadable:
    """Define the Humanreadable dataclass for constant(s)."""

    Yes: str
    No: str


humanreadable = Humanreadable("Yes", "No")


# markers constant
@dataclass(frozen=True)
class Markers:
    """Define the Markers dataclass for constant(s)."""

    Bad_Fifteen: str
    Bad_Zero_Zero: str
    Empty_Bytes: bytes
    Empty: str
    Ellipse: str
    Forward_Slash: str
    Dot: str
    Hidden: str
    Indent: str
    Newline: str
    Nothing: str
    Single_Quote: str
    Space: str
    Tab: str
    Underscore: str


markers = Markers(
    Bad_Fifteen="<15>",
    Bad_Zero_Zero="",
    Empty_Bytes=b"",
    Empty="",
    Ellipse="...",
    Forward_Slash="/",
    Dot=".",
    Hidden=".",
    Indent="   ",
    Newline="\n",
    Nothing="",
    Single_Quote="'",
    Space=" ",
    Tab="\t",
    Underscore="_",
)
