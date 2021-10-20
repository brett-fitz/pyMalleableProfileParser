from typing import Set
from mpp.constants import DELIM


class Statement:

    def __init__(self, statement: str, value: str = ''):
        self.statement = statement
        self.value = value

    def validate(self, valid_statements: Set) -> bool:
        return self.statement in valid_statements

    def __str__(self):
        if self.value:
            return f'{self.statement} "{self.value}"{DELIM}'
        return f'{self.statement}{DELIM}'

    def __repr__(self):
        return f'Statement(statement={self.statement}, value="{self.value}")'


class HeaderParameter(Statement):

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


class StringReplace(Statement):

    def __init__(self, statement: str, string: str, replace: str = ''):
        super().__init__(statement=statement)
        self.string = string
        self.replace = replace

    def __str__(self):
        return f'{self.statement} "{self.string}" "{self.replace}"{DELIM}'

    def __repr__(self):
        return f'Statement(statement={self.statement}, string="{self.string}", replace="{self.replace}")'
