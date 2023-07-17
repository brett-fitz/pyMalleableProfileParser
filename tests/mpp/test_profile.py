""" Testing: mpp.profile
"""
from typing import Dict

import git
import pytest

from mpp.profile import MalleableProfile, get_attr_recursively


path = f'{git.Repo(__file__, search_parent_directories=True).working_tree_dir}/tests/data/'


@pytest.mark.parametrize(
    "profile,mapping",
    [
        (
            'amazon.profile',
            {
                'jitter.value': '0',
                'http_get.uri.value': '/s/ref=nb_sb_noss_1/167-3294888-0262949/field-keywords=books',
                'http_get.client.Host.value': 'www.amazon.com',
                'http_get.client.Accept.value': '*/*',
                'http_post.client.Accept.value': '*/*',
                'http_post.client.dc_ref.value': 'http%3A%2F%2Fwww.amazon.com',
                'http_post.server.X_Frame_Options.value': 'SAMEORIGIN'
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
                'http_config.headers.value': 'Content-Type, Connection, Server, Link, X-Cache',
                'http_config.Link.value': "<https://newsnetwork.mayoclinic.org/wp-json/>; rel=\\\"https://api.w.org/\\\"",
                'http_get.uri.value': '/discussion/mayo-clinic-radio-als/ /discussion/ /hubcap/mayo-clinic-radio-full-shows/ /category/research-2/',
                'http_get.client.Accept.value': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
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
    profile = MalleableProfile.from_file(filename=path + profile)
    for attribute, value in mapping.items():
        assert get_attr_recursively(
            profile=profile,
            attribute=attribute
        ) == value
    assert profile.validate()
