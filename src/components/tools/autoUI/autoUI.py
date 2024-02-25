import pyautogui
import time

from baseWindow import BaseWindow

class AutoUI(BaseWindow):
    def __init__(self):
        self.WINDOW_TITLE = "AutoUI"
        super().__init__()
        self.setup_ui()
        self.short_cut:str=""
    def setup_ui(self):
        self.addWidgetToLayout("QLable", "press "+self.short_cut+" to start auto-click")

