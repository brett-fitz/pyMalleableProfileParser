import logging
from mpp.parser import Parser
from mpp.constants import PROFILE_BLOCKS, PROFILE_VARIANTS, INVALID_VARIANT, INVALID_BLOCK, GLOBAL_OPTIONS, \
    INVALID_OPTION, DNS_BEACON_OPTIONS
from mpp.blocks import Block
from mpp.options import Option
from typing import List, Tuple, Union

# logger
logger = logging.getLogger('MalleableProfile')


class OptionNotFound(KeyError):
    """option was not found in the profile"""


class BlockNotFound(KeyError):
    """block was not found in the profile"""


class MalleableProfile:

    def __init__(self, profile: str):
        """
        Init class object
        :param profile: Path to malleable profile file
        """
        try:
            with open(profile, 'r') as file:
                self.profile = Parser.parse_config(file.read().splitlines())
        except FileNotFoundError:
            raise FileNotFoundError

    def validate(self, version: int = 4.0) -> Union[bool, List[Tuple]]:
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
