from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6.QtCore import Signal
import sys
from baseWindow import BaseWindow


class WordSimulator(BaseWindow):
    WINDOW_TITLE = "Word"
    FILE_SUPPORTED = "Notebook(*.txt);;Word File(*.doc,*.docx,*.oct);;All Files (*)"
    isClosed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)
        self.addBasicMenus()
        self.addWidgetToLayout("QTextEdit")
        self.addWidgetToLayout("QPushButton", text="Save",
                               clickedConn=self.save_document)

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self, self.WINDOW_TITLE,
                                     "Are you sure to quit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print(self.WINDOW_TITLE, "closed.")  # DEBUGGER
            event.accept()
        else:
            event.ignore()
        event.accept()

    def save_document(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save", "", self.FILE_SUPPORTED)
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_edit.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    word_simulator = WordSimulator()
    word_simulator.show()
    sys.exit(app.exec())
