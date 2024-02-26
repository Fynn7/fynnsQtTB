from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
)
from PySide6.QtCore import (
    Qt,
    Signal,
)


class FynnsProgressbar(QDialog):
    '''
    A progressbar dialog for showing the progress of a task
    NOTE: a task as a thread is expected to be running in the background
    
    Attributes:
    progressbar: QProgressBar
    cancel_button: QPushButton
    current_translate_label: QLabel
    
    Methods:
    update_progress: update the progressbar value
    update_current_translate_label: update the current_translate_label text
    
    '''
    # cancel_task:Signal = Signal()
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Fynns Progressbar Prototype")
        layout = QVBoxLayout(self)

        self.progressbar = QProgressBar()
        self.progressbar.setAlignment(Qt.AlignCenter)

        self.cancel_button = QPushButton("Cancel Task")

        self.current_translate_label = QLabel("Progress running...")
        
        layout.addWidget(self.progressbar)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.current_translate_label)
        
        # connect the cancel button to the cancel_task signal
        # self.cancel_button.clicked.connect(lambda: self.cancel_task.emit(True))
        
    def update_progress(self, value:int):
        self.progressbar.setValue(value)

    def update_current_translate_label(self, value:str):
        self.current_translate_label.setText(value)