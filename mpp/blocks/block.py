from typing import Dict
from typing import Union, List, Tuple
from mpp.constants import INVALID_OPTION, DATA_TRANSFORM_STATEMENTS, TERMINATION_STATEMENTS, \
    INVALID_TRANSFORM_STATEMENT, INVALID_TERMINATION_STATEMENT, INVALID_STATEMENT, INVALID_BLOCK


class Block:

    def __init__(self, data: Dict):
        self.data = data

    def __getattr__(self, item):
        return self.data[item.replace('_', '-')]


class BlockWithOptions(Block):
    VALID_OPTIONS = set()

    def validate(self) -> Union[bool, List[Tuple]]:
        options = self.data.keys()
        invalid_options = []
        for option in options:
            if option not in self.VALID_OPTIONS:
                invalid_options.append((option, INVALID_OPTION))
        if invalid_options:
            return invalid_options
        return True


class BlockWithStatements(Block):
    VALID_STATEMENTS = set()

    def validate(self) -> Union[bool, List[Tuple]]:
        statements = [*self.data]
        i = 0
        invalid_values = []
        while i < len(statements):
            if statements[i] not in self.VALID_STATEMENTS:
                invalid_values.append((statements[i], INVALID_STATEMENT))
            i += 1
        if invalid_values:
            return invalid_values
        return True


class BlockWithSubBlocks(BlockWithStatements):
    VALID_BLOCKS = set()

    def validate(self) -> Union[bool, List[Tuple]]:
        data = [*self.data]
        i = 0
        invalid_values = []
        while i < len(data):
            if data[i] not in self.VALID_STATEMENTS:
                if data[i] not in self.VALID_BLOCKS and isinstance(self.data[data[i]], Block):
                    invalid_values.append((data[i], INVALID_BLOCK))
                invalid_values.append((data[i], INVALID_STATEMENT))
            i += 1
        if invalid_values:
            return invalid_values
        return True


class TransformBlock(Block):
    VALID_TERMINATION_STATEMENTS = TERMINATION_STATEMENTS

    def validate(self) -> Union[bool, List[Tuple]]:
        statements = [*self.data]
        i = 0
        invalid_values = []
        while i < len(statements):
            if i == len(statements) - 1:
                if statements[i] not in self.VALID_TERMINATION_STATEMENTS:
                    invalid_values.append((statements[i], INVALID_TERMINATION_STATEMENT))
                    return invalid_values
            elif statements[i] not in DATA_TRANSFORM_STATEMENTS:
                invalid_values.append((statements[i], INVALID_TRANSFORM_STATEMENT))
            i += 1
        if invalid_values:
            return invalid_values
        return True
