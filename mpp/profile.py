"""mpp module: Profile
"""
import logging
import re
from typing import Any, Dict, List, Tuple, Union

import regex

from mpp.blocks import Block
from mpp.constants import (DNS_BEACON_OPTIONS, GLOBAL_OPTIONS, INVALID_BLOCK,
                           INVALID_OPTION, INVALID_VARIANT, PROFILE_BLOCKS,
                           PROFILE_VARIANTS)
from mpp.options import Option


# logger
logger = logging.getLogger('MalleableProfile')


__all__ = [
    "BlockNotFound",
    "get_attr_recursively",
    "MalleableProfile",
    "OptionNotFound"
]


class OptionNotFound(KeyError):
    """option was not found in the profile"""


class BlockNotFound(KeyError):
    """block was not found in the profile"""


class MalleableProfile:
    """MalleableProfile Class
    """

    def __init__(self, profile: Union[str, Dict]):
        """Init Class Object

        Usage:
            Starting with mpp v0.4, users should leverage the class
            methods to initialize a class object. Backwards compatibility
            exists for filenames.

        Args:
            profile: Filename to open and parse or profile dict.
            

        Raises:
            FileNotFoundError: _description_
        """
        if isinstance(profile, dict):
            self.profile = profile
        elif isinstance(profile, str):
            if '{' in profile:
                self.profile = self.from_string(string=profile)
            else:
                self.profile = self.from_file(filename=profile).profile
        else:
            raise TypeError(profile)

    def __str__(self):
        return "\n".join(
            [
                str(item)
                for key, item in self.profile.items()
            ]
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        """Parse a Malleable Profile from bytes

        Args:
            profile: Malleable Profile in bytes

        Returns:
            MalleableProfile object
        """
        return cls.from_string(string=data.decode('utf-8'))

    @classmethod
    def from_file(cls, filename: str):
        """Parse Malleable Profile from file

        Args:
            profile: Filename
        
        Returns:
            MalleableProfile object
        """
        with open(file=filename, mode='r', encoding='utf-8') as file:
            return cls.from_string(string=file.read())

    @classmethod
    def from_string(cls, string: str) -> Dict:
        """Parse a Malleable Profile from a string and return
        a dictionary object containing a mapping of keys to
        objects. An object can be a Block, Statement, or Option.

        Args:
            profile: Malleable Profile.

        Returns:
            Parsed profile mapping.
        """
        profile = {}

        # Get global options
        options = Option.from_string(
            string="".join(
                [
                    item
                    for item in regex.split(Block.NON_BLOCK_DATA_REGEX, string, flags=re.MULTILINE | re.DOTALL)
                    if item is not None
                ]
            )
        )
        if options:
            for option in options:
                profile[option.option] = option

        # Loop through root blocks
        blocks = regex.finditer(Block.BLOCK_REGEX, string, flags=re.MULTILINE | re.DOTALL)
        for match in blocks:
            profile[match.groups()[0]] = Block.from_string(string=match.group())

        # Return class object
        return cls(
            profile=profile
        )

    def validate(self, version: int = 4.0) -> Union[bool, List[Tuple]]:
        """Validate a Malleable Profile

        Args:
            version: Minimum version compliance (Default: 4.0)

        Returns:
            _description_
        """
        keys = [*self.profile]
        invalid_values = []
        for i in keys:
            # blocks
            if isinstance(self.profile[i], Block) and self.profile[i].name not in PROFILE_BLOCKS:
                invalid_values.append((self.profile[i], INVALID_BLOCK))
            elif isinstance(self.profile[i], Block) and self.profile[i].name in PROFILE_BLOCKS:
                # check if variant and if allowed
                if self.profile[i].variant:
                    if self.profile[i] not in PROFILE_VARIANTS:
                        invalid_values.append((self.profile[i], INVALID_VARIANT))
                tmp = self.profile[i].validate()
                if isinstance(tmp, List):
                    invalid_values += tmp
            elif isinstance(self.profile[i], Option) and self.profile[i].option not in GLOBAL_OPTIONS:
                # check if dns-beacon option (4.0-4.2)
                if self.profile[i].option in DNS_BEACON_OPTIONS:
                    if version >= 4.3:
                        invalid_values.append((self.profile[i], INVALID_OPTION))
                    else:
                        logger.warning(f'starting with v4.3, dns options have been moved into \'dns-beacon\' block: '
                                       f'{self.profile[i].option}')
        if invalid_values:
            return invalid_values
        return True

    def __getattr__(self, item):
        try:
            return self.profile[item.replace('_', '-')]
        except KeyError:
            return self.profile[item]


def get_attr_recursively(profile, attribute: str) -> Any:
    """Recursive implementation to get a profile attribute.

    Args:
        profile: _description_
        attribute: _description_

    Returns:
        _description_
    """
    attributes = attribute.split('.')
    if len(attributes) > 1:
        return get_attr_recursively(
            getattr(profile, attributes[0]),
            attribute=attribute[len(attributes[0]) + 1:]
        )
    return getattr(profile, attributes[0])
