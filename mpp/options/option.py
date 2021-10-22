from typing import Set
from mpp.constants import DELIM


class Option:

    def __init__(self, option: str, value: str):
        self.option = option
        self.value = value

    def validate(self, valid_options: Set) -> bool:
        return self.option in valid_options

    def __str__(self):
        return f'set {self.option} "{self.value}"{DELIM}'

    def __repr__(self):
        return f'Option(option="{self.option}", value="{self.value}")'
