from PySide6.QtWidgets import (
    QInputDialog
)

def open_input_dialog(title:str,message:str)->str:
    '''
    Open a simple input dialog

    args:
    - title: str
    - message: str

    returns:
    - str
    '''
    return QInputDialog.getText(None,title,message)[0] if QInputDialog.getText(None,title,message)[1] else None