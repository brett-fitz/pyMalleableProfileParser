import logging
from collections import OrderedDict
from typing import List, Tuple, OrderedDict as OrderedDictType
from mpp.options import Option
from mpp.statements import Statement
from mpp.blocks import Block
from mpp.constants import DELIM

# logger
logger = logging.getLogger('Parser')


class InvalidOption(ValueError):
    """invalid option format, expected: set [option] "[value]";"""


class InvalidBlock(ValueError):
    """invalid block found"""


class ParsingError(ValueError):
    """parsing error when reading profile"""


class Parser:

    @staticmethod
    def parse_config(profile: List):
        """
        Init Parser Object
        :param profile: List of lines read from a malleable c2 profile file
        """
        parsed_profile = {}

        i = 0
        while i < len(profile):
            # Blank line
            if profile[i].strip() == '':
                logger.info(f'skipping blank line: {i}')
                pass
            elif profile[i].strip()[0] == '#':
                logger.info(f'skipping comment line: {i}')
                pass
            # Option
            elif profile[i].strip()[:3] == 'set':
                option = _get_option(profile[i])
                parsed_profile[option.option] = option
            # Group
            elif profile[i].strip()[-1] == '{':
                block, displacement = _get_block(profile[i:])
                logger.info(f'found group: {block.name}')
                i += displacement
                parsed_profile[block.name] = block
            # Unknown
            else:
                raise ParsingError
            i += 1
        return parsed_profile


def _get_option(line: str) -> Option:
    """
    Parses an option in the following format:
        set [option] "[value]";
    :param line: String to parse
    :return: Tuple(option, value)
    """
    line = line.strip()
    if line[:3] != 'set' and line[-1] != ';':
        raise InvalidOption
    line = line.split(' "')
    option = line[0].strip().split()[1]
    value = line[1]
    if value[-2] != '"':
        raise InvalidOption
    logger.info(f'found option: {option} value: {value[:-2]}')
    return Option(option=option, value=value[:-2])


def _get_statement(line: str) -> Statement:
    """
    Parses a statement in the following formats:
        <statement>;
            or
        <statement> "value";
    :param line:
    :return: Statement
    """
    # TODO better handling of Headers and Parameters
    # TODO (BUG!) better handling of byte objects
    # TODO (BUG!) better handling of multiline values
    line = line.split()
    statement = line[0]
    value = ' '.join(line[1:])[:-1]
    if statement[-1] == DELIM:
        statement = statement[:-1]
    logger.info(f'found statement: {statement} value: {value}')
    return Statement(statement=statement, value=value)


def _get_block(lines: List) -> Tuple[Block, int]:
    block = Block(
        name=lines[0].strip().split(' ')[0],
        data=OrderedDict()
    )
    i = 1
    while i < len(lines):
        # Blank line / Comment
        if lines[i].strip() == '':
            pass
        # End of group
        elif lines[i].strip() == '}':
            return block, i
        # Subgroup
        elif lines[i].strip()[-1] == '{':
            sub_block, displacement = _get_block(lines[i:])
            block.data[sub_block.name] = sub_block
            i += displacement
        # Option
        elif lines[i].strip()[:3] == 'set':
            option = _get_option(lines[i])
            block.data[option.option] = option
        # Generic Statement
        elif lines[i].strip()[-1] == ';':
            statement = _get_statement(lines[i].strip())
            block.data[statement.statement] = statement
        i += 1
    # If we got here, then the block was not properly closed
    raise ParsingError


