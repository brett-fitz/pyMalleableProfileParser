"""mpf module: Finder
"""

import logging
from typing import Any, Dict, List, Tuple, Union
from mpf.utils import *
from mpp.profile import *
import os


# logger
logger = logging.getLogger('MalleableProfileFinder')

__all__ = [
    "MalleableProfileFinder",
    "SubmodulesNotLoaded",
]


class SubmodulesNotLoaded(Exception):
    """submodules not loaded"""
    def __init__(
            self, 
            message="Submodules are not instantiated, check the README for instructions on how to properly instantiate..."
        ) -> None:
        super().__init__(message)


class MalleableProfileFinder:
    """MalleableProfileFinder Class
    """

    def __init__(self, profile: Dict[str, str] = None, profile_dir: str = None) -> List['str']:
        """Init Class Object

        Usage:
            If you have a set of profile features ready in a dictionary, pass them into 'profile',
            otherwise you can dynamically set settings after instantiation.
        
        Args:
            profile: A dictionary containing profile settings the user wishes to search
            known malleable profiles for
            profile_dir: Custom directory with '.profile' files to be laoded in addition to the submodules 

        Returns:
            List of filenames from 'data' directory indicating matched profiles
        """
        
        #  TODO: custom profile directory support
        # if profile_dir:
        #     find_malleable_profiles(profile_dir)

        self.malleable_profiles = self.load_profiles()

        self.search_profile = profile


    @staticmethod
    def load_profiles(profile_files: Dict[str, List[Union[os.PathLike, str]]] = None) -> Dict:
        """Parses a list of malleable profile files and returns MalleableProfile objects

        Args:
            profile_files: List of all profile files to be parsed and loaded

        Returns:
            Dictionary of parsed profiles with a key of the repository/submodule they came from
        """

        if not profile_files:
            profile_files = find_malleable_profiles()
            if not profile_files:
                raise(SubmodulesNotLoaded())
        
        print(profile_files)
        parsed_profiles = {}
        for source, files in profile_files.items():
            for file in files:
                profile = MalleableProfile(profile=file)
                if not parsed_profiles.get(source):
                    parsed_profiles[source] = {}

                parsed_profiles[source][file] = profile
        
        return parsed_profiles

    #def find_profile