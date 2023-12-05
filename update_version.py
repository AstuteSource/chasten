from pathlib import Path

import toml

# defines the max value for the version except for the first value
UPDATE_STEP = 10


def updated_version(version: str) -> str:
    """Updates the version based on the current version and specified step"""
    # gets a list of integers by splitting the version by a period
    # this is so it can separately change each part of the version
    version_list = [int(x) for x in version.split(".")]
    # adds 1 to the last value of version
    version_list[2] += 1
    # iterates through to make sure if the value is equal
    # to ten it sets it to zero and adds 1 to the next part of
    # version so it would change [0,2,10] to [0,3,0]
    for i in range(2, 0, -1):
        if version_list[i] >= UPDATE_STEP:
            version_list[i - 1] += 1
            version_list[i] = 0
    # turns the result back into a string split by a period and returns it
    # ex -> [0,3,0] turns into "0.3.0"
    result = ".".join([str(x) for x in version_list])
    return result


if __name__ == "__main__":
    # Open toml file and change the version of the program.
    file = Path("pyproject.toml")
    # turns the toml into a dictionary to be able to find
    # the specified value and not change anything else
    toml_dict = toml.load(file)
    version = toml_dict["tool"]["poetry"]["version"]
    # reads the text as a string
    content = file.read_text()
    # replaces the version with the updated version using the function
    # updated_version, Only replaces the first instance of it
    content = content.replace(version, updated_version(version), 1)
    # write the changes to the toml file
    file.write_text(content)
