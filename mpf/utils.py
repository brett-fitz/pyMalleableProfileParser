"""mpf module: Utils

Package-wide utility functions are stored here.
"""
import os
from pathlib import Path
from typing import List

def find_malleable_profiles() -> List[str]:
    """Find directory locations for malleable profiles in submodules

    Returns:
        List of all the file locations for the malleable profiles from submodules
    """

    path = Path(__file__).resolve().parent.parent / 'data'
    profiles = path.rglob('*')
    profiles = [file for file in profiles if str(file).endswith('.profile')]
    return profiles
