import logging
from mpp.parser import Parser

# logger
logger = logging.getLogger('MalleableProfile')


class OptionNotFound(KeyError):
    """option was not found in the profile"""


class GroupNotFound(KeyError):
    """group was not found in the profile"""


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

    def __getattr__(self, item):
        return self.profile[item.replace('_', '-')]
