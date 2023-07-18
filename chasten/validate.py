"""Validate various aspects of configurations and command-line arguments."""

from typing import Any, Dict, Tuple

import jsonschema
from jsonschema.exceptions import ValidationError

from chasten import constants

JSON_SCHEMA = {
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
            },
            "additionalProperties": False,
        },
    },
}


def validate_configuration(
    configuration: Dict[str, Dict[str, Any]]
) -> Tuple[bool, str]:
    """Validate the configuration."""
    # indicate that validation passed; since there
    # were no validation errors, return an empty string
    try:
        jsonschema.validate(configuration, JSON_SCHEMA)
        return (True, constants.markers.Empty)
    # indicate that validation failed;
    # since validation errors exist, package them up
    # and return them along with the indication
    except ValidationError as validation_error:
        error_message = str(validation_error)
        error_message = error_message.lstrip()
        print(error_message)
        return (False, error_message)
