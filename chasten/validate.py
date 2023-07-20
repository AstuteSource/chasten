"""Validate various aspects of configurations and command-line arguments."""

from typing import Any, Dict, List, Tuple

import jsonschema
from jsonschema.exceptions import ValidationError

from chasten import constants

JSON_SCHEMA_CONFIG = {
    "type": "object",
    "required": [],
    "properties": {
        "chasten": {
            "type": "object",
            "properties": {
                "verbose": {
                    "type": "boolean",
                    "required": [],
                },
                "debug-level": {
                    "type": "string",
                    "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                    "required": [],
                },
                "debug-destination": {
                    "type": "string",
                    "enum": ["CONSOLE", "SYSLOG"],
                    "required": [],
                },
                "search-directory": {
                    "type": "array",
                    "items": {"type": "string"},
                    "required": [],
                },
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
                    "pattern": {"type": "string"},
                    "code": {"type": "string"},
                    "count": {
                        "oneOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "min": {"type": "integer"},
                                    "max": {"type": "integer"},
                                },
                                "required": ["min", "max"],
                            },
                            {"type": "boolean"},
                        ]
                    },
                },
                "required": ["name", "id", "pattern"],
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
    if "chasten" in configuration.keys():
        # there is a "checks-file" key
        if "checks-file" in configuration["chasten"]:
            # extract the name of the checks-files
            # and return them in a list with a boolean
            # indicate to show that checks files were found
            checks_file_name_list = configuration["chasten"]["checks-file"]
            return (True, checks_file_name_list)
    # contents were not found and thus returen no filenames
    return (False, [constants.markers.Empty])


def validate_configuration(
    configuration: Dict[str, Dict[str, Any]],
    schema: Dict[str, Any] = JSON_SCHEMA_CONFIG,
) -> Tuple[bool, str]:
    """Validate the main configuration."""
    # indicate that validation passed; since there
    # were no validation errors, return an empty string
    try:
        jsonschema.validate(configuration, schema)
        return (True, constants.markers.Empty)
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
