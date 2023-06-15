"""mpp.parser module: exceptions
"""

__all__ = [
    "InvalidBlock",
    "InvalidOption",
    "InvalidStatement",
    "ParsingError"
]


class InvalidBlock(ValueError):
    """invalid block found"""


class InvalidOption(ValueError):
    """invalid option format, expected: set [option] "[value]";"""


class InvalidStatement(ValueError):
    """invalid statement format, expected: [statement] <optional value>;"""


class ParsingError(ValueError):
    """parsing error when reading profile"""
