from PyQt6.QtWidgets import QMainWindow, QMenuBar, QVBoxLayout, QWidget, QApplication,QMessageBox,QMenu,QPushButton,QLabel
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal,QEvent
import traceback

class LayoutObject:
    '''Just for type hinting'''
    pass
class Function:
    '''Just for callable type hinting'''
    pass
_WINDOW_TITLE:str = 'Base Window'
_WINDOW_SIZE:tuple[int,int] = (800, 600)

# Later move to json file as settings.json
_LANGUAGE_SUPPORTED:str=["zh_CN","en_US","de_DE"]
_ENCODING:str="utf-8"

class BaseWindow(QMainWindow):
    language:str="en_US"
    hasCloseEvent:bool=True
    isClosed:pyqtSignal = pyqtSignal(bool)
    __layout:LayoutObject=None

    def __init__(self):
        super().__init__()
        self.__setupBaseUI()


    def __setupBaseUI(self):
        # Set window title 
        self.setWindowTitle(_WINDOW_TITLE)
        
        # Set window size
        self.resize(*_WINDOW_SIZE)

        # Setup Menubar
        self.__setupBasicMenubar()

        # Set layout (has already set central widget)
        self.__setupLayout()

    def __setupBasicMenubar(self)->None:
        returnCode=self.createBasicMenubar()
        print("setupMenu() returned code: ",returnCode) # DEBUGGER


    def __setupLayout(self)->None:
        '''
        Initialize basic layout: aka with no widgets.
        '''
        self.updateLayout(QVBoxLayout())

    def getLayout(self)->LayoutObject:
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
    
    def updateLayout(self,layout:LayoutObject)->None:
        '''
        Principle: According to `Information Hiding`

        Public method to update and SET a new layout. 
        Layout could be other than QVBoxLayout.

        It should already been set with widgets inside the layout. aka: you should update a "finished" layout with this methode.

        NOTE: Automatically set central widget.
        '''
        # set central widget
        centralWidget=QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        # save layout object variable
        self.__layout=layout

    def addWidgetToLayout(self,widgetType:str,widgetDisplayText:str="someWidgetDisplayText",conn:Function|None=None)->QWidget:
        '''
        Public methode

        For quick and easy adding widget to layout.

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
        lo=self.getLayout()
        # create widget and add display text, if it could be added
        try:
            widget:QWidget=eval(f"{widgetType}(widgetDisplayText)") # e.g. widget=QPushButton("someWidgetDisplayText")
        except NameError:
            # if failed to add display text, just create widget
            widget=eval(f"{widgetType}(widgetDisplayText)")
        except Exception:
            QMessageBox.critical(self,"Fatal Error","Failed to create widget object.")
            print(traceback.format_exc())
            return
        
        if conn: # if the widget needs connection function
            widget.clicked.connect(conn)
        lo.addWidget(widget)
        self.updateLayout(lo)

    def createBasicMenubar(self)->int:
        '''
        public method to setup BASIC menu.
        NOTE: After use this method, use self.menuBar().addMenu() to add more sub-menus.

        Return:
        Code 0: Success
        Code 1: Failed
        '''
        # menubar. inherited from QMainWindow
        try:
            # get current menubar
            baseMenuBar=self.menuBar() 

            # file menu
            fileMenu=baseMenuBar.addMenu("File (Alt+F)")
            # add exit action
            exitAction=QAction("Exit (Alt+F4)",self)
            exitAction.triggered.connect(self.close)
            fileMenu.addAction(exitAction)

            # settings menu
            settingsMenu=baseMenuBar.addMenu("Settings (Alt+S)")
            # add change language sub-menu
            languageMenu=QMenu("Language",self)
            # add change to chinese action
            toZhCNAction=QAction("简体中文",self)
            toZhCNAction.triggered.connect(lambda:self.changeLanguage(lang="zh_CN"))
            languageMenu.addAction(toZhCNAction)
            # add change to english action
            toEnUSAction=QAction("English",self)
            toEnUSAction.triggered.connect(lambda:self.changeLanguage(lang="en_US"))
            languageMenu.addAction(toEnUSAction)
            # add change to german action
            toDeDEAction=QAction("Deutsch",self)
            toDeDEAction.triggered.connect(lambda:self.changeLanguage(lang="de_DE"))
            languageMenu.addAction(toDeDEAction)
            # add all language options to settings menu
            settingsMenu.addMenu(languageMenu)
            # add change font sub-menu
            fontMenu=QMenu("Font",self)
            # add change to font times new roman action
            toFontTimesNewRomanAction=QAction("Times New Roman",self)
            toFontTimesNewRomanAction.triggered.connect(lambda:self.changeFont(font="Times New Roman"))
            fontMenu.addAction(toFontTimesNewRomanAction)
            # add change to font consolas action
            toFontConsolasAction=QAction("Consolas",self)
            toFontConsolasAction.triggered.connect(lambda:self.changeFont(font="Consolas"))
            fontMenu.addAction(toFontConsolasAction)
            # add change to font courier new action
            toFontCourierNewAction=QAction("Courier New",self)
            toFontCourierNewAction.triggered.connect(lambda:self.changeFont(font="Courier New"))
            fontMenu.addAction(toFontCourierNewAction)
            # add all font options to settings menu
            settingsMenu.addMenu(fontMenu)
            return 0
        
        except Exception:
            QMessageBox.critical(self,"Fatal Error","Failed to create basic menu.")
            print(traceback.format_exc())
            return 1
        
    def getCurrentMenubar(self)->QMenuBar|None:
        '''
        Built-in method from QMainwindow to get current menubar.
        '''
        return self.menuBar()

    def changeLanguage(self,lang:str):
        pass
    
    def changeFont(self,font:str):
        pass

    if hasCloseEvent:
        def closeEvent(self, event:QEvent)->None:
            '''Override the close event to perform custom actions'''
            reply = QMessageBox.question(self, "BaseWindow",
                                        "Are you sure to quit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.isClosed.emit(True)
                print(_WINDOW_TITLE,"closed.") # DEBUGGER
                event.accept()
            else:
                event.ignore()
            event.accept()

    def customCloseEvent(self):
        # Implement this method in your derived classes to perform custom actions on close
        pass

if __name__ == '__main__':
    app = QApplication([])
    mainWindow = BaseWindow()
    mainWindow.show()
    app.exec()
