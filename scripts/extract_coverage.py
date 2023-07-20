from coverage import CoverageData

# Construct CoverageData instance
data = CoverageData()
data.read()

print(data)

# Get covered line numbers for a file
filename = 'chasten/util.py'
covered_lines = set(data.lines(filename))

print(f"Covered lines in {filename}:")
print(covered_lines)
