""" Testing: Profile Parsing
"""
from typing import Dict

import git
import pytest

from mpp.profile import MalleableProfile, get_attr_recursively

path = f'{git.Repo(__file__, search_parent_directories=True).working_tree_dir}/tests/'


@pytest.mark.parametrize(
    "profile,mapping",
    [
        (
            'amazon.profile',
            {
                'jitter.value': '0',
                'http_get.client.Host.value': 'www.amazon.com'
            },
        ),
        (
            'bing_maps.profile',
            {
                'sleeptime.value': '38500',
                'http_get.client.metadata.base64.value': ''
            }
        ),
        (
            'mayoclinic.profile',
            {
                'useragent.value': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'stage.transform_x86.ReflectiveLoader.replace': ''
            }
        )
    ]
)
def test_profile_parsing_from_file(profile: str, mapping: Dict):
    """Test profile parsing from files

    Args:
        profile: Malleable Profile filename
        mapping: Mapping of expected keys and values
    """
    profile = MalleableProfile.parse_malleable_profile_from_file(profile=path + profile)
    for attribute, value in mapping.items():
        assert get_attr_recursively(
            profile=profile,
            attribute=attribute
        ) == value
    assert profile.validate()
