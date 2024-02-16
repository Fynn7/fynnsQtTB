import numpy as np
import pandas as pd
from googletrans import Translator
from PySide6.QtCore import QThread, Signal

class TranslationThread(QThread):
    progress_updated = Signal(int)
    current_translate_text=Signal(str)

    def __init__(self, df:pd.DataFrame, chosen_columns:list, dest_lang:str='zh-cn',src_lang:str='de'):
        super().__init__()
        self.df = df
        self.chosen_columns = chosen_columns
        self.dest_lang = dest_lang
        self.src_lang = src_lang

    def translate_df(self, df, chosen_columns, dest_lang,src_lang):
        total_elements = sum(df[col].count() for col in chosen_columns if df[col].dtype == 'O')
        translated_elements = 0
        def translate(x):
            nonlocal translated_elements
            try:
                print("translating element: ", x)
                self.current_translate_text.emit(f"Translating {x}")
                translated_text = translator.translate(x, dest=dest_lang,src=src_lang).text
                translated_elements += 1
                self.progress_updated.emit(translated_elements * 100 / total_elements)  # Emit signal for each translated element
                return translated_text
            except Exception as e:
                print("An error occurred:", e)
                return np.nan

        for col in chosen_columns:
            translator = Translator()
            if df[col].dtype == 'O':
                df[col] = df[col].apply(translate)
        return df

    def run(self):
        self.df = self.translate_df(self.df, self.chosen_columns, self.dest_lang,self.src_lang)
