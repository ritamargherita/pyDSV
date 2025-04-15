import pytest
import tempfile
import os
from pyDSV.csvLoader import CSVLoader
import pandas as pd

@pytest.fixture
def sample_csv_loader():
    """
    Fixture to create a CSVLoader instance with a temporary file.
    """
    with tempfile.NamedTemporaryFile(mode='w', newline='', delete=False) as temp_csv_file:
        temp_csv_file.write("col1,col2,col3\n")
        temp_csv_file.write("1,2,3\n")
        temp_csv_file.write("4,5,6\n")
        temp_csv_file_path = temp_csv_file.name
    loader = CSVLoader(temp_csv_file_path)
    yield loader
    os.remove(temp_csv_file_path)

def test_is_csv_valid(sample_csv_loader):
    assert sample_csv_loader.is_csv_valid() is True

def test_load_to_dataframe(sample_csv_loader):
    assert isinstance(sample_csv_loader.df, pd.DataFrame)
    assert sample_csv_loader.df.shape == (2, 3)
    assert "col1" in sample_csv_loader.df.columns
    assert "col2" in sample_csv_loader.df.columns
    assert "col3" in sample_csv_loader.df.columns

def test_missing_column_headers():
    with tempfile.NamedTemporaryFile(mode='w', newline='', delete=False) as temp_csv_file:
        temp_csv_file.write("col1,,col3\n")
        temp_csv_file.write("1,2,3\n")
        temp_csv_file.write("4,5,6\n")
        temp_csv_file_path = temp_csv_file.name
    with pytest.raises(ValueError):
        CSVLoader(temp_csv_file_path)
    os.remove(temp_csv_file_path)

def test_malformed_csv():
    with tempfile.NamedTemporaryFile(mode='w', newline='', delete=False) as temp_csv_file:
        temp_csv_file.write("col1,col2,col3\n")
        temp_csv_file.write("1,2\n")
        temp_csv_file.write("4,5,6\n")
        temp_csv_file_path = temp_csv_file.name
    with pytest.raises(ValueError):
        CSVLoader(temp_csv_file_path)
    os.remove(temp_csv_file_path)

def test_non_existent_file():
    with pytest.raises(ValueError):
        CSVLoader("non_existent_file.csv")