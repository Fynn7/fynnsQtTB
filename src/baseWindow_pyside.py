from PySide6 import QtWidgets, QtGui,QtCore
import traceback
import json

_ENCODING: str = "utf-8"
_SETTINGS_FILE_PATH: str = "settings.json"
_settings: dict = json.load(open(_SETTINGS_FILE_PATH, "r", encoding=_ENCODING))


class LayoutObject:
    '''Unused class just for layout type hinting'''
    pass


class Function:
    '''Unused class just for callable type hinting'''
    pass


class BaseWindow(QtWidgets.QMainWindow):
    WINDOW_TITLE: str = 'Base Window'

    def __init__(self):
        super().__init__()
        self.WINDOW_SIZE: tuple[int, int] = (
            _settings["windowSize"]["width"], _settings["windowSize"]["height"])
        self.language: str = _settings["language"]
        self.__layout: LayoutObject = None
        self.__setupBaseUI()
        self.setFont(QtGui.QFont(
            _settings["font"]["family"], pointSize=_settings["font"]["size"], italic=_settings["font"]["italic"]))

    def __setupBaseUI(self):
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)
        self.__setupBasicMenubar()
        self.__setupLayout()

    def __setupBasicMenubar(self) -> None:
        pass

    def __setupLayout(self) -> None:
        '''
        Initialize basic layout: aka with no widgets.
        '''
        self.updateLayout(QtWidgets.QVBoxLayout())

    @staticmethod
    def getEncoding() -> str:
        return _ENCODING

    def getSettings(self) -> dict:
        return json.load(open("settings.json", "r", encoding=_ENCODING))

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
                fileMenu = baseMenuBar.addMenu("File (Alt+F)")
                # add exit action
                exitAction = QtGui.QAction("Exit (Alt+F4)", self)
                exitAction.triggered.connect(self.close)
                fileMenu.addAction(exitAction)

            if withConfig:
                # settings menu
                settingsMenu = baseMenuBar.addMenu("Settings (Alt+S)")
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
                # add all font options to settings menu
                settingsMenu.addMenu(fontMenu)
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

    def changeLanguage(self, lang: str):
        pass

    def changeFont(self, family: str | None = None, size: int | None = None, italic: bool | None = None) -> int:
        if family:
            _settings["font"]["family"] = family
        if size:
            _settings["font"]["size"] = size
        if italic != None:
            _settings["font"]["italic"] = italic
        try:
            json.dump(_settings, open("settings.json",
                      "w", encoding=_ENCODING), indent=4)
            QtWidgets.QMessageBox.information(
                self, "Success", "Please restart the program to apply changes.")
            return 0
        except Exception:
            QtWidgets.QMessageBox.critical(
                self, "Fatal Error", "Failed to change font.")
            print(traceback.format_exc())
            return 1

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

    # press ESC to close window
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        # press Alt+F to open file menu
        elif event.key() == QtCore.Qt.Key.Key_F and event.modifiers() == QtCore.Qt.KeyboardModifier.AltModifier:
            self.menuBar().actions()[0].menu().exec(QtGui.QCursor.pos())
        # press Alt+S to open settings menu
        elif event.key() == QtCore.Qt.Key.Key_S and event.modifiers() == QtCore.Qt.KeyboardModifier.AltModifier:
            self.menuBar().actions()[1].menu().exec(QtGui.QCursor.pos())
        else:
            super().keyPressEvent(event) # inherit keyEvent from parent class


# if __name__ == "__main__":
#     app = QtWidgets.QApplication([])
#     mainWindow = BaseWindow()
#     mainWindow.show()
#     app.exec()
