import numpy as np
import pandas as pd
import traceback

from ...templates.fynnsComponents import _select_file, _save_file


class DataHandler:
    '''
    Handle data cleaning, analysis, and visualization
    '''

    def __init__(self) -> None:
        pass

    def clean(cls, df: pd.DataFrame):
        pass

    def analyze(cls, df: pd.DataFrame):
        pass


class FileConverter:
    '''
    Convert data to different file formats
    '''

    def __init__(self, df: pd.DataFrame) -> None:
        pass

    @staticmethod
    def read_data() -> pd.DataFrame | None:
        file_path = _select_file()
        # cut the file extension
        if file_path:
            return eval(f"pd.read_{file_path.split('.')[-1]}")(file_path)

    @classmethod
    def converted(cls, target_type: str) -> pd.DataFrame:
        '''
        Convert a file to a different file format

        args:
        - target_type: "excel" | "json" | "csv" 
        '''
        data = cls.read_data()
        if data is not None:
            try:
                data = eval(f"data.to_{target_type}")()
                save_file_path = _save_file(
                    placeholder=f"untitled.{target_type}")
                if save_file_path:
                    with open(save_file_path, 'w') as f:
                        f.write(data)
            except Exception:
                print(traceback.format_exc())
                raise Exception(
                    "Invalid target file type. Should be among 'excel', 'json', or 'csv'")
            return data
