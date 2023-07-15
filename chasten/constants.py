"""Define constants with dataclasses for use in chasten."""

from dataclasses import dataclass


# chasten constant
@dataclass(frozen=True)
class Chasten:
    """Define the Chasten dataclass for constant(s)."""

    Application_Name: str
    Application_Author: str
    Emoji: str
    Https: str
    Name: str
    Separator: str
    Server_Shutdown: str
    Tagline: str
    Website: str


chasten = Chasten(
    Application_Name="Chasten",
    Application_Author="ChastenedTeam",
    Emoji=":dizzy:",
    Https="https://",
    Name="chasten",
    Separator="/",
    Server_Shutdown=":person_shrugging: Shut down chasten's sylog server",
    Tagline="chasten: Check the AST of Python Source Code",
    Website=":link: https://github.com/gkapfham/chasten",
)


# filesystem constant
@dataclass(frozen=True)
class Filesystem:
    """Define the Filesystem dataclass for constant(s)."""

    Current_Directory: str


filesystem = Filesystem(Current_Directory=".")


# humanreadable constant
@dataclass(frozen=True)
class Humanreadable:
    """Define the Humanreadable dataclass for constant(s)."""

    Yes: str
    No: str


humanreadable = Humanreadable(Yes="Yes", No="No")


# logger constant
@dataclass(frozen=True)
class Logger:
    """Define the Logger dataclass for constant(s)."""

    Function_Prefix: str
    Richlog: str
    Syslog: str


logger = Logger(
    Function_Prefix="configure_logging_",
    Richlog="chasten-richlog",
    Syslog="chasten-syslog",
)


# logging constant
@dataclass(frozen=True)
class Logging:
    """Define the Logging dataclass for constant(s)."""

    Debug: str
    Info: str
    Warning: str
    Error: str
    Critical: str
    Console_Logging_Destination: str
    Syslog_Logging_Destination: str
    Default_Logging_Destination: str
    Default_Logging_Level: str
    Format: str
    Rich: str


logging = Logging(
    Debug="DEBUG",
    Info="INFO",
    Warning="WARNING",
    Error="ERROR",
    Critical="CRITICAL",
    Console_Logging_Destination="CONSOLE",
    Syslog_Logging_Destination="syslog",
    Default_Logging_Destination="console",
    Default_Logging_Level="ERROR",
    Format="%(message)s",
    Rich="Rich",
)


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


# output constant
@dataclass(frozen=True)
class Output:
    """Define the Output dataclass for constant(s)."""

    Syslog: str
    Test_Start: str


output = Output(
    Syslog=":sparkles: Syslog server for receiving debugging information",
    Test_Start=":sparkles: Start to run test suite for the specified program",
)


# server constant
@dataclass(frozen=True)
class Server:
    """Define the Server dataclass for constant(s)."""

    Backup_Count: int
    Localhost: str
    Log_File: str
    Max_Log_Size: int
    Poll_Interval: float
    Port: int
    Utf8_Encoding: str


server = Server(
    Backup_Count=1,
    Localhost="127.0.0.1",
    Log_File=".discover.log",
    Max_Log_Size=1048576,
    Poll_Interval=0.5,
    Port=2525,
    Utf8_Encoding="utf-8",
)
