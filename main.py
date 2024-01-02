from PyQt6 import QtCore, QtGui, QtWidgets

from Components.Tools.pomodoroTimer.pomodoroTimer import PomodoroTimer
from Components.Tools.wordSimulator.wordSimulator import WordSimulator
from Components.Tools.mlToolBox.mlToolBox import MlToolBox
from Components.Games.Dice.dice import Dice
from baseWindow import BaseWindow

class ToolBoxUI(BaseWindow):
    WINDOW_TITLE = "万能工具盒"
    WINDOW_SIZE = (800, 600)
    LANGUAGE="中文"
    components = {
        "Tools": {
            "WordSimulator": None,
            "PomodoroTimer": None,
            "MlToolBox": None, },
        "Games": {
            "Dice": None,
        }
    }

    def setupUi(self, mainWindow: QtWidgets.QMainWindow) -> None:
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(*self.WINDOW_SIZE)
        self.centralwidget = QtWidgets.QWidget(parent=mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget_lastUsedTools = QtWidgets.QListWidget(
            parent=self.centralwidget)
        self.listWidget_lastUsedTools.setObjectName("listWidget_lastUsedTools")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_lastUsedTools.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_lastUsedTools.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_lastUsedTools.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_lastUsedTools.addItem(item)
        self.gridLayout.addWidget(self.listWidget_lastUsedTools, 0, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)

    def setupMenubar(self, mainWindow: QtWidgets.QMainWindow) -> None:
        self.menubar = QtWidgets.QMenuBar(parent=mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu_files = QtWidgets.QMenu(parent=self.menubar)
        self.menu_files.setObjectName("menu_files")
        self.menu_edit = QtWidgets.QMenu(parent=self.menubar)
        self.menu_edit.setObjectName("menu_edit")
        self.menu_Alt_S = QtWidgets.QMenu(parent=self.menubar)
        self.menu_Alt_S.setObjectName("menu_Alt_S")
        self.menu_Alt_H = QtWidgets.QMenu(parent=self.menubar)
        self.menu_Alt_H.setObjectName("menu_Alt_H")
        self.menu_toolMenus = QtWidgets.QMenu(parent=self.menubar)
        self.menu_toolMenus.setObjectName("menu_toolMenus")
        self.menu_games = QtWidgets.QMenu(parent=self.menubar)
        self.menu_games.setObjectName("menu_games")
        mainWindow.setMenuBar(self.menubar)
        


    def setupStatusbar(self, mainWindow: QtWidgets.QMainWindow) -> None:
        self.statusbar = QtWidgets.QStatusBar(parent=mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

    def setupActions(self, mainWindow: QtWidgets.QMainWindow) -> None:
        self.action_language = QtGui.QAction(parent=mainWindow)
        self.action_language.setObjectName("action_language")
        self.action_pomodoroTimer = QtGui.QAction(parent=mainWindow)
        self.action_pomodoroTimer.setObjectName("action_pomodoroTimer")
        self.action_wordSimulator = QtGui.QAction(parent=mainWindow)
        self.action_wordSimulator.setObjectName("action_wordSimulator")
        self.action_mlToolBox = QtGui.QAction(parent=mainWindow)
        self.action_mlToolBox.setObjectName("action_mlToolBox")
        self.action_font = QtGui.QAction(parent=mainWindow)
        self.action_font.setObjectName("action_font")
        self.action_diceGame=QtGui.QAction(parent=mainWindow)
        self.action_diceGame.setObjectName("action_diceGame")


        self.menu_Alt_S.addAction(self.action_language)
        self.menu_Alt_S.addAction(self.action_font)
        self.menu_toolMenus.addAction(self.action_pomodoroTimer)
        self.menu_toolMenus.addAction(self.action_wordSimulator)
        self.menu_toolMenus.addAction(self.action_mlToolBox)
        self.menubar.addAction(self.menu_files.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_toolMenus.menuAction())
        self.menubar.addAction(self.menu_Alt_S.menuAction())
        self.menubar.addAction(self.menu_games.menuAction())
        self.menubar.addAction(self.menu_Alt_H.menuAction())
        self.menu_games.addAction(self.action_diceGame)

    def setupConnections(self, mainWindow: QtWidgets.QMainWindow) -> None:
        # 连接番茄时钟的信号与槽
        self.action_pomodoroTimer.triggered.connect(
            lambda: self.open_component_window("Tools","PomodoroTimer"))

        self.action_wordSimulator.triggered.connect(
            lambda: self.open_component_window("Tools","WordSimulator"))
        # 连接机器学习工具集的信号与槽
        self.action_mlToolBox.triggered.connect(
            lambda: self.open_component_window("Tools","MlToolBox"))

        self.action_diceGame.triggered.connect(
            lambda: self.open_component_window("Games","Dice"))

    def setupFinal(self, mainWindow: QtWidgets.QMainWindow) -> None:
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def warn(self, msg: str) -> None:
        '''
        Directly call a default standard warning message box.
        '''
        QtWidgets.QMessageBox.warning(
            self.centralwidget,
            "警告",
            msg,
            QtWidgets.QMessageBox.StandardButton.Ok
        )

    def retranslateUi(self, mainWindow: QtWidgets.QMainWindow) -> None:
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", self.WINDOW_TITLE))
        __sortingEnabled = self.listWidget_lastUsedTools.isSortingEnabled()
        self.listWidget_lastUsedTools.setSortingEnabled(False)
        item = self.listWidget_lastUsedTools.item(0)
        item.setText(_translate("mainWindow", "历史使用工具："))
        item = self.listWidget_lastUsedTools.item(1)
        item.setText(_translate("mainWindow", "tool1"))
        item = self.listWidget_lastUsedTools.item(2)
        item.setText(_translate("mainWindow", "tool2"))
        item = self.listWidget_lastUsedTools.item(3)
        item.setText(_translate("mainWindow", "tool3"))
        self.listWidget_lastUsedTools.setSortingEnabled(__sortingEnabled)
        self.menu_files.setTitle(_translate("mainWindow", "文件(Alt+F)"))
        self.menu_edit.setTitle(_translate("mainWindow", "编辑(Alt+E)"))
        self.menu_Alt_S.setTitle(_translate("mainWindow", "设置(Alt+S)"))
        self.menu_Alt_H.setTitle(_translate("mainWindow", "帮助(Alt+H)"))
        self.menu_toolMenus.setTitle(_translate("mainWindow", "菜单(Alt+M)"))
        self.menu_games.setTitle(_translate("mainWindow", "游戏(Alt+G)"))
        self.action_pomodoroTimer.setText(_translate("mainWindow", "番茄时间"))
        self.action_wordSimulator.setText(_translate("mainWindow", "Word模拟器"))
        self.action_mlToolBox.setText(_translate("mainWindow", "机器学习工具集"))
        self.action_language.setText(_translate("mainWindow", "语言"))
        self.action_font.setText(_translate("mainWindow", "字体"))
        self.action_diceGame.setText(_translate("mainWindow","骰子游戏"))

    def create_and_save_component(self, class_name:str,component_name: str) -> QtWidgets.QMainWindow:
        try:
            component: QtWidgets.QMainWindow = eval(f"{component_name}()")
            # save component object, otherwise it will be deleted directly after opening this component window
            self.components[class_name][component_name] = component
            return component
        except NameError as e:
            self.warn(
                msg=f"Component {component_name} under class {class_name} not found.\nOriginal error message:\n{e}")
            raise NameError(e)
        except Exception as e:
            self.warn(
                msg=f"Unknown error when creating component {component_name} under class {class_name}.\nOriginal error message:\n{e}")
            raise Exception(e)

    def reset_component(self, class_name:str,component_name: str) -> None:
        self.components[class_name][component_name] = None
        print("Current components' status =", self.components)

    def add_resent_used(self, class_name:str,component_name: str) -> None:
        # append component name into resent used list
        print("Component", class_name,'.',component_name, "added into resent used list.")

    def open_component_window(self, class_name:str,component_name: str) -> None:
        # if 1 component is already opened, warn
        if self.components[class_name][component_name]:
            self.warn(f"{class_name}.{component_name} 已经打开")
        else:
            # 创建新的 component 对象并显示
            component = self.create_and_save_component(class_name,component_name)
            component.show()
            print("\"", class_name,'.',component_name, "\"", "opened.")
            # append component name into resent used list
            self.add_resent_used(class_name,component_name)
            print("Current components' status =", self.components)
            # connect component closed signal with reset_component()
            component.isClosed.connect(
                lambda: self.reset_component(class_name,component_name))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainWindow = QtWidgets.QMainWindow()
    ui = ToolBoxUI()
    ui.setupUi(mainWindow)
    ui.setupMenubar(mainWindow)
    ui.setupStatusbar(mainWindow)
    ui.setupActions(mainWindow)
    ui.setupConnections(mainWindow)
    ui.setupFinal(mainWindow)
    mainWindow.show()
    app.exec()
