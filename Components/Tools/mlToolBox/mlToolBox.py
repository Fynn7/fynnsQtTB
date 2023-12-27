from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt6.QtCore import pyqtSignal

class MlToolBox(QMainWindow):
    WINDOW_TITLE = "PDF OCR识别翻译"
    WINDOW_SIZE = (400, 200)
    isClosed = pyqtSignal(bool)
    