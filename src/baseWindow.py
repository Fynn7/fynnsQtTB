# from abc import ABC, abstractmethod
import sys
import ctypes
import traceback
import json

try:
    from PySide6 import QtWidgets, QtGui,QtCore

except ImportError as ie:
    ctypes.windll.user32.MessageBoxW(0, str(ie), "Import Error",0x10)
    print(traceback.format_exc())
    sys.exit()

except Exception as e:
    ctypes.windll.user32.MessageBoxW(0, str(e), "Unknown Error", 0x10)
    print(traceback.format_exc())
    sys.exit()


ORIG_SETTINGS:dict={
    "language": "en_US",
    "windowSize": {
        "width": 800,
        "height": 600
    },
    "font": {
        "family": "Consolas",
        "size": 12,
        "italic": False
    },
    "enable_closeEvent": True
}
_ENCODING: str = "utf-8"
_SETTINGS_FILE_PATH: str = "fynnsQtTB/src/settings.json"
_settings: dict = json.load(open(_SETTINGS_FILE_PATH, "r", encoding=_ENCODING))


class LayoutObject:
    '''Unused class just for layout type hinting'''
    pass


class Function:
    '''Unused class just for callable type hinting'''
    pass


class BaseWindow(QtWidgets.QMainWindow):
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
    isClosed = QtCore.Signal(bool)

    def __init__(self):
        print("BaseWindow initializing...")
        super().__init__()
        # Read settings
        self.WINDOW_SIZE: tuple[int, int] = (
            _settings["windowSize"]["width"], _settings["windowSize"]["height"])
        self.language: str = _settings["language"]
        self.enable_closeEvent: bool = _settings["enable_closeEvent"]

        self.__layout: LayoutObject = None
        self.__setupBaseUI()
        self.setFont(QtGui.QFont(
            _settings["font"]["family"], pointSize=_settings["font"]["size"], italic=_settings["font"]["italic"]))
        print("BaseWindow initialized.")
    
    if _settings["enable_closeEvent"]:
        def closeEvent(self, event) -> None:
            '''Override closeEvent'''
            reply = QtWidgets.QMessageBox.question(self, self.WINDOW_TITLE,
                                                "Are you sure to quit?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,  QtWidgets.QMessageBox.StandardButton.No)

            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.isClosed.emit(True)
                print(self.WINDOW_TITLE, "closed.")
                event.accept()
            else:
                event.ignore()
    else: # without popup, but still emitting signal
        def closeEvent(self, event) -> None:
            '''Override closeEvent'''
            self.isClosed.emit(True)
            print(self.WINDOW_TITLE, "closed.")
            event.accept()

    def __setupBaseUI(self):
        print("Setting up basic UI...")
        # check language
        if self.language == "en_US":
            print("Language detected: English.")
            # TODO: use QTranslator , build qm file, add to resource file
            # self.translator = QtCore.QTranslator(self)
            # self.translator.load("en_US.qm")
            # QtWidgets.QApplication.installTranslator(self.translator)
            ... 
        elif self.language == "zh_CN":
            print("Language detected: Simplified Chinese.")
            ...
        elif self.language == "de_DE":
            print("Language detected: German.")
            ...
        else:
            print("Language not supported. Using default language: English.")
            ...

        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)
        self.__setupBasicMenubar()
        self.__setupLayout()
        print("Basic UI set up.")

    def __setupBasicMenubar(self) -> None:
        print("Setting up basic menubar...")
        self.addBasicMenus(withFile=False,withConfig=False)
        print("Basic menubar set up.")
        pass

    def __setupLayout(self) -> None:
        '''
        Initialize basic layout: aka with no widgets.
        '''
        print("Setting up basic layout...")
        self.updateLayout(QtWidgets.QVBoxLayout())
        print("Basic layout set up.")

    @staticmethod
    def getEncoding() -> str:
        return _ENCODING

    def resetSettings(self) -> int:
        print("Resetting settings applied.")
        reply=QtWidgets.QMessageBox.warning(
            self, "Warning", "This will reset all settings to default. Are you sure to continue?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
        if reply==QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                json.dump(ORIG_SETTINGS, open(_SETTINGS_FILE_PATH,
                        "w", encoding=_ENCODING), indent=4)
                QtWidgets.QMessageBox.information(
                    self, "Success", "Please restart the program to apply changes.")
                return 0
            except Exception:
                QtWidgets.QMessageBox.critical(
                    self, "Fatal Error", "Failed to reset settings.")
                print(traceback.format_exc())
                return 1
        else:
            return 0
        

    def getSettings(self) -> dict:
        return json.load(open(_SETTINGS_FILE_PATH, "r", encoding=_ENCODING))

    def getLayout(self) -> LayoutObject:
        '''
        Principle: According to `Information Hiding`

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
        Principle: According to `Information Hiding`

        Public method to update and SET a new layout. 
        Layout could be other than QVBoxLayout.

        It should already been set with widgets inside the layout. aka: you should update a "finished" layout with this methode.

        NOTE: Automatically set central widget.
        '''
        # set central widget
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        # save layout object variable
        self.__layout = layout

    def addWidgetToLayout(self, widgetType: str, text: str | None = None, clickedConn: Function | None = None) -> QtWidgets.QWidget | int:
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
                widget: QtWidgets.QWidget = eval(
                    f"QtWidgets.{widgetType}(text)")
            else:
                # e.g. widget=QtWidgets.QTimer()
                widget: QtWidgets.QWidget = eval(f"QtWidgets.{widgetType}()")
        except NameError:
            # if failed to add display text, just create widget
            widget = eval(f"QtWidgets.{widgetType}()")
        except Exception:
            QtWidgets.QMessageBox.critical(
                self, "Fatal Error", "Failed to create widget object.")
            print(traceback.format_exc())
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
                exitAction = QtGui.QAction("Exit", self)
                exitAction.triggered.connect(self.close)
                fileMenu.addAction(exitAction)

            if withConfig:
                # settings menu
                settingsMenu = baseMenuBar.addMenu("Settings")

                # add reset settings action to settings menu
                resetSettingsAction = QtGui.QAction("Reset Settings", self)
                resetSettingsAction.triggered.connect(self.resetSettings)
                settingsMenu.addAction(resetSettingsAction)

                # add enable/disable closeEvent action to settings menu
                enableCloseEventCheckBox = QtWidgets.QCheckBox("Enable closeEvent")
                enableCloseEventCheckBox.setChecked(_settings["enable_closeEvent"])
                enableCloseEventWidgetAction = QtWidgets.QWidgetAction(self)
                enableCloseEventWidgetAction.setDefaultWidget(enableCloseEventCheckBox)
                enableCloseEventCheckBox.stateChanged.connect(self.handleCloseEvent)
                settingsMenu.addAction(enableCloseEventWidgetAction)
                # save the checkbox as class attribute in order to get the value in handleCloseEvent
                self.enableCloseEventCheckBox=enableCloseEventCheckBox

                # add change language sub-menu
                languageMenu = QtWidgets.QMenu("Language", self)
                # add change to chinese action
                toZhCNAction = QtGui.QAction("简体中文", self)
                toZhCNAction.triggered.connect(
                    lambda: self.changeLanguage(lang="zh_CN"))
                languageMenu.addAction(toZhCNAction)
                # add change to english action
                toEnUSAction = QtGui.QAction("English", self)
                toEnUSAction.triggered.connect(
                    lambda: self.changeLanguage(lang="en_US"))
                languageMenu.addAction(toEnUSAction)
                # add change to german action
                toDeDEAction = QtGui.QAction("Deutsch", self)
                toDeDEAction.triggered.connect(
                    lambda: self.changeLanguage(lang="de_DE"))
                languageMenu.addAction(toDeDEAction)
                # add all language options to settings menu
                settingsMenu.addMenu(languageMenu)
                # add change font sub-menu
                fontMenu = QtWidgets.QMenu("Font", self)
                # add change to font times new roman action
                toFontTimesNewRomanAction = QtGui.QAction(
                    "Times New Roman", self)
                toFontTimesNewRomanAction.triggered.connect(
                    lambda: self.changeFont(family="Times New Roman"))
                fontMenu.addAction(toFontTimesNewRomanAction)
                # add change to font consolas action
                toFontConsolasAction = QtGui.QAction("Consolas", self)
                toFontConsolasAction.triggered.connect(
                    lambda: self.changeFont(family="Consolas"))
                fontMenu.addAction(toFontConsolasAction)
                # add change to font courier new action
                toFontCourierNewAction = QtGui.QAction("Courier New", self)
                toFontCourierNewAction.triggered.connect(
                    lambda: self.changeFont(family="Courier New"))
                fontMenu.addAction(toFontCourierNewAction)
                
                # add change font size action
                changeFontSizeAction = QtGui.QAction("Font Size", self)
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
            QtWidgets.QMessageBox.critical(
                self, "Fatal Error", "Failed to create basic menu.")
            print(traceback.format_exc())
            return 1

    def getCurrentMenubar(self) -> QtWidgets.QMenuBar | None:
        '''
        Built-in method from QMainwindow to get current menubar.
        '''
        return self.menuBar()

    def changeLanguage(self, lang: str)->int:
        try:
            _settings["language"] = lang
            QtWidgets.QMessageBox.information(
                    self, "Success", "Please restart the program to apply changes.")
            json.dump(_settings, open(_SETTINGS_FILE_PATH,
                      "w", encoding=_ENCODING), indent=4)
            return 0
        except Exception:
            QtWidgets.QMessageBox.critical(
                self, "Fatal Error", "Failed to change language.")
            print(traceback.format_exc())
            return 1
        
    def changeFont(self, family: str | None = None, size: int | None = None, italic: bool | None = None) -> int:
        if family:
            _settings["font"]["family"] = family
        if size:
            _settings["font"]["size"] = size
        if italic != None:
            _settings["font"]["italic"] = italic
        try:
            json.dump(_settings, open(_SETTINGS_FILE_PATH,
                      "w", encoding=_ENCODING), indent=4)
            QtWidgets.QMessageBox.information(
                self, "Success", "Please restart the program to apply changes.")
            return 0
        except Exception:
            QtWidgets.QMessageBox.critical(
                self, "Fatal Error", "Failed to change font.")
            print(traceback.format_exc())
            return 1

    def changeFontSize(self)->int:
        try:
            changed_size,save_setting=QtWidgets.QInputDialog.getInt(self, "Change Font Size", "Enter font size:",value=_settings["font"]["size"],minValue=7,maxValue=20)
        except Exception:
            QtWidgets.QMessageBox.critical(
                self, "Fatal Error", "Failed to change font size.")
            print(traceback.format_exc())
            return 1
        if save_setting:
            self.changeFont(size=changed_size)
            print("Font size changed to",changed_size)
        return 0
    def showMessageBox(self, msgType: str = "information", msg: str = "") -> QtWidgets.QMessageBox.StandardButton | int:
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
            return QtWidgets.QMessageBox.question(self, "Question", msg, QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        else:
            try:
                # if msgType is not "question", then set 1 button and to "Ok"
                return eval(f"QtWidgets.QMessageBox.{msgType}(self,msgType.capitalize(),msg,QtWidgets.QMessageBox.StandardButton.Ok)")
            except Exception:
                QtWidgets.QMessageBox.critical(
                    self, "Fatal Error", "Failed to show message box.")
                print(traceback.format_exc())
                return 1
            
    def handleCloseEvent(self) -> int:
        _settings["enable_closeEvent"]=self.enableCloseEventCheckBox.isChecked()
        try:
            json.dump(_settings, open(_SETTINGS_FILE_PATH,
                      "w", encoding=_ENCODING), indent=4)
            QtWidgets.QMessageBox.information(
                self, "Success", "Please restart the program to apply changes.")
            return 0
        except Exception:
            QtWidgets.QMessageBox.critical(
                self, "Fatal Error", "Failed to change closeEvent settings.")
            print(traceback.format_exc())
            return 1

    # press ESC to close window
    def keyPressEvent(self, event):
        '''override keyPressEvent by BaseWindow'''
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        else:
            super().keyPressEvent(event) # inherit keyEvent from QMainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    base_window = BaseWindow()
    base_window.addBasicMenus()
    base_window.show()
    sys.exit(app.exec())