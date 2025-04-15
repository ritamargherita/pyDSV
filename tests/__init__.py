# tests/test_csv_loader.py

import tempfile
import pandas as pd
from pyDSV.csvLoader import CSVLoader

def test_valid_csv():
    csv_content = "name,age\nAlice,30\nBob,25"
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        f.seek(0)
        loader = CSVLoader(f.name)
        df = loader.load_to_dataframe()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2, 2)