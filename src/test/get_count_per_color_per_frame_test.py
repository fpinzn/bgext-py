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
    assert get_pixel_count_per_color_in_frame(frame) == {'ff0000': 9}

    frame = np.array(
        [[[255,0,0],[15,0,0],[15,0,0]],
        [[15,0,0],[15,0,0],[255,17,17]],
        [[255,17,17],[255,17,17],[254,0,0]]]
    )
    print(get_pixel_count_per_color_in_frame(frame))
    assert get_pixel_count_per_color_in_frame(frame) == {'ff0000': 1, '0f0000': 4, 'ff1111': 3, 'fe0000': 1,}


def test_get_hex_from_decimal_rgb():
    assert '000000' == get_hex_from_decimal_rgb(np.array([0,0,0]))
    assert 'ffffff' == get_hex_from_decimal_rgb(np.array([255,255,255]))
    assert '00ff00' == get_hex_from_decimal_rgb(np.array([0,255,0]))
    assert '000014' == get_hex_from_decimal_rgb(np.array([0,0,20]))
