from typing import Union, List, Tuple
from mpp.constants import INVALID_OPTION, INVALID_TERMINATION_STATEMENT, INVALID_STATEMENT, INVALID_BLOCK, \
    DATA_TRANSFORM_BLOCKS, PROFILE, TERMINATION_STATEMENTS
from mpp.statements import Statement, HeaderParameter, StringReplace
from mpp.options import Option


class Block:

    def __init__(self, name: str, data: List, variant: str = None):
        self.name = name
        self.data = data
        # TODO Support variants
        self.variant = variant
        # TODO add properties to easily get options, statements, blocks

    def validate(
            self,
            name: str = ''
    ) -> Union[bool, List[Tuple]]:
        if name != '':
            name = name + '.' + self.name
        else:
            name = self.name
        valid_options = PROFILE[name]['options']
        valid_statements = PROFILE[name]['statements']
        valid_blocks = PROFILE[name]['blocks']
        i = 0
        invalid_values = []
        while i < len(self.data):
            if i == len(self.data) - 1 and self.name in DATA_TRANSFORM_BLOCKS:
                if self.data[i].statement not in TERMINATION_STATEMENTS:
                    invalid_values.append((self.data[i], INVALID_TERMINATION_STATEMENT))
                elif self.name == 'output' and self.data[i].statement != 'print' and 'client' not in name:
                    invalid_values.append((self.data[i], INVALID_TERMINATION_STATEMENT))
            elif isinstance(self.data[i], Statement) and self.data[i].statement not in valid_statements:
                invalid_values.append((self.data[i], INVALID_STATEMENT))
            elif isinstance(self.data[i], Option) and self.data[i].option not in valid_options:
                invalid_values.append((self.data[i], INVALID_OPTION))
            elif isinstance(self.data[i], Block) and self.data[i].name not in valid_blocks:
                invalid_values.append((self.data[i], INVALID_BLOCK))
            elif isinstance(self.data[i], Block):
                tmp = self.data[i].validate(name=name)
                if isinstance(tmp, list):
                    invalid_values += tmp
            i += 1
        if invalid_values:
            return invalid_values
        return True

    def __getattr__(self, item):
        # TODO return all matches for statements
        tmp = item.replace('_', '-')
        for i in self.data:
            if isinstance(i, Block):
                if tmp == i.name or item == i.name:
                    return i
            elif isinstance(i, Option):
                if tmp == i.option or item == i.option:
                    return i
            elif isinstance(i, HeaderParameter):
                if tmp == i.key or item == i.key:
                    return i
            elif isinstance(i, StringReplace):
                if tmp == i.string or item == i.string:
                    return i
            elif isinstance(i, Statement):
                if i.value == '':
                    if tmp == i.statement or item == i.statement:
                        return i
                else:
                    if tmp == i.value or item == i.value:
                        return i

    def __str__(self):
        if self.variant:
            return f'{self.name} "{self.variant}" {self.data}'
        return f'{self.name} {self.data}'

    def __repr__(self):
        return f'Block(name={self.name}, data={self.data})'

