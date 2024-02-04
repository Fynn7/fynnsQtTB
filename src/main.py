import sys
import ctypes
import traceback


try:
    from PySide6 import (
        QtCore, 
        QtGui,
        QtWidgets
    )
    from baseWindow import BaseWindow
    from components.tools.pomodoroTimer.pomodoroTimer import PomodoroTimer
    from components.tools.wordSimulator.wordSimulator import WordSimulator
    from components.tools.mlToolBox.mlToolBox import MlToolBox
    from components.games.dice.dice import Dice

except ImportError as ie:
    ctypes.windll.user32.MessageBoxW(0, str(ie), "Import Error",0x10)
    print(traceback.format_exc())
    sys.exit()

except Exception as e:
    ctypes.windll.user32.MessageBoxW(0, str(e), "Unknown Error", 0x10)
    print(traceback.format_exc())
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

    isClosed = QtCore.Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setup_ui()
        self.setup_menubar()
    
    def closeEvent(self, event) -> None:
        '''Override closeEvent by main.py'''
        reply = QtWidgets.QMessageBox.question(self, self.WINDOW_TITLE,
                                               "Are you sure to quit?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,  QtWidgets.QMessageBox.StandardButton.No)

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print(self.WINDOW_TITLE, "closed.")  # DEBUGGER
            event.accept()
        else:
            event.ignore()

    def setup_ui(self):
        self.addWidgetToLayout("QLabel", text="Recent Used Application(s):")

    def setup_menubar(self) -> None:
        self.addBasicMenus()
        menubar = self.getCurrentMenubar()
        # components menu
        components_menu = menubar.addMenu("components")

        # pomodoro timer action
        pomodoro_timer_action = QtGui.QAction("🍅 Pomodoro Timer", self)
        pomodoro_timer_action.triggered.connect(
            lambda: self.open_component_window("Tools", "PomodoroTimer"))
        components_menu.addAction(pomodoro_timer_action)

        # word simulator action
        word_simulator_action = QtGui.QAction("🖋 Word", self)
        word_simulator_action.triggered.connect(
            lambda: self.open_component_window("Tools", "WordSimulator"))
        components_menu.addAction(word_simulator_action)

        # ml toolbox action
        ml_toolbox_action = QtGui.QAction("🤖 Machine Learning", self)
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
        # TODO
        ...

    def open_component_window(self, class_name: str, component_name: str) -> None:
        # if 1 component is already opened, warn
        if self.components[class_name][component_name]:
            self.showMessageBox(msgType="warning",
                                msg=f"{class_name}.{component_name} already opened.")
        else:
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
