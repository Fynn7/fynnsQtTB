from PySide6.QtWidgets import (
    QFileDialog,
    QApplication,
    QDialog,
    QTableWidgetItem,
    QMessageBox,
    QScrollArea
)
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QAction,

)


from baseWindow import BaseWindow
import ds

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

    def setupUi(self):
        self.scroll_area=QScrollArea()
        self.setCentralWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)

    def setupMenubar(self):
        menubar = self.getCurrentMenubar()
