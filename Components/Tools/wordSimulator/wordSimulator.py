from PyQt6.QtWidgets import QApplication, QFileDialog,QMessageBox
from PyQt6.QtCore import pyqtSignal
import sys
from baseWindow import BaseWindow

class WordSimulator(BaseWindow):        
    WINDOW_TITLE = "Word模拟器"
    FILE_SUPPORTED = "记事本(*.txt);;文档(*.doc,*.docx,*.oct);;所有文件 (*)"
    isClosed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)
        self.addBasicMenus()
        self.addWidgetToLayout("QTextEdit")
        self.addWidgetToLayout("QPushButton",text="保存",clickedConn=self.save_document)


    def closeEvent(self, event)->None:
        '''Override the close event to perform custom actions if hasCloseEvent is True.'''
        reply = QMessageBox.question(self, self.WINDOW_TITLE,
                                    "Are you sure to quit?",QMessageBox.StandardButton.Yes |QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply ==QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print(self.WINDOW_TITLE,"closed.") # DEBUGGER
            event.accept()
        else:
            event.ignore()
        event.accept()

    def save_document(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文档", "", self.FILE_SUPPORTED)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    word_simulator = WordSimulator()
    word_simulator.show()
    sys.exit(app.exec())
