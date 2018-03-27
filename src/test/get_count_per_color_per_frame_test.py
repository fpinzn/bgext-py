import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../lib')

import pytest
import numpy as np
from get_count_per_color_per_frame import *

def test_get_pixel_count_per_color_in_frame():
    frame = np.array(
        [[[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]]]
    )
    assert get_pixel_count_per_color_in_frame(frame) == {'0000ff': 9}

    frame = np.array(
        [[[255,0,0],[15,0,0],[15,0,0]],
        [[15,0,0],[15,0,0],[255,17,17]],
        [[255,17,17],[255,17,17],[254,0,0]]]
    )
    print(get_pixel_count_per_color_in_frame(frame))
    assert get_pixel_count_per_color_in_frame(frame) == {'0000ff': 1, '00000f': 4, '1111ff': 3, '0000fe': 1}


def get_hex_from_decimal_bgr():
    assert '000000' == get_hex_from_decimal_rgb(np.array([0,0,0]))
    assert 'ffffff' == get_hex_from_decimal_rgb(np.array([255,255,255]))
    assert '0000ff' == get_hex_from_decimal_rgb(np.array([0,255,0]))
    assert '140000' == get_hex_from_decimal_rgb(np.array([0,0,20]))

def test_format_json():
    assert '[{"color":"ff0000","count":1},{"color":"0f0000","count":4},{"color":"ff1111","count":3}]' == format_json({'ff0000': 1, '0f0000': 4, 'ff1111': 3})
