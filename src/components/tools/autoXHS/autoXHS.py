from baseWindow import BaseWindow

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QDialog,
)
from PySide6.QtCore import (
    Slot
)

from ...templates.fynnsLoginDialog import FynnsLoginDialog


class AutoXHS(BaseWindow):
    TARGET_URL: str = "https://www.xiaohongshu.com/"

    def __init__(self):
        self.WINDOW_TITLE = "Auto XHS"
        super().__init__()
        self.setup_ui()
        self.setup_menubar()

        # self.open_login_dialog()

    def setup_ui(self):
        self.setWindowTitle(self.WINDOW_TITLE)

    def setup_menubar(self):
        menubar = self.menuBar()
        self.login_action = QAction("Login", self)
        self.login_action.triggered.connect(self.open_login_dialog)
        menubar.addAction(self.login_action)

        # login should be manually done because of the complexity of the login process on xiaohongshu.com
        self.login_action.setDisabled(True)

    @Slot()
    def open_login_dialog(self):
        saved_login_data: dict = self.load_data()["login_data"]
        login_dialog = FynnsLoginDialog(saved_login_data)
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            login_data = login_dialog.get_login_data()
            print("got login info:", login_data)
            self.update_data_file({"login_data": login_data})

    def xhs_login(self):
        # username,password = self.load_data()["login_data"]['username'],self.load_data()["login_data"]['password']
        # driver = webdriver.Edge()

        # driver.get(self.TARGET_URL)

        # # TODO: NEXT STEP IS TO FIND THE LOGIN ELEMENT ON THE WEBPAGE
        # username_field = driver.find_element_by_name("username")  # replace with the actual name
        # password_field = driver.find_element_by_name("password")  # replace with the actual name

        # username_field.send_keys(username)
        # password_field.send_keys(password)

        # password_field.send_keys(Keys.RETURN)  # submit the form
        pass
