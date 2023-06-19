"""mpp.statements module: Statement
"""
import logging
import re
from typing import Set

from mpp.constants import DELIM


__all__ = [
    "Statement",
    "HeaderParameter",
    "StringReplace"
]

# logger
logger = logging.getLogger(__file__)


class Statement:
    """Statement Class
    """
    STATEMENT_REGEX = re.compile(
        r'^\s*([\w\d]+)\s*(?:(?:"((?:[^"\\]|\\.)*)")|);'
        r'\s*(?:#|//).*|^\s*([\w\d]+)\s*(?:(?:"((?:[^"\\]|\\.)*)")|);\s*$',
        flags=re.MULTILINE
    )

    def __init__(self, statement: str, value: str = ''):
        self.statement = statement
        self.value = value

    def validate(self, valid_statements: Set) -> bool:
        """Validate a statement

        Args:
            valid_statements: _description_

        Returns:
            _description_
        """
        return self.statement in valid_statements

    @classmethod
    def from_string(cls, string):
        """
        Parses statements in the following format and retuns a list
        of class objects if statements are found.
        Format:
            <statement>;
            or
            <statement> "value";

        Args:
            string: _description_

        Raises:
            InvalidStatement: _description_

        Returns:
            _description_
        """
        matches = cls.STATEMENT_REGEX.findall(string)
        if matches:
            return [
                cls(
                    statement=match[0] or match[2],
                    value=match[1] or match[3]
                )
                for match in matches
            ]
        return []

    def __str__(self):
        if self.value:
            return f'{self.statement} "{self.value}"{DELIM}'
        return f'{self.statement}{DELIM}'

    def __repr__(self):
        return f'Statement(statement={self.statement}, value="{self.value}")'


class HeaderParameter(Statement):
    """Header or Parameter Statement

    Args:
        Statement: _description_
    """
    STATEMENT_REGEX = re.compile(
        r'(header|parameter)\s+"([^"]+)"\s+"([^"]+)"\s*;',
        flags=re.MULTILINE
    )

    def __init__(self, statement: str, key: str, value: str = ''):
        super().__init__(statement=statement)
        self.key = key
        self.value = value

    def __str__(self):
        if self.value:
            return f'{self.statement} "{self.key}" "{self.value}"{DELIM}'
        return f'{self.statement} "{self.key}"{DELIM}'

    def __repr__(self):
        return f'Statement(statement={self.statement}, key="{self.key}", value="{self.value}")'

    @classmethod
    def from_string(cls, string):
        """
        Parses statements in the following format and retuns a list
        of class objects if statements are found.

        Args:
            string: _description_

        Raises:
            InvalidStatement: _description_

        Returns:
            _description_
        """
        matches = cls.STATEMENT_REGEX.findall(string)
        if matches:
            return [
                cls(
                    statement=match[0],
                    key=match[1],
                    value=match[2]
                )
                for match in matches
            ]
        return []


class StringReplace(Statement):
    """String Replace Statement

    Args:
        Statement: _description_
    """
    STATEMENT_REGEX = re.compile(r'^\s*(strrep)\s+"([^"]+)"\s*"(.*?)"\s*;(?:\s*#.*|//.*)?', flags=re.MULTILINE)

    def __init__(self, statement: str, string: str, replace: str = ''):
        super().__init__(statement=statement)
        self.string = string
        self.replace = replace

    def __str__(self):
        return f'{self.statement} "{self.string}" "{self.replace}"{DELIM}'

    def __repr__(self):
        return (
            f'Statement(statement={self.statement}, '
            f'string="{self.string}", replace="{self.replace}")'
        )

    @classmethod
    def from_string(cls, string):
        """
        Parses statements in the following format and retuns a list
        of class objects if statements are found.

        Args:
            string: _description_

        Raises:
            InvalidStatement: _description_

        Returns:
            _description_
        """
        matches = cls.STATEMENT_REGEX.findall(string)
        if matches:
            return [
                cls(
                    statement=match[0],
                    string=match[1],
                    replace=match[2]
                )
                for match in matches
            ]
        return []
