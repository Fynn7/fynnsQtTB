from baseWindow import BaseWindow
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtCore import (
    Slot
)
from .poker21 import Poker21

class Poker(BaseWindow):
    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "Poker Game"
        super(Poker, self).__init__()
        self.setup_ui()
        self.setup_menubar()
        self.poker21:Poker21=None

    def setup_ui(self):
        self.addWidgetToLayout("QPushButton", "Poker21", self.play_poker21)

    def setup_menubar(self):
        self.addBasicMenus(False,withConfig=True)
    
    @Slot()
    def play_poker21(self):
        if not self.poker21:
            self.poker21 = Poker21()    
        self.poker21.show()
        