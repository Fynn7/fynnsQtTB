from PySide6.QtWidgets import QLabel, QCheckBox, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from ...templates.fynnsSettingsDialog import FynnsSettingsDialog

class ChooseColumn(FynnsSettingsDialog):
    def __init__(self, column_names: list,only_choose_one:bool=False,description:str="Choose columns to execute the function:"):
        super().__init__()

        self.column_names = list(column_names)
        self.only_choose_one = only_choose_one
        self.description = description
        print("ChooseColumn().__init__() got column names:", column_names)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Choose Column")
        choose_column_label = QLabel(self.description)

        # add a QListWidget to allow multiple selection of columns
        self.choose_column_listwidget = QListWidget()

        for column_name in self.column_names:
            column_item = QListWidgetItem(column_name)
            column_item.setFlags(column_item.flags() | Qt.ItemIsUserCheckable)
            column_item.setCheckState(Qt.Unchecked)
            # check item state change

            self.choose_column_listwidget.addItem(column_item)

        # check if all items are checked
        self.choose_column_listwidget.itemChanged.connect(self.check_all_selected)

        # add a checkbox for select/deselect all
        self.select_all_checkbox = QCheckBox("Select All")
        self.select_all_checkbox.setCheckState(Qt.Unchecked)
        self.select_all_checkbox.stateChanged.connect(self.select_all)

        self.layout.addWidget(choose_column_label)
        self.layout.addWidget(self.choose_column_listwidget)
        self.layout.addWidget(self.select_all_checkbox)

        # if the user didn't choose any column, then disable the OK button
        self.choose_column_listwidget.itemChanged.connect(self.check_any_selected)

        if self.only_choose_one:
            self.select_all_checkbox.hide()
        # add the OK and Cancel buttons, inherited from FynnsSettingsDialog
        self.result_buttonBox=self.add_result_buttonBox()
        # to avoid the OK button to be enabled when no item is selected!
        self.result_buttonBox.button(self.result_buttonBox.StandardButton.Ok).setEnabled(False)
    def select_all(self, state: Qt.CheckState):
        states = {
            0: Qt.Unchecked,
            2: Qt.Checked
        }
        for i in range(self.choose_column_listwidget.count()):
            column_item = self.choose_column_listwidget.item(i)
            column_item.setCheckState(states[state])

    def check_all_selected(self, item):
        all_selected = all(self.choose_column_listwidget.item(i).checkState() == Qt.Checked for i in range(self.choose_column_listwidget.count()))
        self.select_all_checkbox.blockSignals(True)
        self.select_all_checkbox.setChecked(all_selected)
        self.select_all_checkbox.blockSignals(False)
    
    def check_any_selected(self, item):
        any_selected = any(self.choose_column_listwidget.item(i).checkState() == Qt.Checked for i in range(self.choose_column_listwidget.count()))
        # if any item is selected, then hide all other items
        if self.only_choose_one:
            if any_selected:
                for i in range(self.choose_column_listwidget.count()):
                    column_item = self.choose_column_listwidget.item(i)
                    if column_item.checkState() == Qt.Unchecked:
                        column_item.setHidden(True)
            else:
                for i in range(self.choose_column_listwidget.count()):
                    column_item = self.choose_column_listwidget.item(i)
                    column_item.setHidden(False)

        # to avoid the OK button to be enabled when no item is selected!
        if any_selected:
            self.result_buttonBox.button(self.result_buttonBox.StandardButton.Ok).setEnabled(True)
        else:
            self.result_buttonBox.button(self.result_buttonBox.StandardButton.Ok).setEnabled(False)
    def get_chosen_columns(self) -> list:
        chosen_columns = []
        for i in range(self.choose_column_listwidget.count()):
            item = self.choose_column_listwidget.item(i)
            if item.checkState() == Qt.Checked:
                chosen_columns.append(self.column_names[i])
        return chosen_columns
