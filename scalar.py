import pandas as pd

def to_scalar(val):
    """
    Convert a pandas Series (even with multiple values) or a scalar to float.
    If Series, use the first value.
    """
    if isinstance(val, pd.Series):
        return float(val.iloc[0])
    return float(val)