import logging
from typing import List, Tuple, Dict

# logger
logger = logging.getLogger('Parser')


class InvalidOption(ValueError):
    """invalid option format, expected: set [option] "[value]";"""


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
                option, value = _get_option(profile[i])
                parsed_profile[option] = value
            # Group
            elif profile[i].strip()[-1] == '{':
                name, group, displacement = _get_group(profile[i:])
                logger.info(f'found group: {name}')
                i += displacement
                parsed_profile[name] = group
            # Unknown
            else:
                raise ParsingError
            i += 1
        return parsed_profile


def _clean_list(l: List):
    for i in l:
        if i == '':
            del i
    return l


def _get_option(line: str) -> Tuple:
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
    return option, value[:-2]


def _get_group(lines: List) -> Tuple[str, Dict, int]:
    name = lines[0].strip().split(' ')[0]
    group = {'statements': []}
    i = 1
    while i < len(lines):
        # Blank line / Comment
        if lines[i].strip() == '':
            pass
        # End of group
        elif lines[i].strip() == '}':
            return name, group, i
        # Subgroup
        elif lines[i].strip()[-1] == '{':
            subgroup_name, subgroup, displacement = _get_group(lines[i:])
            group[subgroup_name] = subgroup
            i += displacement
        # Option
        elif lines[i].strip()[:3] == 'set':
            option, value = _get_option(lines[i])
            group[option] = value
        # Generic Statement
        elif lines[i].strip()[-1] == ';':
            group['statements'].append(lines[i].strip())
        i += 1


