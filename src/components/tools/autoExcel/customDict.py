from PySide6.QtWidgets import (
    QLabel,
    QDialog,
    QMessageBox,
    QScrollArea,
)
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QAction,
)
import pandas as pd

from baseWindow import BaseWindow
from .chooseTable import ChooseTable
from .chooseColumn import ChooseColumn
from ...templates.fynnsComponents import _select_file


class CustomDict(BaseWindow):
    def __init__(self):
        self.WINDOW_TITLE = "Custom Dictionary/Mapping Settings"
        super().__init__()
        self.setup_ui()
        self.setup_menubar()
        self.data: dict = self.load_data()["custom_dicts"]

    def setup_ui(self):
        self.addWidgetToLayout(
            "QLabel", "Choose a table from the selected file:")
        self.addWidgetToLayout(
            "QPushButton", "Select Table", self.select_column)
        self.mapping_name_input = self.addWidgetToLayout(
            "QLineEdit", "Mapping 1")
        self.mapping_name_input.setPlaceholderText(
            "Enter a name for the mapping")

        # create a scrollable area for the settings
        self.custom_dict_storage_scrollArea = QScrollArea()
        self.custom_dict_storage_scrollArea.setWidgetResizable(True)
        self.custom_dict_storage_scrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOn)
        self.custom_dict_storage_label = QLabel(
            "Saved Dictionary/Mapping:\n\n")
        self.custom_dict_storage_label.setWordWrap(True)
        self.custom_dict_storage_scrollArea.setWidget(
            self.custom_dict_storage_label)
        layout = self.getLayout()
        layout.addWidget(self.custom_dict_storage_scrollArea)

    def setup_menubar(self):
        menubar = self.getCurrentMenubar()
        settings_menu = menubar.addMenu("Settings")
        clear_storage_action = QAction(
            "Clear All Permanent Mapping Storage", self)
        clear_storage_action.triggered.connect(self.clear_storage)
        settings_menu.addAction(clear_storage_action)

    def select_column(self) -> None:
        # check if the mapping name is empty
        if not self.mapping_name_input.text():
            QMessageBox.critical(self, "No Mapping Name",
                                 "Please enter a name for the mapping.")
            return
        file_path = _select_file(
            "Excel Files (*.xlsx *.xls *.csv);; CSV Files (*.csv)")
        if not file_path:
            return

        if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            # get all tables from the excel file
            tables: dict[str, pd.DataFrame] = pd.read_excel(
                file_path, sheet_name=None)
            # create a new window to select the table
            choose_table_dialog = ChooseTable(tables.keys())
            if choose_table_dialog.exec() == QDialog.DialogCode.Accepted:
                got_chosen_table_name: str = choose_table_dialog.get_chosen_table()
                got_chosen_table: pd.DataFrame = tables[got_chosen_table_name]
            else:
                # user canceled the selection
                return
        elif file_path.endswith(".csv"):
            got_chosen_table: pd.DataFrame = pd.read_csv(file_path)
        else:
            QMessageBox.critical(self, "Unsupported File Type",
                                 "The file type is not supported. Please select an Excel file or a CSV file.")
            # call the function again
            self.select_column()

        # first choose the keys of the dictionary
        choose_column_dialog = ChooseColumn(
            got_chosen_table.columns, only_choose_one=True, description="Choose the keys of the dictionary:")
        if choose_column_dialog.exec() == QDialog.DialogCode.Accepted:
            got_chosen_keys_column: str = choose_column_dialog.get_chosen_columns()[
                0]
            print("CustomDict().select_column() got chosen keys column:",
                  got_chosen_keys_column)
        else:
            # user canceled the selection
            return

        # then choose the values of the dictionary
        # the user can choose multiple columns, and the values of the dictionary will be a list of the values of the chosen columns
        choose_column_dialog = ChooseColumn(
            got_chosen_table.columns, only_choose_one=False, description="Choose the values of the dictionary:")
        if choose_column_dialog.exec() == QDialog.DialogCode.Accepted:
            got_chosen_values_columns: list = choose_column_dialog.get_chosen_columns()
            print("CustomDict().select_column() got chosen values column:",
                  got_chosen_values_columns)
        else:
            # user canceled the selection
            return

        # create the dictionary, keys are the values of the chosen keys column, values are the values of the chosen values columns
        # dictionary = {key: [value1, value2, ...], ...}
        mapping_name = self.mapping_name_input.text()
        self.data[mapping_name] = dict(zip(
            got_chosen_table[got_chosen_keys_column], got_chosen_table[got_chosen_values_columns].values.tolist()))

        print("CustomDict().select_column() created dictionary:", self.data)

        # update the label to show the saved dictionary/mapping
        s = "Saved Dictionary/Mapping:\n\n"
        for d in self.data:
            s += f"{d}:\n{self.data[d]}\n\n"
        self.custom_dict_storage_label.setText(s)

        # save the dictionary to the data file
        self.update_data_file({
            "custom_dicts": self.data
        })

    def clear_storage(self):
        # ask the user if they really want to clear the storage
        reply = QMessageBox.question(
            self, "Clear Storage", "Do you really want to clear all the mapping storage?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.update_data_file({
                "custom_dicts": {}
            })
            print("CustomDict().clear_storage() cleared storage.")
            self.custom_dict_storage_label.setText(
                "Saved Dictionary/Mapping:\n\n")

    def get_settings_data(self) -> dict:
        return self.data
