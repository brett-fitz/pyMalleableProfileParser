"""mpp.blocks module: block
"""
import logging
import re
from typing import List, Tuple, Union

import regex

from mpp.constants import (DATA_TRANSFORM_BLOCKS, INVALID_BLOCK,
                           INVALID_OPTION, INVALID_STATEMENT,
                           INVALID_TERMINATION_STATEMENT, PROFILE,
                           TERMINATION_STATEMENTS)
from mpp.options import Option
from mpp.statements import HeaderParameter, Statement, StringReplace


__all__ = [
    "Block"
]


logger = logging.getLogger(__name__)


class Block:
    """Block Class
    """
    # Regex to parse blocks with support for variants
    # https://hstechdocs.helpsystems.com/manuals/cobaltstrike/current/userguide/content/topics/malleable-c2_profile-variants.htm
    BLOCK_REGEX = r'^\s*([\w\-\_]+)\s*(?:"([\w\s]+)"\s*)?(\{(?:[^{}"\']+|\'(?:[^\']+|\\.)*\'|"(?:[^"\\]+|\\.)*"|(?R))*\})'
    NON_BLOCK_DATA_REGEX = r'\{(?:[^{}"\']+|\'(?:[^\']+|\\.)*\'|"(?:[^"\\]+|\\.)*"|(?R))*\}'

    def __init__(self, name: str, data: List, variant: str = None):
        self.name = name
        self.data = data
        # TODO Support variants
        self.variant = variant
        # TODO add properties to easily get options, statements, blocks

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

    def __str__(self, depth: int = 1):
        def generate_string(obj, curr_depth):
            indentation = '\t' * curr_depth
            if isinstance(obj, Block):
                name = f'{obj.name} "{obj.variant}"' if obj.variant else obj.name
                block_data = [generate_string(item, curr_depth + 1) for item in obj.data]
                block_string = f"\n{indentation}".join(block_data)
                return f'{name} {{\n{indentation}{block_string}\n{indentation[:-1]}}}'
            return str(obj)
        return generate_string(self, depth)

    def __repr__(self):
        return f'Block(name={self.name}, data={self.data})'

    @property
    def options(self) -> List:
        """Get all options in the root block

        Returns:
            _description_
        """
        return [
            item
            for item in self.data
            if isinstance(item, Option)
        ]

    @property
    def statements(self) -> List:
        """Get all statements in the root block

        Returns:
            _description_
        """
        return [
            item
            for item in self.data
            if isinstance(item, Statement)
        ]

    @classmethod
    def from_string(cls, string: str):
        """Parse a block and its nested blocks from a string in the following format:
            name "<optional variant>" { 
                data
            }

        Args:
            string: _description_

        Returns:
            _description_
        """
        data = []

        # Get block
        block = regex.search(Block.BLOCK_REGEX, string, flags=re.MULTILINE | re.DOTALL)
        if block:
            logger.info(f'found block in string: {string}')
            # Get Non block data
            non_block_data = "".join(
                [
                    item
                    for item in regex.split(Block.NON_BLOCK_DATA_REGEX, block.groups()[2].strip()[1:-1], flags=re.MULTILINE)
                    if item is not None
                ]
            )
            logger.info(f'non-block data: {non_block_data}')
            # Get Options
            data += Option.from_string(string=non_block_data)

            # Get statements
            data += Statement.from_string(string=non_block_data)
            data += HeaderParameter.from_string(string=non_block_data)
            data += StringReplace.from_string(string=non_block_data)

            # Get nested block
            for nested_block in regex.finditer(
                pattern=Block.BLOCK_REGEX,
                string=block.groups()[2],
                flags=re.MULTILINE | re.DOTALL
            ):
                if nested_block:
                    data.append(cls.from_string(string=nested_block.group()))
        else:
            logger.warning(f'did not find a valid block in string:{string}')
            return None

        return cls(
            name=block.groups()[0],
            data=data,
            variant=block.groups()[1]
        )

    def validate(
            self,
            name: str = ''
    ) -> Union[bool, List[Tuple]]:
        """Validate a block and it's sub-blocks

        Args:
            name: Name of the block. Defaults to ''.

        Returns:
            _description_
        """
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
