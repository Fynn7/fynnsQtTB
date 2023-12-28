from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QLCDNumber, QMenuBar, QMenu, QMessageBox, QWidget,QDialog,QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, QTime, pyqtSignal,QPropertyAnimation
from PyQt6.QtGui import QAction,QColor

class FuncScaler(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Function Scaler")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.label = QLabel("Enter a scaling factor:")
        self.layout.addWidget(self.label)

        self.scale_button = QPushButton("Scale Function")
        self.scale_button.clicked.connect(self.scale_function)
        self.layout.addWidget(self.scale_button)

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

    def scale_function(self):
        scaling_factor = 2  # Example scaling factor
        # Perform scaling operation on the function

        self.result_label.setText(f"Function scaled by {scaling_factor}")
