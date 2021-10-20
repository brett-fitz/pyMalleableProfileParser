from typing import Union, List, Tuple, Set, OrderedDict
from mpp.constants import INVALID_OPTION, INVALID_TERMINATION_STATEMENT, INVALID_STATEMENT, INVALID_BLOCK, \
    DATA_TRANSFORM_BLOCKS, START_BLOCK_DELIM, END_BLOCK_DELIM, PROFILE
from mpp.statements import Statement
from mpp.options import Option


class Block:

    def __init__(self, name: str, data: OrderedDict, variant: str = None):
        self.name = name
        self.data = data
        # TODO Support variants
        self.variant = variant
        # TODO add properties to easily get options, statements, blocks

    def validate(
            self,
            name: str = ''
    ) -> Union[bool, List[Tuple]]:
        name = self.name + '.' + name
        if name[-1] == '.':
           name = name[:-1]
        valid_options = PROFILE[name]
        valid_statements = PROFILE[name]
        valid_blocks = PROFILE[name]
        keys = [*self.data]
        i = 0
        invalid_values = []
        while i < len(keys):
            if i == len(keys) - 1 and self.name == DATA_TRANSFORM_BLOCKS:
                if keys[i] not in self.VALID_TERMINATION_STATEMENTS:
                    invalid_values.append((keys[i], INVALID_TERMINATION_STATEMENT))
                elif self.name == 'output' and keys[i] != 'print':
                    invalid_values.append((keys[i], INVALID_TERMINATION_STATEMENT))
            elif isinstance(self.data[keys[i]], Statement) and keys[i] not in valid_statements:
                invalid_values.append((self.data[keys[i]], INVALID_STATEMENT))
            elif isinstance(self.data[keys[i]], Option) and keys[i] not in valid_options:
                invalid_values.append((self.data[keys[i]], INVALID_OPTION))
            elif isinstance(self.data[keys[i]], Block) and keys[i] not in valid_blocks:
                invalid_values.append((self.data[keys[i]], INVALID_BLOCK))
            elif isinstance(self.data[keys[i]], Block):
                tmp = self.data[keys[i]].validate(name=name)
                if isinstance(tmp, list):
                    invalid_values += tmp
            i += 1
        if invalid_values:
            return invalid_values
        return True

    def __getattr__(self, item):
        return self.data[item.replace('_', '-')]

    def __str__(self):
        if self.variant:
            return f'{self.name} "{self.variant}" {self.data}'
        return f'{self.name} {self.data}'

    def __repr__(self):
        return f'Block(name={self.name}, data={self.data})'

