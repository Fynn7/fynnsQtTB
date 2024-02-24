from ...templates.fynnsProgressbar import FynnsProgressbar

class ShowProgressbar(FynnsProgressbar):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Translate Progress")
        self.current_translate_label.setText("Translate running...")