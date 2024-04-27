# from typing import type_check_only
# from abc import ABC, abstractmethod
import sys
import ctypes
import traceback
import json
import pkg_resources

try:
    from PySide6.QtCore import (
        Qt,
        Slot,
        Signal
    )
    from PySide6.QtWidgets import (
        QWidget,
        QMenuBar,
        QMainWindow,
        QLayoutItem,
        QVBoxLayout,
        QWidget,
        QCheckBox,
        QMessageBox,
        QMenu,
        QWidgetAction,
        QInputDialog,
    )
    from PySide6 import QtWidgets  # for "addWidgetToLayout" method
    from PySide6.QtGui import (
        QFont,
        QAction,
    )
except ImportError as ie:
    ctypes.windll.user32.MessageBoxW(
        0, str(ie)+"\n\nActivate venv and try again!", "Import Error", 0x10)
    print(traceback.format_exc())
    sys.exit()

except Exception as e:
    ctypes.windll.user32.MessageBoxW(0, str(e), "Unknown Error", 0x10)
    print(traceback.format_exc())
    sys.exit()


ORIG_SETTINGS: dict = {
    "language": "en_US",
    "font": {
        "family": "Consolas",
        "size": 12,
        "italic": False
    },
    "enable_closeEvent": False
}
ORIG_DATA: dict = {
    "balance": 0,
    "login_data": {
        "username": "",
        "password": ""
    },
    "custom_dicts": {},
    "emoji":{
        "emoji":"\ud83d\ude0a",
        "status":{
            "hunger":10,
            "cleanliness":10,
            "health":10,
        }
    }
}
_ENCODING: str = "utf-8"

_SETTINGS_PATH: str = pkg_resources.resource_filename(
    __name__, 'resources/settings.json')
_DATA_PATH: str = pkg_resources.resource_filename(
    __name__, 'resources/data.json')

# @type_check_only


class LayoutObject:
    '''Unused class just for layout type hinting'''

    def count(self):
        '''
        Return the number of items in the layout.
        NOTE: this is only a hint for type checking
        '''
        pass

    def takeAt(self, index: int) -> QLayoutItem:
        '''
        Return the item at position index from the layout.
        NOTE: this is only a hint for type checking
        '''
        pass

# @type_check_only


class function:
    '''Unused class just for function type hinting'''

    def __call__(self):
        '''
        Return the result of calling this function.
        NOTE: this is only a hint for type checking
        '''
        pass


class BaseWindow(QMainWindow):
    '''
    NOTE: This class is not meant to be used directly. It's a base class for other windows. Even though it is not defined as an abstract class

    Steps:
    (* means optional step)
    1. Create a new class that inherits from BaseWindow
    2. Overwrite the WINDOW_TITLE attribute
    3. Call the parent class __init__ method
    4. Setup the UI in the setup_ui method
    5. Add the basic menus in the setup_ui method
    6. Add widgets to the layout in the setup_ui method
    7. * Resize the window in the setup_ui method
    8. * Add other methods and attributes as needed
    9. Run the program

    Example:

    ```
class Dice(BaseWindow):
    def __init__(self):
        self.WINDOW_TITLE = "Dice Game" # overwriting the parent class attribute before parent calling its __init__
        # self.enable_closeEvent = False # overwriting the parent class attribute before parent calling its __init__
        super(Dice, self).__init__()
        self.setup_ui()


    def setup_ui(self):
        self.addBasicMenus() # optional if you want to add menu bar to this window
        self.addWidgetToLayout("QLabel", text="Dice Game") # optional
        self.addWidgetToLayout("QPushButton", text="Roll Dice", clickedConn=self.roll_dice) # optional
        self.resize(300, 200) # optional

    def roll_dice(self):
        import random
        dice = random.randint(1, 6)
        self.addWidgetToLayout("QLabel", text=f"You rolled a {dice}")
    ```
    '''
    WINDOW_TITLE: str = 'Base Window'
    isClosed: Signal = Signal(bool)
    changed_balance: Signal = Signal(float)

    def __init__(self):
        print("BaseWindow initializing...")
        super().__init__()
        # Read settings
        self.WINDOW_SIZE: tuple[int, int] = 800, 600

        self.__layout: LayoutObject = None
        self.__setupBaseUI()
        self.setFont(QFont(
            self.load_settings()["font"]["family"], pointSize=self.load_settings()["font"]["size"], italic=self.load_settings()["font"]["italic"]))
        print("BaseWindow initialized.")

    @staticmethod
    def load_settings() -> dict | None:
        try:
            with open(_SETTINGS_PATH, 'r') as file:
                settings_data = json.load(file)
        except Exception as e:
            print(traceback.format_exc())
            sys.exit(1)
        return settings_data
    
    def load_settings(self) -> dict | None:
        try:
            with open(_SETTINGS_PATH, 'r') as file:
                settings_data = json.load(file)
        except Exception as e:
            print(traceback.format_exc())
            QMessageBox.critical(
                self, "Fatal Error", "Failed to load settings: "+str(e))
            sys.exit(1)
        return settings_data

    @staticmethod
    def update_settings_file(new_settings: dict) -> int | None:
        '''
        write new settings to settings file
        and update GUI
        '''
        try:
            current_settings = BaseWindow.load_settings()
            current_settings.update(new_settings)
            # write to file

            with open(_SETTINGS_PATH, 'w') as file:
                json.dump(current_settings, file, indent=4)

            # update GUI
            BaseWindow.update_settings_to_gui(current_settings)
            return 0
        except Exception:
            print(traceback.format_exc())
            sys.exit(1)

    def update_settings_file(self, new_settings: dict) -> int | None:
        '''
        write new settings to settings file
        and update GUI
        '''
        try:
            current_settings = self.load_settings()
            current_settings.update(new_settings)
            # write to file

            with open(_SETTINGS_PATH, 'w') as file:
                json.dump(current_settings, file, indent=4)

            # update GUI
            self.update_settings_to_gui(current_settings)
            return 0
        except Exception:
            print(traceback.format_exc())
            QMessageBox.critical(
                self, "Fatal Error", "Failed to update settings file.")
            sys.exit(1)

    def update_settings_to_gui(self, new_settings: dict) -> int | None:
        '''
        update GUI with new settings
        '''
        try:
            # update GUI
            self.setFont(QFont(
                new_settings["font"]["family"], pointSize=new_settings["font"]["size"], italic=new_settings["font"]["italic"]))
            self.enableCloseEventCheckBox.setChecked(
                new_settings["enable_closeEvent"])
            # update all text according to language settings
            ...
            # adapt the window size after font size changed
            self.resize(self.WINDOW_SIZE[0]*new_settings['font']['size'] //
                        12, self.WINDOW_SIZE[1]*new_settings['font']['size']//12)
            return 0

        except Exception:
            print(traceback.format_exc())
            QMessageBox.critical(
                self, "Fatal Error", "Failed to update settings file.")
            sys.exit(1)

    @staticmethod
    def load_data() -> dict | None:
        try:
            with open(_DATA_PATH, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(traceback.format_exc())
            sys.exit(1)
        return data
    
    def load_data(self) -> dict | None:
        try:
            with open(_DATA_PATH, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(traceback.format_exc())
            QMessageBox.critical(
                self, "Fatal Error", "Failed to load data: "+str(e))
            sys.exit(1)
        return data

    @staticmethod
    def update_data_file(new_data: dict) -> int | None:
        '''
        write new data to data file
        '''
        try:
            # write to file
            current_data = BaseWindow.load_data()
            current_data.update(new_data)
            with open(_DATA_PATH, 'w') as file:
                json.dump(current_data, file, indent=4)
            return 0
        except Exception:
            print(traceback.format_exc())
            sys.exit(1)

    def update_data_file(self, new_data: dict) -> int | None:
        '''
        write new data to data file
        '''
        try:
            # write to file
            current_data = self.load_data()
            current_data.update(new_data)
            with open(_DATA_PATH, 'w') as file:
                json.dump(current_data, file, indent=4)
            return 0
        except Exception:
            print(traceback.format_exc())
            QMessageBox.critical(
                self, "Fatal Error", "Failed to update data file.")
            sys.exit(1)

    # virtual method for update data to gui
    def update_data_to_gui(self, new_data: dict) -> int | None:
        '''
        developer should override this method to update GUI with new data
        '''
        raise NotImplementedError(
            "This method should be overridden by developers.")

    @staticmethod
    def reset_data() -> int | None:
        '''
        reset all data to None but leave the keys
        '''
        reply = QMessageBox.warning(
            None, "Warning", "This will reset all data to default. Are you sure to continue?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            print("Resetting data applied.")
            try:
                with open(_DATA_PATH, 'w') as file:
                    json.dump(ORIG_DATA, file, indent=4)
                return 0
            except Exception:
                print(traceback.format_exc())
                QMessageBox.critical(
                    None, "Fatal Error", "Failed to reset data file.")
                sys.exit(1)
        return -1
    
    def reset_data(self) -> int | None:
        '''
        reset all data to None but leave the keys

        original data structure:
            {
            "balance":0 ,
            "login_data": {
                "username": "",
                "password": ""
            },
            "custom_dicts":{

            }
        }
        '''
        reply = QMessageBox.warning(
            self, "Warning", "This will reset all data to default. Are you sure to continue?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            print("Resetting data applied.")
            try:
                with open(_DATA_PATH, 'w') as file:
                    json.dump(ORIG_DATA, file, indent=4)
                return 0
            except Exception:
                print(traceback.format_exc())
                QMessageBox.critical(
                    self, "Fatal Error", "Failed to reset data file.")
                sys.exit(1)
        return -1  # if user clicked "No"

    def closeEvent(self, event) -> None:
        '''Override closeEvent'''
        if self.load_settings()["enable_closeEvent"]:
            reply = QMessageBox.question(self, self.WINDOW_TITLE,
                                         "Are you sure to quit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.isClosed.emit(True)
                print(self.WINDOW_TITLE, "closed.")
                event.accept()
            else:
                event.ignore()
        else:  # without popup, but still emitting signal
            self.isClosed.emit(True)
            print(self.WINDOW_TITLE, "closed.")
            event.accept()

    def __setupBaseUI(self):
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)
        self.__setupBasicMenubar()
        self.__setupLayout()
        print("Basic UI set up.")

    def __setupBasicMenubar(self) -> None:
        print("Setting up basic menubar...")
        self.addBasicMenus(withFile=False, withConfig=False)
        print("Basic menubar set up.")
        pass

    def __setupLayout(self) -> None:
        '''
        Initialize basic layout: aka with no widgets.
        '''
        print("Setting up basic layout...")
        self.updateLayout(QVBoxLayout())
        print("Basic layout set up.")

    @staticmethod
    def getEncoding() -> str:
        return _ENCODING

    def resetSettings(self) -> int:
        '''
        rvalues:
        0: Success
        -1: User clicked "No"
        1: Failed
        '''
        reply = QMessageBox.warning(
            self, "Warning", "This will reset all settings to default. Are you sure to continue?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            print("Resetting settings applied.")
            self.enableCloseEventCheckBox.setChecked(False)
            return self.update_settings_file(ORIG_SETTINGS)
        return -1  # if user clicked "No"

    def getLayout(self) -> LayoutObject:
        '''
        Public method to get current layout.

        Use this to add widget:
        ```
        layout=self.getLayout()
        self.someButton=QPushButton("Some Button")
        self.someButton.clicked.connect(self.someButtonFunction)
        layout.addWidget(widget)
        self.updateLayout(layout)
        ``` 

        Or a quicker way using public methode: if you don't want to save widget as class attribute:
        ```
        self.addWidgetToLayout()
        ```
        '''
        return self.__layout

    def updateLayout(self, layout: LayoutObject) -> None:
        '''
        Public method to update and SET a new layout. 
        Layout could be other than QVBoxLayout.

        It should already been set with widgets inside the layout. aka: you should update a "finished" layout with this methode.

        NOTE: Automatically set central widget.
        '''
        # set central widget
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        # save layout object variable
        self.__layout = layout

    def addWidgetToLayout(self, widgetType: str, text: str | None = None, clickedConn: function | None = None) -> QWidget | int:
        '''
        Public methode

        For quick and easy adding widget to CURRENT layout.
        NOTE: DIRECTLY ADD WIDGET TO CURRENT LAYOUT

        Return:
        returns created widget object

        widgetType: 
        - "QPushButton"
        - "QLabel"
        - "QLineEdit"
        - "QTextEdit"
        - "QPlainTextEdit"
        - "QComboBox"
        - "QSpinBox"
        - "QDoubleSpinBox"
        - "QCheckBox"
        - "QRadioButton"
        - "QProgressBar"
        - "QSlider"
        - "QDial"
        - "QCommandLinkButton"
        - "QDateEdit"
        - "QTimeEdit"
        - "QDateTimeEdit"
        - "QKeySequenceEdit"
        - "QFontComboBox"
        - "QColorDialog"
        - "QFileDialog"
        - "QInputDialog"
        - "QErrorMessage"
        - "QWizard"
        - "QWizardPage"
        - "QSpacerItem"
        ...

        '''
        lo = self.getLayout()
        # create widget and add display text, if it could be added
        try:
            if text:
                # e.g. widget=QPushButton("someWidgetDisplayText")
                widget: QWidget = eval(
                    f"QtWidgets.{widgetType}(text)")
            else:
                # e.g. widget=QtWidgets.QTimer()
                widget: QWidget = eval(f"QtWidgets.{widgetType}()")
        except NameError:
            # if failed to add display text, just create widget
            widget = eval(f"QtWidgets.{widgetType}()")
        except Exception:
            print(traceback.format_exc())
            QMessageBox.critical(
                self, "Fatal Error", "Failed to create widget object.")
            return 1

        if clickedConn:  # if the widget needs connection function
            widget.clicked.connect(clickedConn)
        lo.addWidget(widget)
        self.updateLayout(lo)
        return widget

    def addBasicMenus(self, withFile: bool = True, withConfig: bool = True) -> int:
        '''
        public method to setup BASIC menu.
        NOTE: After use this method, use self.menuBar().addMenu() to add more sub-menus.

        Return:
        Code 0: Success
        Code 1: Failed
        '''
        try:
            # get current menubar
            baseMenuBar = self.menuBar()

            if withFile:
                # file menu
                fileMenu = baseMenuBar.addMenu("File")
                # add exit action
                exitAction = QAction("Exit", self)
                exitAction.triggered.connect(self.close)
                fileMenu.addAction(exitAction)

            if withConfig:
                # settings menu
                settingsMenu = baseMenuBar.addMenu("Settings")

                # add reset settings action to settings menu
                resetSettingsAction = QAction("Reset Settings", self)
                resetSettingsAction.triggered.connect(self.resetSettings)
                settingsMenu.addAction(resetSettingsAction)

                # add enable/disable closeEvent action to settings menu
                enableCloseEventCheckBox = QCheckBox("Enable closeEvent")
                enableCloseEventCheckBox.setChecked(
                    self.load_settings()["enable_closeEvent"])
                enableCloseEventWidgetAction = QWidgetAction(self)
                enableCloseEventWidgetAction.setDefaultWidget(
                    enableCloseEventCheckBox)
                enableCloseEventCheckBox.stateChanged.connect(
                    self.handleCloseEvent)
                settingsMenu.addAction(enableCloseEventWidgetAction)
                # save the checkbox as class attribute in order to get the value in handleCloseEvent
                self.enableCloseEventCheckBox = enableCloseEventCheckBox

                # add change language sub-menu
                languageMenu = QMenu("Language", self)
                # add change to chinese action
                toZhCNAction = QAction("简体中文", self)
                toZhCNAction.triggered.connect(
                    lambda: self.update_settings_file({"language": "zh_CN"}))
                languageMenu.addAction(toZhCNAction)
                # add change to english action
                toEnUSAction = QAction("English", self)
                toEnUSAction.triggered.connect(
                    lambda: self.update_settings_file({"language": "en_US"}))
                languageMenu.addAction(toEnUSAction)
                # add change to german action
                toDeDEAction = QAction("Deutsch", self)
                toDeDEAction.triggered.connect(
                    lambda: self.update_settings_file({"language": "de_DE"}))
                languageMenu.addAction(toDeDEAction)
                # add all language options to settings menu
                settingsMenu.addMenu(languageMenu)
                # add change font sub-menu
                fontMenu = QMenu("Font", self)
                # add change to font times new roman action
                toFontTimesNewRomanAction = QAction(
                    "Times New Roman", self)
                toFontTimesNewRomanAction.triggered.connect(
                    lambda: self.changeFont(family="Times New Roman"))
                fontMenu.addAction(toFontTimesNewRomanAction)
                # add change to font consolas action
                toFontConsolasAction = QAction("Consolas", self)
                toFontConsolasAction.triggered.connect(
                    lambda: self.changeFont(family="Consolas"))
                fontMenu.addAction(toFontConsolasAction)
                # add change to font courier new action
                toFontCourierNewAction = QAction("Courier New", self)
                toFontCourierNewAction.triggered.connect(
                    lambda: self.changeFont(family="Courier New"))
                fontMenu.addAction(toFontCourierNewAction)

                # add change font size action
                changeFontSizeAction = QAction("Font Size", self)
                changeFontSizeAction.triggered.connect(self.changeFontSize)
                fontMenu.addAction(changeFontSizeAction)

                # add all font options to settings menu
                settingsMenu.addMenu(fontMenu)

                # NOTE: HERE FOR DEBUG THE BUTTONS ARE DISABLED
                toZhCNAction.setEnabled(False)
                toEnUSAction.setEnabled(False)
                toDeDEAction.setEnabled(False)
            return 0

        except Exception:
            print(traceback.format_exc())
            QMessageBox.critical(
                self, "Fatal Error", "Failed to create basic menu.")
            return 1

    def getCurrentMenubar(self) -> QMenuBar | None:
        '''
        Built-in method from QMainwindow to get current menubar.
        '''
        return self.menuBar()

    @Slot()  # syntax sugar for signal-slot connection
    def changeFont(self, family: str | None = None, size: int | None = None, italic: bool | None = None) -> int:
        # should update the whole font settings
        font_settings: dict = self.load_settings()["font"]
        if family:
            font_settings["family"] = family
        if size:
            font_settings["size"] = size
        if italic != None:
            font_settings["italic"] = italic
        return self.update_settings_file({"font": font_settings})

    @Slot()  # syntax sugar for signal-slot connection
    def changeFontSize(self) -> int:
        font_settings: dict = self.load_settings()["font"]
        changed_size, save_setting = QInputDialog.getInt(
            self, "Change Font Size", "Enter font size:", value=font_settings["size"], minValue=7, maxValue=20)
        if save_setting:
            font_settings["size"] = changed_size
            return self.update_settings_file({"font": font_settings})

    def showMessageBox(self, msgType: str = "information", msg: str = "") -> QMessageBox.StandardButton | int:
        '''
        Public method to show a message box.

        msgType:
        - "information"
        - "warning"
        - "critical"
        - "question"
        - "about"

        Return:
        the button which is clicked. (Yes Button  or no button)
        '''
        if msgType == "question":
            return QMessageBox.question(self, "Question", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        else:
            try:
                # if msgType is not "question", then set 1 button and to "Ok"
                return eval(f"QtWidgets.QMessageBox.{msgType}(self,msgType.capitalize(),msg,QtWidgets.QMessageBox.StandardButton.Ok)")
            except Exception:
                print(traceback.format_exc())
                QMessageBox.critical(
                    self, "Fatal Error", "Failed to show message box.")
                return 1

    @Slot()  # syntax sugar for signal-slot connection
    def handleCloseEvent(self) -> int:
        self.update_settings_file(
            {"enable_closeEvent": self.enableCloseEventCheckBox.isChecked()})

    # override keyPressEvent by BaseWindow
    def keyPressEvent(self, event):
        '''override keyPressEvent by BaseWindow'''
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        else:
            super().keyPressEvent(event)  # inherit keyEvent from QMainWindow

    def clearLayout(self):
        '''Clearout all widgets in the layout'''
        layout = self.getLayout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv) # introduce command line arguments
#     base_window = BaseWindow()
#     base_window.addBasicMenus()
#     base_window.show()
#     sys.exit(app.exec())
