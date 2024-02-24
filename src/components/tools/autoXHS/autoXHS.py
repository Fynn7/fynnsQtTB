from baseWindow import BaseWindow
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QDialog,
)

from ...templates.fynnsLoginDialog import FynnsLoginDialog
class AutoXHS(BaseWindow):
    def __init__(self):
        self.WINDOW_TITLE = "Auto XHS"
        super().__init__()
        self.setup_ui()
        self.setup_menubar()

    def setup_ui(self):
        self.setWindowTitle(self.WINDOW_TITLE)

    def setup_menubar(self):
        menubar=self.menuBar()
        login_action = QAction("Login", self)
        login_action.triggered.connect(self.open_login_dialog)
        menubar.addAction(login_action)

    def open_login_dialog(self):
        login_dialog = FynnsLoginDialog()
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            login_info = login_dialog.get_login_info()
            print("got login info:", login_info)
            ...