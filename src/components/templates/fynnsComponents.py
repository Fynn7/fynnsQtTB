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
        
def _select_dir()->str|None:
    '''
    How to use:
    
    ```
    path=_select_dir()
    if path:
        # do something with the path
        ...
    ```
    '''
    return _select_file(file_mode=QFileDialog.Directory)