from baseWindow import BaseWindow
from PySide6 import QtWidgets

class Dice(BaseWindow):
    def __init__(self):
        self.WINDOW_TITLE = "Dice Game" # overwriting the parent class attribute before parent calling its __init__
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

    def closeEvent(self, event) -> None:
        super().closeEvent(event)
        print("Dice Game Closed")