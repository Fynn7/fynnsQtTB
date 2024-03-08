from PySide6.QtWidgets import QLabel, QComboBox
from ...templates.fynnsSettingsDialog import FynnsSettingsDialog

class ChooseTable(FynnsSettingsDialog):
    '''
    Example usage:
    ```
    tables: dict[str, pd.DataFrame] = pd.read_excel(
        file_path, sheet_name=None)
    choose_table_dialog = ChooseTable(tables.keys())
    ```
    '''
    def __init__(self, table_names: list,default_table_name: str|None = None):
        super().__init__()
        self.table_names = list(table_names)
        self.default_table_name = default_table_name
        print("ChooseTable().__init__() got table names:", table_names)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Choose Table")
        choose_table_label = QLabel("Choose a table from the selected file:")

        self.choose_table_combobox = QComboBox()
        self.choose_table_combobox.addItems(self.table_names)
        if self.default_table_name:
            self.choose_table_combobox.setCurrentText(self.default_table_name)
        
        self.layout.addWidget(choose_table_label)
        self.layout.addWidget(self.choose_table_combobox)

        # add the OK and Cancel buttons to the dialog (inherited from FynnsSettingsDialog)
        self.add_result_buttonBox()

    def get_chosen_table(self) -> str|None:
        return self.choose_table_combobox.currentText()
