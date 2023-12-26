from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QAction
class Window1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        button = QPushButton("Go to Window 2")
        button.clicked.connect(self.goToWindow2)
        layout.addWidget(button)
    
    def goToWindow2(self):
        self.window2 = Window2()
        self.window2.show()
        self.hide()

class Window2(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        button = QPushButton("Go to Window 1")
        button.clicked.connect(self.goToWindow1)
        layout.addWidget(button)
    
    def goToWindow1(self):
        self.window1 = Window1()
        self.window1.show()
        self.hide()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.window1 = Window1()
        self.setCentralWidget(self.window1)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()