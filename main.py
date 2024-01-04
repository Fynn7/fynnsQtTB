import sys
import ctypes
def showSysMsgBox(msg: str|BaseException, title: str, msgType: str = "info") -> None:
    '''Show system default message box.'''
    if msgType == "info":
        ctypes.windll.user32.MessageBoxW(0, str(msg), title, 0)
    elif msgType == "warning":
        ctypes.windll.user32.MessageBoxW(0, str(msg), title, 0x00000030)
    elif msgType == "error":
        ctypes.windll.user32.MessageBoxW(0, str(msg), title, 0x00000010)
    else:
        raise ValueError("msgType must be one of \"info\", \"warning\", \"error\".")
try:
    from PyQt6 import QtCore, QtGui, QtWidgets
    # from .Components.Tools.pomodoroTimer.pomodoroTimer import PomodoroTimer
    # from .Components.Tools.wordSimulator.wordSimulator import WordSimulator
    # from .Components.Tools.mlToolBox.mlToolBox import MlToolBox
    # from .Components.Games.Dice.dice import Dice
    from Components.Tools.pomodoroTimer.pomodoroTimer import PomodoroTimer
    from Components.Tools.wordSimulator.wordSimulator import WordSimulator
    from Components.Tools.mlToolBox.mlToolBox import MlToolBox
    from Components.Games.Dice.dice import Dice
    from baseWindow import BaseWindow
except ImportError as ie:
    showSysMsgBox(ie, title="Import Error", msgType="error")
    sys.exit()

except Exception as e:
    # show system default error message box
    showSysMsgBox(e, title="Unknown Error", msgType="error")
    sys.exit()

class ToolBoxUI(BaseWindow):
    WINDOW_TITLE = "Tool Box"
    components = {
        "Tools": {
            "WordSimulator": None,
            "PomodoroTimer": None,
            "MlToolBox": None, 
            },
        "Games": {
            "Dice": None,
        }
    }

    isClosed = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setupUI()
        self.setupMenubar()

    def closeEvent(self, event) -> None:
        '''Override the close event to perform custom actions if hasCloseEvent is True.'''
        reply = QtWidgets.QMessageBox.question(self, self.WINDOW_TITLE,
                                               "Are you sure to quit?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,  QtWidgets.QMessageBox.StandardButton.No)

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print(self.WINDOW_TITLE, "closed.")  # DEBUGGER
            event.accept()
        else:
            event.ignore()
        event.accept()

    def setupUI(self):
        self.addWidgetToLayout("QLabel", text="Recent Used Application(s):")

    def setupMenubar(self) -> None:
        self.addBasicMenus()
        menubar = self.getCurrentMenubar()
        # components menu
        components_menu = menubar.addMenu("components")
        # pomodoro timer action
        pomodoro_timer_action = QtGui.QAction("pomodoro timer", self)
        pomodoro_timer_action.triggered.connect(
            lambda: self.open_component_window("Tools", "PomodoroTimer"))
        components_menu.addAction(pomodoro_timer_action)

        # word simulator action
        word_simulator_action = QtGui.QAction("word simulator", self)
        word_simulator_action.triggered.connect(
            lambda: self.open_component_window("Tools", "WordSimulator"))
        components_menu.addAction(word_simulator_action)

        # ml toolbox action
        ml_toolbox_action = QtGui.QAction("ml toolbox", self)
        ml_toolbox_action.triggered.connect(
            lambda: self.open_component_window("Tools", "MlToolBox"))
        components_menu.addAction(ml_toolbox_action)

    def create_and_save_component(self, class_name: str, component_name: str) -> QtWidgets.QMainWindow:
        try:
            component: QtWidgets.QMainWindow = eval(f"{component_name}()")
            # save component object, otherwise it will be deleted directly after opening this component window
            self.components[class_name][component_name] = component
            return component
        except NameError as e:
            self.showMessageBox(msgType="warning",
                                msg=f"Component {component_name} under class {class_name} not found.\nOriginal error message:\n{e}")
            raise NameError(e)
        except Exception as e:
            self.showMessageBox(msgType="warning",
                                msg=f"Unknown error when creating component {component_name} under class {class_name}.\nOriginal error message:\n{e}")
            raise Exception(e)

    def reset_component(self, class_name: str, component_name: str) -> None:
        self.components[class_name][component_name] = None
        print("Current components' status =", self.components)

    def add_resent_used(self, class_name: str, component_name: str) -> None:
        # append component name into resent used list
        print("Component", class_name, '.', component_name,
              "added into resent used list.")

    def open_component_window(self, class_name: str, component_name: str) -> None:
        # if 1 component is already opened, warn
        if self.components[class_name][component_name]:
            self.showMessageBox(msgType="warning",
                                msg=f"{class_name}.{component_name} 已经打开")
        else:
            # 创建新的 component 对象并显示
            component = self.create_and_save_component(
                class_name, component_name)
            component.show()
            print("\"", class_name, '.', component_name, "\"", "opened.")
            # append component name into resent used list
            self.add_resent_used(class_name, component_name)
            print("Current components' status =", self.components)
            # connect component closed signal with reset_component()
            component.isClosed.connect(
                lambda: self.reset_component(class_name, component_name))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainWindow = ToolBoxUI()
    mainWindow.show()
    app.exec()
