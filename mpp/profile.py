import logging
from mpp.parser import Parser
from mpp.constants import PROFILE_BLOCKS, PROFILE_VARIANTS, INVALID_VARIANT, INVALID_BLOCK, GLOBAL_OPTIONS, \
    INVALID_OPTION, DNS_BEACON_OPTIONS, HTTP_CONFIG_OPTIONS, HTTP_CONFIG_STATEMENTS, HTTP_OPTIONS, HTTP_BLOCKS
from mpp.blocks import Block
from mpp.options import Option
from typing import List, Tuple

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

    def validate(self, version: int = 4.0):
        keys = [*self.profile.keys()]
        invalid_values = []
        for i in keys:
            # blocks
            if isinstance(self.profile[i], Block) and self.profile[i] not in PROFILE_BLOCKS:
                invalid_values.append((self.profile[i], INVALID_BLOCK))
            elif isinstance(self.profile[i], Block) and self.profile[i] in PROFILE_BLOCKS:
                # check if variant and if allowed
                if self.profile[i].variant:
                    if self.profile[i] not in PROFILE_VARIANTS:
                        invalid_values.append((self.profile[i], INVALID_VARIANT))
                tmp = self.profile[i].validate()
                if isinstance(tmp, List):
                    invalid_values += tmp
            elif isinstance(self.profile[i], Option) and self.profile[i] not in GLOBAL_OPTIONS:
                # check if dns-beacon option (4.0-4.2)
                if self.profile[i] in DNS_BEACON_OPTIONS:
                    if version >= 4.3:
                        invalid_values.append((self.profile[i], INVALID_OPTION))

    def __getattr__(self, item):
        return self.profile[item.replace('_', '-')]
