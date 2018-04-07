import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../lib')

from chromatic_distance import *

## pasar un frame sencillisimo y ver que está pasando
def test_getDistanceRGB():
    # define array
    # test it is accounted as expected
    frame = np.array(
        [[[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]]]
        )
    frame2 = np.array(
        [[[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,1]]]
        )
    assert getDistanceRGB(frame, frame2) == 1

def test_getDistanceHSV():
    # define array
    # test it is accounted as expected
    frame = np.array(
        [[[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]]]
        )
    frame2 = np.array(
        [[[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,1]]]
        )
    assert getDistanceHSV(frame, frame2, useHueOnly=False) == 1

    frame = np.array(
        [[[360,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]]]
        )
    frame2 = np.array(
        [[[0,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]]]
        )
    assert getDistanceHSV(frame, frame2, useHueOnly=False) == 0
