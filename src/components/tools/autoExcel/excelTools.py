import numpy as np
import pandas as pd
import os

def merge_excel(dir_path:str,save=False):
    # read all excel files in the directory
    files = os.listdir(dir_path)
    df = pd.DataFrame()
    for file in files:
        if file.endswith('.xlsx'):
            df = df._append(pd.read_excel(dir_path + file), ignore_index=True)
    # save the merged data to a new excel file
    if save:
        df.to_excel(dir_path + 'MERGED.xlsx', index=False)
    return df

def get_unique_rows(df:pd.DataFrame, col:str):
    '''
    Get unique rows from a dataframe based on a column
    '''
    return df.drop_duplicates(subset=col)

if __name__=='__main__':
    ...