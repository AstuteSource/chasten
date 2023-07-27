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
    Programming_Language: str
    Separator: str
    Server_Shutdown: str
    Tagline: str
    Theme_Background: str
    Theme_Colors: str
    Website: str


chasten = Chasten(
    Application_Name="chasten",
    Application_Author="ChastenedTeam",
    Emoji=":dizzy:",
    Https="https://",
    Name="chasten",
    Programming_Language="python",
    Separator="/",
    Server_Shutdown=":person_shrugging: Shut down chasten's sylog server",
    Tagline="chasten: Analyze the AST of Python Source Code",
    Theme_Background="default",
    Theme_Colors="ansi_dark",
    Website=":link: GitHub: https://github.com/gkapfham/chasten",
)


# checks constant
@dataclass(frozen=True)
class Checks:
    """Define the Checks dataclass for constant(s)."""

    Check_Chasten: str
    Check_Code: str
    Check_Count: str
    Check_Confidence: int
    Check_File: str
    Check_Id: str
    Checks_Label: str
    Check_Max: str
    Check_Min: str
    Check_Name: str
    Check_Pattern: str


checks = Checks(
    Check_Chasten="chasten",
    Check_Code="code",
    Check_Count="count",
    Check_Confidence=80,
    Check_File="checks-file",
    Check_Id="id",
    Checks_Label="checks",
    Check_Max="max",
    Check_Min="min",
    Check_Name="name",
    Check_Pattern="pattern",
)


# filesystem constant
@dataclass(frozen=True)
class Filesystem:
    """Define the Filesystem dataclass for constant(s)."""

    Current_Directory: str
    Main_Configuration_File: str
    Main_Checks_File: str


filesystem = Filesystem(
    Current_Directory=".",
    Main_Configuration_File="config.yml",
    Main_Checks_File="checks.yml",
)


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
    Code_Context: int
    Comma_Space: str
    Empty_Bytes: bytes
    Empty_String: str
    Ellipse: str
    Forward_Slash: str
    Dot: str
    Hidden: str
    Indent: str
    Newline: str
    Non_Zero_Exit: int
    Nothing: str
    Single_Quote: str
    Slice_One: int
    Space: str
    Tab: str
    Underscore: str
    Xml: str
    Zero_Exit: int


markers = Markers(
    Bad_Fifteen="<15>",
    Bad_Zero_Zero="",
    Code_Context=5,
    Comma_Space=", ",
    Empty_Bytes=b"",
    Empty_String="",
    Ellipse="...",
    Forward_Slash="/",
    Dot=".",
    Hidden=".",
    Indent="   ",
    Newline="\n",
    Non_Zero_Exit=1,
    Nothing="",
    Single_Quote="'",
    Slice_One=1,
    Space=" ",
    Tab="\t",
    Underscore="_",
    Xml="xml",
    Zero_Exit=0,
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
