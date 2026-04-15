from arucutter.utils import area, AreaError#
import pytest
import numpy as np

def test_area():
    """ 
    A square with side of 100 has an area of 10000
    """
    rectangle1 = np.array([0,0,100,0,100,100,0,100], dtype=np.int32).reshape(4,2)
    #print(f"The area of the rectangle is: {area(rectangle1)}")
    assert area(rectangle1) == 10000.
    
def test_area2():
    """ 
    A skewed form raises an AreaError
    """
    rectangle2 = np.array([0,0,100,0,200,100,0,100], dtype=np.int32).reshape(4,2)
    with pytest.raises(AreaError):
        area(rectangle2)
