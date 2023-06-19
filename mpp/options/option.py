"""mpp.options module: Option
"""
import logging
import re
from typing import Set

from mpp.constants import DELIM


__all__ = [
    "Option"
]


# logger
logger = logging.getLogger(__file__)


class Option:
    """Option Class
    """
    # This regex will parse an option, ignoring anything after a comment and any whitespace
    # that may occur between values
    OPTION_REGEX = re.compile(r'^\s*set\s+(\w+)\s+"([^"]*)"\s*;(?:\s*#.*|//.*)?', re.MULTILINE)

    def __init__(self, option: str, value: str):
        self.option = option
        self.value = value

    def __str__(self):
        return f'set {self.option} "{self.value}"{DELIM}'

    def __repr__(self):
        return f'Option(option="{self.option}", value="{self.value}")'

    @classmethod
    def from_string(cls, string: str):
        """Parses options in the following format and returns a list of class 
        objects if options are found.
            Format: set [option] "[value]";

        Args:
            string: _description_

        Returns:
            _description_
        """
        matches = cls.OPTION_REGEX.findall(string)
        if matches:
            return [
                cls(option=match[0], value=match[1])
                for match in matches
            ]
        return []

    def validate(self, valid_options: Set) -> bool:
        """Validate an option

        Args:
            valid_options: Valid options for a block or general.

        Returns:
            Boolean indicating validity.
        """
        return self.option in valid_options
