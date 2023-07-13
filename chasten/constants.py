"""Define constants for use in chasten."""

import collections
import itertools


def create_constants(name, *args, **kwargs):
    """Create a namedtuple of constants."""
    # the constants are created such that:
    # the name is the name of the namedtuple
    # for *args with "Constant_Name" or **kwargs with Constant_Name = "AnyConstantName"
    # note that this creates a constant that will
    # throw an AttributeError when attempting to redefine
    new_constants = collections.namedtuple(name, itertools.chain(args, kwargs.keys()))
    return new_constants(*itertools.chain(args, kwargs.values()))


# define the constants for file system access
filesystem = create_constants(
    "filesystem",
    Current_Directory=".",
)


# define the constants for human-readable output
humanreadable = create_constants(
    "humanreadable",
    Yes="Yes",
    No="No",
)
