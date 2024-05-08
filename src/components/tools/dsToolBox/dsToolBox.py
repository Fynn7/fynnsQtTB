from PySide6.QtWidgets import (
    QMessageBox,
    QScrollArea,
    QMenu,
    QLabel
)
from PySide6.QtCore import (
    Slot
)
from PySide6.QtGui import (
    QAction,
)


from baseWindow import BaseWindow
from .ds import DataHandler, FileConverter

class DSToolBox(BaseWindow):
    '''
    Excel Handling Tool
    '''

    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "Data Science Toolbox"
        super().__init__()
        self.setupUi()
        self.setupMenubar()
        self.credit_calculator_window=None

    def setupUi(self):
        self.scroll_area=QScrollArea()
        self.setCentralWidget(self.scroll_area)
        self.info_label=QLabel("Select a file to convert")
        self.scroll_area.setWidget(self.info_label)
        self.scroll_area.setWidgetResizable(True)

    def setupMenubar(self):
        self.addBasicMenus(False)
        menubar = self.getCurrentMenubar()
        
        # File Converter Menu
        file_converter_menu = QMenu("File Converter",self)

        toCSV_action = QAction("To CSV",self)
        toCSV_action.triggered.connect(lambda: self.handle_file_converter("csv"))

        toExcel_action = QAction("To Excel",self)
        toExcel_action.triggered.connect(lambda: self.handle_file_converter("excel"))
        toExcel_action.setEnabled(False)

        toJSON_action = QAction("To JSON",self)
        toJSON_action.triggered.connect(lambda: self.handle_file_converter("json"))

        file_converter_menu.addAction(toCSV_action)
        file_converter_menu.addAction(toExcel_action)
        file_converter_menu.addAction(toJSON_action)

        menubar.addMenu(file_converter_menu)


    @Slot()
    def handle_file_converter(self,target_type:str):
        try:
            self.info_label.setText(FileConverter.converted(target_type))
        except Exception as e:
            QMessageBox.critical(self,"Error",str(e))