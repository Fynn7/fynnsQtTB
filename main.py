import sys
import ctypes
import traceback

try:
    from PySide6.QtCore import (
        Slot,
        Signal
    )
    from PySide6.QtWidgets import (
        QMainWindow,
        QApplication
    )
    from PySide6.QtGui import (
        QAction,
    )
    from baseWindow import BaseWindow
    from src.components.tools.pomodoroTimer.pomodoroTimer import PomodoroTimer
    from src.components.tools.mlToolBox.mlToolBox import MlToolBox
    from src.components.tools.autoExcel.autoExcel import AutoExcel
    from src.components.tools.autoXHS.autoXHS import AutoXHS
    from src.components.tools.dsToolBox.dsToolBox import DSToolBox
    from src.components.tools.gpaCalculator.gpaCalculator import GPACalculator

    from src.components.games.dice.dice import Dice
    from src.components.games.poker.poker21 import Poker21

    from src.components.basic.shop import Shop
    from src.components.basic.emoji import EmojiThread, Emoji
    from src.components.basic.inventory import Inventory

except ImportError as ie:
    ctypes.windll.user32.MessageBoxW(
        0, str(ie)+"\n\nActivate venv and try again!", "Import Error", 0x10)
    print(traceback.format_exc())
    sys.exit()

except Exception as e:
    ctypes.windll.user32.MessageBoxW(0, str(e), "Unknown Error", 0x10)
    print(traceback.format_exc())
    sys.exit()


class ToolBoxUI(BaseWindow):
    # window obj control
    components: dict = {
        "Tools": {
            "PomodoroTimer": None,
            "MlToolBox": None,
            "AutoExcel": None,
            "AutoXHS": None,
            "DSToolBox": None,
            "GPACalculator": None,
        },
        "Games": {
            "Dice": None,
            "Poker21": None,
        },
        "Basic": {
            "Shop": None,
            "Emoji": None,
            "Inventory": None,
        }
    }

    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "Fynns Metaverse Playground"
        super().__init__()
        self.setup_ui()
        self.setup_menubar()
        # initialize emoji thread
        self.components["Basic"]["Emoji"] = EmojiThread(
            self.load_data()["emoji"])
        self.emoji_thread = self.components["Basic"]["Emoji"]
        # emoji signal connection
        self.emoji_thread.emoji_signals_updated.connect(
            self.handle_emoji_status_updated)
        self.emoji_thread.message_updated.connect(
            self.handle_emoji_message_updated)
        self.emoji_thread.start()

    def setup_ui(self) -> None:
        self.addWidgetToLayout(
            "QLabel", text="Welcome to Fynn's metaverse playground.\nNothing to show (but later can used as a notification area instead of pop-up windows)\nDieses Programm ist natürlich gar nicht großartig, aber ich kann alles herumspielen, was ich will.")

    def setup_menubar(self) -> None:
        # add basic menus (baseWindow parent method)
        self.addBasicMenus(withFile=False)

        menubar = self.menuBar()

        # file menu
        file_menu = menubar.addMenu("File")

        # reset data action
        reset_data_action = QAction("Reset Data", self)
        reset_data_action.triggered.connect(self.reset_data_with_gui)
        file_menu.addAction(reset_data_action)

        ############################################################
        # tool menu
        tool_menu = menubar.addMenu("Tools")

        # pomodoro timer action
        pomodoro_timer_action = QAction("🍅 Pomodoro Timer", self)
        pomodoro_timer_action.triggered.connect(
            lambda: self.open_component_window("Tools", "PomodoroTimer"))
        tool_menu.addAction(pomodoro_timer_action)

        # ml toolbox action
        ml_toolbox_action = QAction("🤖 Machine Learning", self)
        ml_toolbox_action.triggered.connect(
            lambda: self.open_component_window("Tools", "MlToolBox"))
        tool_menu.addAction(ml_toolbox_action)

        # auto excel action
        auto_excel_action = QAction("📊 Auto Excel", self)
        auto_excel_action.triggered.connect(
            lambda: self.open_component_window("Tools", "AutoExcel"))
        tool_menu.addAction(auto_excel_action)

        # auto xhs action
        auto_xhs_action = QAction("📕 Auto XiaoHongShu", self)
        auto_xhs_action.triggered.connect(
            lambda: self.open_component_window("Tools", "AutoXHS"))
        auto_xhs_action.setDisabled(True)
        tool_menu.addAction(auto_xhs_action)

        # data science toolbox action
        ds_toolbox_action = QAction("📈 Data Science", self)
        ds_toolbox_action.triggered.connect(
            lambda: self.open_component_window("Tools", "DSToolBox"))
        tool_menu.addAction(ds_toolbox_action)

        # credits calculator action
        credit_calculator_action = QAction("💯 Credit Calculator", self)
        credit_calculator_action.triggered.connect(
            lambda: self.open_component_window("Tools", "GPACalculator")
        )
        tool_menu.addAction(credit_calculator_action)

        ############################################################
        # game menu
        game_menu = menubar.addMenu("Games")

        # dice action
        dice_action = QAction("🎲 Dice", self)
        dice_action.triggered.connect(
            lambda: self.open_component_window("Games", "Dice"))
        game_menu.addAction(dice_action)

        # poker action
        poker_action = QAction("🃏 Poker", self)
        poker_action.triggered.connect(
            lambda: self.open_component_window("Games", "Poker21"))
        game_menu.addAction(poker_action)

        ############################################################
        # shop action: directly add to base menubar
        init_balance: float = self.load_data()["balance"]
        shop_action = QAction(str(init_balance)+" €", self)
        shop_action.triggered.connect(
            lambda: self.open_component_window("Basic", "Shop"))
        menubar.addAction(shop_action)

        # bank action
        bank_action = QAction("🏦 Bank", self)
        bank_action.setDisabled(True)
        menubar.addAction(bank_action)

        # inventory action
        inventory_action = QAction("🎒 Inventory", self)
        inventory_action.triggered.connect(
            lambda: self.open_component_window("Basic", "Inventory"))
        menubar.addAction(inventory_action)

        # emoji menu
        emoji_menu = menubar.addMenu("😊")
        menubar.addMenu(emoji_menu)

        # study action
        study_action = QAction("📚 Study", self)
        study_action.setDisabled(True)
        emoji_menu.addAction(study_action)

        # work action
        work_action = QAction("💼 Work", self)
        work_action.setDisabled(True)
        emoji_menu.addAction(work_action)

        # message action: display what the emoji says
        message_action = QAction("Hey there", self)
        message_action.setDisabled(True)
        menubar.addAction(message_action)

        # hunger action: display emoji hunger
        hunger_action = QAction("100", self)
        hunger_action.triggered.connect(
            lambda: self.components["Basic"]["Emoji"].emoji_obj.operate("feed", 100))
        hunger_action.triggered.connect(
            lambda: self.handle_emoji_message_updated("Feeding..."))

        emoji_menu.addAction(hunger_action)

        # cleanliness action: display emoji cleanliness
        cleanliness_action = QAction("100", self)
        cleanliness_action.triggered.connect(
            lambda: self.components["Basic"]["Emoji"].emoji_obj.operate("clean", 100))
        cleanliness_action.triggered.connect(
            lambda: self.handle_emoji_message_updated("Cleaning..."))

        emoji_menu.addAction(cleanliness_action)

        # health action: display emoji health
        health_action = QAction("100", self)
        health_action.triggered.connect(
            lambda: self.components["Basic"]["Emoji"].emoji_obj.operate("heal", 100))
        health_action.triggered.connect(
            lambda: self.handle_emoji_message_updated("Healing..."))
        emoji_menu.addAction(health_action)

        # level action: display emoji level
        level_action = QAction("level 0", self)
        level_action.setDisabled(True)
        emoji_menu.addAction(level_action)

    def create_and_save_component(self, class_name: str, component_name: str) -> QMainWindow:
        try:
            component: QMainWindow = eval(f"{component_name}()")
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

    @Slot()
    def reset_component(self, class_name: str, component_name: str) -> None:
        self.components[class_name][component_name] = None
        print("Current components' status =", self.components)

    @Slot(dict)
    def handle_emoji_status_updated(self, emoji_data: dict) -> None:
        # write emoji to file
        self.update_data_file({"emoji": emoji_data})
        menubar = self.menuBar()
        emoji_menu = menubar.actions()[7].menu()
        emoji_menu.setTitle(emoji_data["emoji"])

        hunger_item = emoji_menu.actions()[2]
        hunger_item.setText(
            ''.join([str(emoji_data["status"]["hunger"]), '/100', ' 🍔']))

        cleanliness_item = emoji_menu.actions()[3]
        cleanliness_item.setText(
            ''.join([str(emoji_data["status"]["cleanliness"]), '/100', ' 🚿']))

        health_item = emoji_menu.actions()[4]
        health_item.setText(
            ''.join([str(emoji_data["status"]["health"]), '/100', ' 💗']))

    @Slot(str)
    def handle_emoji_message_updated(self, emoji_message: str) -> None:
        menubar = self.menuBar()
        msg_item = menubar.actions()[8]
        msg_item.setText(emoji_message)

    @Slot()
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

            # connect component balance changed signal with update_balance()
            component.changed_balance.connect(self.update_balance)

            # connect component bought item signal with update_balance()
            if component.WINDOW_TITLE == "Shop":
                component.add_item_to_inventory_signal.connect(
                    self.add_item_to_inventory)
            elif component.WINDOW_TITLE == "My Inventory":
                component.consume_item_signal.connect(
                    self.consume_item_from_inventory)
                # remove item after consuming

    @Slot(float)
    def update_balance(self, new_balance: float) -> None:
        # update main window GUI
        menubar = self.menuBar()
        menubar.actions()[4].setText(str(new_balance)+" €")
        # update data file
        self.update_data_file({"balance": new_balance})
        print("Balance updated to", new_balance, "€")

    @Slot(dict)
    def add_item_to_inventory(self, item: dict) -> None:
        items: list = self.load_data()["inventory"]
        dup_index:int=-1

        inventory: Inventory = self.components["Basic"]["Inventory"]

        for i in range(len(items)):
            if items[i]["id"] == item["id"]:
                dup_index = i
                break
        
        if dup_index != -1:
            items[dup_index]["amount"] += item["amount"]
            # update the item in the list widget
            if inventory:
                inventory.update_item_amount(item["id"], items[dup_index]["amount"])
        else:
            items.append(item)
            if inventory:
                inventory.add_item(item)

        self.update_data_file({"inventory": items})
        print("Item added to inventory:", item)

    @Slot(dict)
    def consume_item_from_inventory(self, item: dict) -> None:
        '''
        NOTE: values from emoji_thread.emoji_obj cannot be directly disturbed by main thread!!!
        Must control emoji thread itself
        '''
        emoji_thread: EmojiThread = self.components["Basic"]["Emoji"]
        emoji_thread.update_status(**item["attributes"])

        # remove item from inventory
        inventory: Inventory = self.components["Basic"]["Inventory"]
        if inventory:  # if the inventory window is open
            inventory.remove_item(item)

    def reset_data_with_gui(self) -> None:
        self.reset_data()
        # reset gui
        current_data = self.load_data()
        menubar = self.menuBar()
        menubar.actions()[4].setText(
            str(current_data["balance"])+" €")

    def closeEvent(self, event) -> None:
        self.emoji_thread.terminate()
        self.emoji_thread.wait()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    mainWindow = ToolBoxUI()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
