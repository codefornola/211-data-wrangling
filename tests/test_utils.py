import os
import pandas as pd
from io import BytesIO

from fixtures import df

from cleanup.utils import write_output_file, get_lat, get_lng


def test_write_output_file(df, mocker):
  # mocks & stubs
  mocker.patch.object(pd.DataFrame, 'to_excel')
  mocker.patch('os.makedirs')
  path_exists_mock = mocker.patch('os.path.exists')
  # it calls to_excel on the file
  filename = 'nondata/somefile.xlsx'
  write_output_file(df, filename)
  pd.DataFrame.to_excel.assert_called_once_with(filename)
  # it doesn't call os.makedirs when not prefixed with 'data'
  filename = 'nondata/somefile.xlsx'
  write_output_file(df, filename)
  os.makedirs.assert_not_called()
  # it doesn't call os.makedirs when prefixed with 'data' & exists
  filename = 'data/somefile.xlsx'
  path_exists_mock.return_value = True
  write_output_file(df, filename)
  os.makedirs.assert_not_called()
  # it calls os.makedirs when prefixed with 'data', but doesn't exist
  filename = 'data/somefile.xlsx'
  path_exists_mock.return_value = False
  write_output_file(df, filename)
  os.makedirs.assert_called_once_with('data')


def test_get_lat():
    assert isinstance(get_lat("70471"), float)  # valid zip
    assert get_lat("00000") is None             # invalid zip
    assert get_lat(None) is None                # null zip


def test_get_lng():
    assert isinstance(get_lng("70471"), float)  # valid zip
    assert get_lng("00000") is None             # invalid zip
    assert get_lng(None) is None                # null zip
