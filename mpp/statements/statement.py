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
            return f'{self.statement} {self.value}{DELIM}'
        return f'{self.statement}{DELIM}'
