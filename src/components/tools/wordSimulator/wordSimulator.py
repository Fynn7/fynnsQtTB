from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox,QTextEdit
from PySide6.QtCore import Slot
import sys
from baseWindow import BaseWindow


class WordSimulator(BaseWindow):
    FILE_SUPPORTED = "Notebook(*.txt);;Word File(*.doc,*.docx,*.oct);;All Files (*)"
    def __init__(self):
        self.WINDOW_TITLE = "Word Simulator" # overwriting the parent class attribute before parent calling its __init__
        super().__init__()
        self.resize(*self.WINDOW_SIZE)
        self.addBasicMenus(withConfig=False)
        self.text_edit:QTextEdit=self.addWidgetToLayout("QTextEdit")
        self.addWidgetToLayout("QPushButton", text="Save",
                               clickedConn=self.save_document)


    @Slot()
    def save_document(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save", "", self.FILE_SUPPORTED)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())