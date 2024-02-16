from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QThread
from PySide6.QtCore import Signal
import time


class ShowProgressbar(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Progress")
        layout = QVBoxLayout(self)

        self.progressbar = QProgressBar()
        self.progressbar.setAlignment(Qt.AlignCenter)

        
        layout.addWidget(self.progressbar)

    def update_progress(self, value):
        self.progressbar.setValue(value)