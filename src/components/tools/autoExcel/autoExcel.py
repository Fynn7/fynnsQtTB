from PySide6 import QtWidgets, QtCore, QtGui
from baseWindow import BaseWindow
import json

from .excelHandler import *

class AutoExcel(BaseWindow):
    '''
    Excel Handling Tool
    '''
    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "Auto Excel"
        super().__init__()
        self.setupUi()
        self.setupMenubar()

    def setupUi(self):
        self.addWidgetToLayout("QLabel", text="Auto Excel Label")

    def setupMenubar(self):
        self.addBasicMenus(withConfig=False)

        menubar = self.getCurrentMenubar()

    def browseFile(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Excel Files (*.xlsx *.xls)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                # Do something with the selected file path
                print("Selected file:", file_path)