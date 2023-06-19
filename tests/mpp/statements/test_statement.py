"""Testing: mpp.statements.statement
"""
from typing import Any, Set
import pytest

from mpp.constants import STATEMENTS
from mpp.statements.statement import Statement, HeaderParameter, StringReplace


@pytest.mark.parametrize(
    "statement,value,valid_statements",
    [
        ("print", "", STATEMENTS),
        ("prepend", "skin=noskin;", STATEMENTS)
    ]
)
def test_statement(statement: str, value: Any, valid_statements: Set):
    """Test statement Class

    Args:
        statement: _description_
        value: _description_
        valid_statements: _description_
    """
    assert Statement(statement=statement, value=value).validate(valid_statements=valid_statements)


@pytest.mark.parametrize(
    "statement,key,value,valid_statements",
    [
        ("header", "Accept", "*/*", STATEMENTS),
        ("parameter", "oe", "oe=ISO-8859-1;", STATEMENTS)
    ]
)
def test_statement_header_parameter(
    statement: str,
    key: str,
    value: Any,
    valid_statements: Set
):
    """Test HeaderParameter Child Statement Class

    Args:
        statement: _description_
        key: _description_
        value: _description_
        valid_statements: _description_
    """
    assert HeaderParameter(
        statement=statement,
        key=key,
        value=value
    ).validate(valid_statements=valid_statements)


@pytest.mark.parametrize(
    "statement,string,replace,valid_statements",
    [
        ("strrep", "ReflectiveLoader", "", STATEMENTS)
    ]
)
def test_statement_string_replace(
    statement: str,
    string: str,
    replace: Any,
    valid_statements: Set
):
    """Test StringReplace Child Statement Class

    Args:
        statement: _description_
        string: _description_
        value: _description_
        valid_statements: _description_
    """
    assert StringReplace(
        statement=statement,
        string=string,
        replace=replace
    ).validate(valid_statements=valid_statements)
