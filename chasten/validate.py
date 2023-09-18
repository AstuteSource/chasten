"""Validate various aspects of configurations and command-line arguments."""

from typing import Any, Dict, List, Tuple

import jsonschema
from jsonschema.exceptions import ValidationError

from chasten import constants, output, util

# intuitive description:
# a configuration file links to one or more checks files
# see ./chasten in the root of the repository for the config.yml file
JSON_SCHEMA_CONFIG = {
    "type": "object",
    "required": [],
    "properties": {
        "chasten": {
            "type": "object",
            "properties": {
                "checks-file": {
                    "type": "array",
                    "items": {"type": "string"},
                    "required": [],
                },
            },
            "additionalProperties": False,
        },
    },
}

# intutive description:
# a checks file describes all of the details for one or more checks
# see ./chasten in the root of the repository for the checks.yml file
JSON_SCHEMA_CHECKS = {
    "type": "object",
    "properties": {
        "checks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "id": {"type": "string"},
                    "description": {"type": "string"},
                    "pattern": {"type": "string"},
                    "code": {"type": "string"},
                    "count": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {"min": {"type": "integer"}},
                                "required": ["min"],
                            },
                            {
                                "type": "object",
                                "properties": {"max": {"type": "integer"}},
                                "required": ["max"],
                            },
                            {
                                "type": "object",
                                "properties": {
                                    "min": {"type": "integer"},
                                    "max": {"type": "integer"},
                                },
                                "required": ["min", "max"],
                            },
                        ]
                    },
                },
                "required": ["name", "id", "pattern", "code"],
                "additionalProperties": False,
            },
        }
    },
}


def extract_checks_file_name(
    configuration: Dict[str, Dict[str, Any]]
) -> Tuple[bool, List[str]]:
    """Validate the checks configuration."""
    # there is a main "chasten" key
    if constants.checks.Check_Chasten in configuration.keys():
        # there is a "checks-file" key
        if constants.checks.Check_File in configuration[constants.checks.Check_Chasten]:
            # extract the name of the checks-files
            # and return them in a list with a boolean
            # indicate to show that checks files were found
            checks_file_name_list = configuration[constants.checks.Check_Chasten][
                constants.checks.Check_File
            ]
            return (True, checks_file_name_list)
    # contents were not found and thus returen no filenames
    return (False, [constants.markers.Empty_String])


def validate_configuration(
    configuration: Dict[str, Dict[str, Any]],
    schema: Dict[str, Any] = JSON_SCHEMA_CONFIG,
) -> Tuple[bool, str]:
    """Validate the main configuration."""
    # indicate that validation passed; since there
    # were no validation errors, return an empty string
    try:
        jsonschema.validate(configuration, schema)
        return (True, constants.markers.Empty_String)
    # indicate that validation failed;
    # since validation errors exist, package them up
    # and return them along with the indication
    except ValidationError as validation_error:
        error_message = str(validation_error)
        error_message = error_message.lstrip()
        return (False, error_message)


def validate_checks_configuration(
    configuration: Dict[str, Dict[str, Any]]
) -> Tuple[bool, str]:
    """Validate the checks configuration."""
    return validate_configuration(configuration, JSON_SCHEMA_CHECKS)


def validate_file(
    file_name: str,
    configuration_file_yaml_str: str,
    yaml_data_dict: Dict[str, Dict[str, Any]],
    json_schema: Dict[str, Any] = JSON_SCHEMA_CONFIG,
    verbose: bool = False,
) -> bool:
    """Validate the provided file according to the provided JSON schema."""
    # perform the validation of the configuration file
    (validated, errors) = validate_configuration(yaml_data_dict, json_schema)
    output.console.print(
        f":sparkles: Validated {file_name}? {util.get_human_readable_boolean(validated)}"
    )
    # there was a validation error, so display the error report
    if not validated:
        output.console.print(f":person_shrugging: Validation errors:\n\n{errors}")
    # validation worked correctly, so display the configuration file
    else:
        output.opt_print_log(verbose, newline="")
        output.opt_print_log(
            verbose, label=f":sparkles: Contents of {file_name}:\n"
        )
        output.opt_print_log(verbose, config_file=configuration_file_yaml_str)
    return validated
