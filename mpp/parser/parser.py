import logging
from typing import List, Tuple
from mpp.options import Option
from mpp.statements import Statement, HeaderParameter, StringReplace
from mpp.blocks import Block
from mpp.constants import DELIM, STATEMENTS
import re

# logger
logger = logging.getLogger('Parser')

line_with_comment_regex = re.compile('(?<=;)\s*#.*')
block_with_comment_regex = re.compile('(?<={)\s*#.*')


class InvalidOption(ValueError):
    """invalid option format, expected: set [option] "[value]";"""


class InvalidStatement(ValueError):
    """invalid statement format, expected: [statement] <optional value>;"""


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
            # Comment Line
            elif profile[i].strip()[0] == '#':
                logger.info(f'skipping comment line: {i}')
            # Option
            elif profile[i].strip()[:3] == 'set':
                option = _get_option(profile[i])
                parsed_profile[option.option] = option
            # Group
            elif profile[i].strip()[-1] == '{':
                block, displacement = _get_block(profile[i:])
                i += displacement
                parsed_profile[block.name] = block
            elif block_with_comment_regex.search(profile[i].strip()):
                block, displacement = _get_block(profile[i:])
                i += displacement
            # Unknown
            else:
                print(profile[i])
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
    if line[:3] != 'set':
        raise InvalidOption
    if line[-1] != ';':
        match = line_with_comment_regex.search(line)
        if match:
            line = line[:match.span()[0]]
        else:
            raise InvalidOption
    line = line.split(' "')
    # cover tab separated values
    if len(line) == 1 and '\t"' in line[0]:
        line = line[0].split('\t"')
    # cover space after value
    if len(line) > 2:
        if line[2] == ';':
            line[1] = line[1] + '"' + line[2]
        else:
            raise InvalidOption
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
    # TODO (BUG!) better handling of byte objects
    line = line.strip()
    tmp = line.split()
    statement = tmp[0]
    value = line[len(statement):].strip()
    if value == '' and statement[-1] != DELIM:
        raise InvalidStatement
    elif value == '':
        statement = statement[:-1]
    elif value[-1] != DELIM:
        raise InvalidStatement
    else:
        value = value[:-1]
    if statement == 'parameter' or statement == 'header':
        if len(value.split(' "')) > 1:
            key = value.split(' "')[0].replace('"', '')
            value = value.split(' "')[1].replace('"', '')
            logger.info(f'found statement: {statement} key: {key} value: {value}')
            return HeaderParameter(statement=statement, key=key, value=value)
        value = value.replace('"', '')
        logger.info(f'found statement: {statement} value: {value}')
        return HeaderParameter(statement=statement, key=value)
    elif statement == 'strrep':
        line = value
        x = 1
        while x < len(line):
            if line[x] == '"' and line[x - 1] != '\\':
                string = line[:x + 1][1:-1]
                replace = line[x + 1:].strip()[1:-1]
                break
            x += 1
        try:
            return StringReplace(statement=statement, string=string, replace=replace)
        except NameError as e:
            raise InvalidStatement
    else:
        if len(value) > 0:
            if value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
        logger.info(f'found statement: {statement} value: {value}')
        return Statement(statement=statement, value=value)


def _get_block(lines: List) -> Tuple[Block, int]:
    # Throw away comment if found
    match = block_with_comment_regex.search(lines[0].strip())
    if match:
        lines[0] = lines[0].strip()[:match.span()[0]]
    # Parse name + variant if available
    line = lines[0].strip().split('{')[0].strip().split(' "')
    name = line[0]
    if len(line) == 2:
        variant = line[1][:-1]
    elif len(line) > 2:
        variant = line[1]
    else:
        variant = ''

    block = Block(
        name=name,
        data=[],
        variant=variant
    )
    logger.info(f'found block: {block.name}')

    i = 1
    while i < len(lines):
        # Blank line
        if lines[i].strip() == '':
            logger.info(f'skipping blank line: {i}')
        # Comment
        elif lines[i].strip()[0] == '#':
            logger.info(f'skipping comment line: {i}')
        # End of group
        elif lines[i].strip() == '}':
            logger.info(f'end of block: {block.name}')
            return block, i
        # Option
        elif lines[i].strip()[:3] == 'set':
            option = _get_option(lines[i])
            block.data.append(option)
        # Generic Statement
        elif lines[i].strip().replace(';', '').split()[0] in STATEMENTS:
            # Single line statement
            if lines[i].strip()[-1] == ';':
                statement = _get_statement(lines[i].strip())
            # Single line statement with comment
            elif line_with_comment_regex.search(lines[i].strip()):
                match = line_with_comment_regex.search(lines[i].strip())
                statement = _get_statement(lines[i].strip()[:match.span()[0]])
            else:
                # Multi line statement
                statement_lines = ''
                while i < len(lines):
                    if lines[i].strip()[-2:] == '";' and lines[i].strip()[-3:] != '\\";':
                        statement_lines += lines[i]
                        break
                    else:
                        statement_lines += lines[i]
                        i += 1
                statement = _get_statement(statement_lines.strip())
            block.data.append(statement)
        # Subgroup
        elif lines[i].strip()[-1] == '{' and lines[i].strip()[-2:] != '"{':
            sub_block, displacement = _get_block(lines[i:])
            block.data.append(sub_block)
            i += displacement
        elif block_with_comment_regex.search(lines[i].strip()):
            match = block_with_comment_regex.search(lines[i].strip())
            lines[i] = lines[i].strip()[:match.span()[0]]
            sub_block, displacement = _get_block(lines[i:])
            block.data.append(sub_block)
            i += displacement
        i += 1
    # If we got here, then the block was not properly closed
    raise ParsingError


