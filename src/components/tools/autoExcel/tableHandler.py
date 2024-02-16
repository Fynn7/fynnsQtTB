import numpy as np
import pandas as pd
# from openpyxl import load_workbook

def peak_unique(df: pd.DataFrame, col: str) -> list:
    '''
    return a list of unique values in the column
    aka: return all *classes of values* in the column
    usage:
    to check if there are any typos in the column
    '''
    return df[col].unique().tolist()