from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox


class ChooseTable(QDialog):
    def __init__(self, table_names: list):
        super().__init__()

        self.table_names = table_names
        print("got table names:", table_names)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Choose Table")
        layout = QVBoxLayout(self)

        choose_table_label = QLabel("Choose a table from the selected file:")

        self.choose_table_combobox = QComboBox()
        self.choose_table_combobox.addItems(self.table_names)

        result_buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        result_buttonBox.accepted.connect(self.accept)
        result_buttonBox.rejected.connect(self.reject)

        layout.addWidget(choose_table_label)
        layout.addWidget(self.choose_table_combobox)

        layout.addWidget(result_buttonBox)

    def get_chosen_table(self) -> str:
        return self.choose_table_combobox.currentText()
