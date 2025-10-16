import pandas as pd
from fastapi import UploadFile
from io import StringIO

def read_csv_file(file: UploadFile):
    """Reads uploaded CSV file and returns a pandas DataFrame."""
    content = file.file.read().decode("utf-8")
    df = pd.read_csv(StringIO(content))
    return df
