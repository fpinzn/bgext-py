import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../lib')

import pytest
from util import *
import numpy as np

def test_write_to_file(tmpdir):
    data = 'hola'
    temp_file = tmpdir.mkdir("sub").join("hello.txt")
    print(str(temp_file))
    write_to_file(data, os.path.abspath(temp_file))
    assert temp_file.read() == data

def test_format_csv():
    # asserts is passed a dictionary
    with pytest.raises(Exception):
        format_csv(1,2,3)

    # asserts all arrays are the same size
    with pytest.raises(Exception):
        format_csv({
            'R': np.array([1,2,3,4]),
            'G': np.array([5,6,7,8]),
            'B': np.array([9,0,1])
        })

    # happy path
    counter = {
        'R': np.array([1,2,3,4]),
        'G': np.array([5,6,7,8]),
        'B': np.array([9,0,1,2])
    }
    assert format_csv(counter) == 'frame,R,G,B\n0,1,5,9\n1,2,6,0\n2,3,7,1\n3,4,8,2'

def test_calc_diffs():
    counter = {
        'R': np.array([1,2,3,4]),
        'G': np.array([5,6,7,8]),
        'B': np.array([9,0,1,2])
    }
    result = calc_diffs(counter)
    assert np.array_equal(result['R'], [0,1,1,1])
    assert np.array_equal(result['G'], [0,1,1,1])
    assert np.array_equal(result['B'], [0,-9,1,1])

def test_prefix_dict_keys():
    initial = {'a':1, 'b': 2, 'c': 3}
    final = {'prea':1, 'preb': 2, 'prec': 3}
    assert prefix_dict_keys(initial, 'pre') == final
