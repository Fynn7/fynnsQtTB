import sys
import ctypes
import traceback
import json

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

    from components.basic.shop import Shop

except ImportError as ie:
    ctypes.windll.user32.MessageBoxW(0, str(ie), "Import Error",0x10)
    print(traceback.format_exc())
    sys.exit()

except Exception as e:
    ctypes.windll.user32.MessageBoxW(0, str(e), "Unknown Error", 0x10)
    print(traceback.format_exc())
    sys.exit()


class ToolBoxUI(BaseWindow):
    components = {
        "Tools": {
            "WordSimulator": None,
            "PomodoroTimer": None,
            "MlToolBox": None, 
            },
        "Games": {
            "Dice": None,
            "Poker":None,
        },
        "Basic": {
            "Shop": None,
        }
    }

    def __init__(self):
        self.WINDOW_TITLE = "Tool Box" # overwriting the parent class attribute before parent calling its __init__
        super().__init__()
        self.setup_ui()
        self.setup_menubar()


    def setup_ui(self)->None:
        self.addWidgetToLayout("QLabel", text="Nothing to show (but later can used as a notification area instead of pop-up windows)")

    def setup_menubar(self) -> None:
        # add basic menus (baseWindow parent method)
        self.addBasicMenus()
        
        menubar = self.getCurrentMenubar()

        # tool menu
        tool_menu = menubar.addMenu("Tools")

        # pomodoro timer action
        pomodoro_timer_action = QtGui.QAction("🍅 Pomodoro Timer", self)
        pomodoro_timer_action.triggered.connect(
            lambda: self.open_component_window("Tools", "PomodoroTimer"))
        tool_menu.addAction(pomodoro_timer_action)

        # word simulator action
        word_simulator_action = QtGui.QAction("🖋 Word", self)
        word_simulator_action.triggered.connect(
            lambda: self.open_component_window("Tools", "WordSimulator"))
        tool_menu.addAction(word_simulator_action)

        # ml toolbox action
        ml_toolbox_action = QtGui.QAction("🤖 Machine Learning", self)
        ml_toolbox_action.triggered.connect(
            lambda: self.open_component_window("Tools", "MlToolBox"))
        tool_menu.addAction(ml_toolbox_action)


        # game menu
        game_menu = menubar.addMenu("Games")

        # dice action
        dice_action = QtGui.QAction("🎲 Dice", self)
        dice_action.triggered.connect(
            lambda: self.open_component_window("Games", "Dice"))
        game_menu.addAction(dice_action)


        # shop action: directly add to base menubar
        init_balance:float= json.load(open("src/data.json", "r"))["balance"]
        shop_action = QtGui.QAction(str(init_balance)+" €", self)
        shop_action.triggered.connect(
            lambda: self.open_component_window("Basic", "Shop"))
        menubar.addAction(shop_action)

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

    @QtCore.Slot()
    def reset_component(self, class_name: str, component_name: str) -> None:
        self.components[class_name][component_name] = None
        print("Current components' status =", self.components)


    @QtCore.Slot()
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
            print("Current components' status =", self.components)
            # connect component closed signal with reset_component()
            component.isClosed.connect(
                lambda: self.reset_component(class_name, component_name))
            component.changed_balance.connect(self.update_balance)

    @QtCore.Slot(float)
    def update_balance(self, new_balance: float) -> None:
        # update main window display
        self.getCurrentMenubar().actions()[4].setText(str(new_balance)+" €")
        json.dump({"balance": new_balance}, open("src/data.json", "w"))
        print("Balance updated to", new_balance, "€")

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = ToolBoxUI()
    mainWindow.show()
    sys.exit(app.exec())
             
if __name__ == "__main__":
    main()