import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from get_statistics import *

## pasar un frame sencillisimo y ver que está pasando
def test_getRGBWeights():
    assert getRGBWeights()
