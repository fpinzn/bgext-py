import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../lib')

import pytest
import anvil2frames
import numpy as np

anvil_test_file = os.path.join(os.path.dirname(__file__), 'fixtures', 'anvil-annotation-file.xml')

def test_get_breaks_with_time_from_anvil_file_path():
    result = anvil2frames.get_breaks_with_time_from_anvil_file_path(anvil_test_file)
    assert result == [('clean break', '11.76'), ('clean break', '12.88'), ('clean break', '15'), ('clean break', '17.04'), ('clean break', '18.04'), ('clean break', '19.4')]

def test_convert_time_to_frame ():
    assert 25 == anvil2frames.convert_time_to_frame(1, 25)

def test_convert_breaks_with_time_dict_to_frame_csv_text ():
    break_list = [('clean break', '11.76'), ('clean break', '12.88'), ('clean break', '15')]
    assert anvil2frames.convert_breaks_with_time_dict_to_frame_csv_text(break_list, 10) == "frame,break-type\n117,clean break\n128,clean break\n150,clean break\n"
