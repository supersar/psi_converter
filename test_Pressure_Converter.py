import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from io import StringIO
from Pressure_Converter import Pressure_Converter

@pytest.fixture
def test_Converter():
  converter = Pressure_Converter(verbose=False)
  return converter

def test_process_input(test_Converter):
    df_in = pd.DataFrame({"Time": [0,1,2,3,4],"Pressure": [91.52037548876822,79.77002316771555,99.596815564853,50.778787424214315,86.8388267217223]})
    expected = pd.DataFrame({
      "t":[0,1,2,3,4],
      "tmp":[59.3103623691,53.0321493302,63.3217031259,34.4421089306,56.876498645],
      "inrange":["None",False,True,False,True],
      "cooling":["None",True,False,True,False]
    })
    result = test_Converter._process_input(df_in)
    
    assert_frame_equal(result, expected)
