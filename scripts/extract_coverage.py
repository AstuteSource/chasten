"""Demonstrate how to extract coverage with coverage.py."""

from coverage import CoverageData

# Construct CoverageData instance
data = CoverageData()
data.read()

print(data)  # noqa

# Get covered line numbers for a file
filename = "chasten/util.py"
covered_lines = set(data.lines(filename))  # type: ignore

print(f"Covered lines in {filename}:")   # noqa
print(covered_lines)  # noqa
