import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../lib')

from get_rgb_difference import *

## pasar un frame sencillisimo y ver que está pasando
def test_getRGBWeights():
    # define array
    # test it is accounted as expected
    frame = np.array(
        [[[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]],
        [[255,0,0],[255,0,0],[255,0,0]]]
        )
    assert getRGBWeights(frame) == {'R': 255, 'G': 0, 'B': 0}

    frame = np.array(
        [[[255,100,10],[255,100,10],[255,100,10]],
        [[255,100,10],[255,100,10],[255,100,10]],
        [[255,100,10],[255,100,10],[255,100,10]]]
        )
    assert getRGBWeights(frame) == {'R': 255, 'G':100, 'B': 10}
