"""mpf module: Utils

Package-wide utility functions are stored here.
"""
import os
from pathlib import Path
from typing import List, Dict

def find_malleable_profiles() -> List[Dict[str, str]]:
    """Find directory locations for malleable profiles in submodules

    Returns:
        List of all the file locations for the malleable profiles from submodules
    """

    path = Path(__file__).resolve().parent.parent / 'data'
    sources = [source for source in path.iterdir() if source.is_dir()]
    
    profiles = {}
    for source in sources:
        found_profiles = [profile for profile in source.rglob('*') if str(profile).endswith('.profile')]
        if found_profiles:
            profiles[source.name] = found_profiles
    return profiles
