from PySide6.QtWidgets import (
    QFileDialog,
)
# import type hint "any"
from typing import Any

def _select_file(name_filter:str="All Files (*)",file_mode:Any=QFileDialog.ExistingFile)->str|None:
    file_dialog = QFileDialog()
    file_dialog.setFileMode(file_mode)
    file_dialog.setNameFilter(name_filter)
    if file_dialog.exec():
        selected_files = file_dialog.selectedFiles()
        if selected_files:
            return selected_files[0]