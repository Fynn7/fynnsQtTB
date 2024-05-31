from baseWindow import BaseWindow
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtCore import (
    Slot,
    QTimer,
)


class Hangman(BaseWindow):
    def __init__(self) -> None:
        self.WINDOW_TITLE = "Hangman"
        super(Hangman, self).__init__()
        self.setup_ui()
        self.setup_menubar()

    def setup_ui(self):
        layout = QVBoxLayout()
        # Substitute with real image later
        self.img_hangman = QLabel("Trial left: -")
        layout.addWidget(self.img_hangman)

        self.word = QLabel("")
        layout.addWidget(self.word)

        self.start_game_button = QPushButton("Start Game")
        self.start_game_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_game_button)
        self.setLayout(layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def setup_menubar(self):
        menubar = self.menuBar()
        ...

    def choose_word(self)->str:
        from pandas import read_csv
        import random
        words = read_csv("src/components/games/hangman/words.csv")
        word = random.choice(words)
        return word

    @Slot()
    def start_game(self):
        self.word_to_guess = self.choose_word()
        self.word.setText(f"{'_ ' * len(self.word_to_guess)}")
        self.start_game_button.setEnabled(False)
        self.trial = 6
        self.img_hangman.setText(f"Trial left: {self.trial}")
    