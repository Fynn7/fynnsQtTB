from PySide6.QtWidgets import QLabel, QDialog,QPushButton 
from ...templates.fynnsSettingsDialog import FynnsSettingsDialog
from .chooseTable import ChooseTable
from .chooseColumn import ChooseColumn

class CustomDict(FynnsSettingsDialog):
    def __init__(self,):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Custom Dictionary")
        choose_table_label = QLabel("Choose a table from the selected file:")
        select_ = QPushButton("Select File")
        select_table_button.clicked.connect(self.open_choose_table_dialog)
        self.layout.addWidget(choose_table_label)
        self.layout.addWidget(select_table_button)


        self.add_result_buttonBox()

    def open_choose_table_dialog(self, table_names: list,default_table_name:str|None=None) -> str | None:
        dialog = ChooseTable(table_names,default_table_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            got_chosen_table = dialog.get_chosen_table()
            print("got_chosen_table:", got_chosen_table)
            return got_chosen_table
        
    def open_choose_column