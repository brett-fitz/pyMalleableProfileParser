"""Testing: mpp.options.option
"""
from typing import Any, Set

import pytest

from mpp.constants import GLOBAL_OPTIONS, HTTP_OPTIONS
from mpp.options.option import Option

@pytest.mark.parametrize(
    "option,value,valid_options",
    [
        ("jitter", 0, GLOBAL_OPTIONS),
        ("uri", "/s/ref=nb_sb_noss_1/167-3294888-0262949/field-keywords=books", HTTP_OPTIONS)
    ]
)
def test_option(option: str, value: Any, valid_options: Set):
    """Test Option Class

    Args:
        option: _description_
        value: _description_
        valid_options: _description_
    """
    assert Option(option=option, value=value).validate(valid_options=valid_options)
