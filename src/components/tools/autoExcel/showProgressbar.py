from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton
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

        self.cancel_button = QPushButton("Cancel Translation")

        self.current_translate_label = QLabel("Translating ...")
        
        layout.addWidget(self.progressbar)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.current_translate_label)
        
    def update_progress(self, value:int):
        self.progressbar.setValue(value)

    def update_current_translate_label(self, value:str):
        self.current_translate_label.setText(value)
