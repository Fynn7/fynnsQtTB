from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QFileDialog, QPushButton, QWidget,QMessageBox
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import pyqtSignal
import sys

class WordSimulator(QMainWindow):        
    WINDOW_TITLE = "Word模拟器"
    WINDOW_SIZE = (800, 600)
    FILE_SUPPORTED = "记事本(*.txt);;文档(*.doc,*.docx,*.oct);;所有文件 (*)"
    isClosed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_document)
        layout.addWidget(self.save_button)

        central_widget.setLayout(layout)

    def save_document(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文档", "", self.FILE_SUPPORTED)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def closeEvent(self, event)->None:
        # 重写(overwrite)关闭事件
        reply = QMessageBox.question(self, '提示',
                                     "确定退出吗?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print("PomodoroTimer closed.")
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    word_simulator = WordSimulator()
    word_simulator.show()
    sys.exit(app.exec())
