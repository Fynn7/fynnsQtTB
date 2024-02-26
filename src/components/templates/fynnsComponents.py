from PySide6.QtWidgets import (
    QFileDialog,
)
# import type hint "any"
from typing import Any

def _select_file(name_filter:str|None=None,file_mode:Any=QFileDialog.ExistingFile)->str|None:
    '''
    How to use:
    
    ```
    file_path=_select_file("CSV Files (*.csv)",QFileDialog.ExistingFile)
    if file_path:
        # do something with the file
        ...
    ```
    '''
    file_dialog = QFileDialog()
    file_dialog.setFileMode(file_mode)
    if name_filter:
        file_dialog.setNameFilter(name_filter)
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            return selected_files[0]
        

def _save_file(name_filter:str|None=None,placeholder:str="untitled") -> str | None:
    '''
    rvalues:
    
    - str: the selected file path'''
    file_dialog = QFileDialog()
    file_dialog.setAcceptMode(QFileDialog.AcceptSave)
    file_dialog.setOption(QFileDialog.ShowDirsOnly, True)
    if name_filter:
        file_dialog.setNameFilter(name_filter)
    file_dialog.selectFile(placeholder)
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            return selected_files[0]
        
def _simple_save_file()->str|None:
    return QFileDialog.getSaveFileName()[0]