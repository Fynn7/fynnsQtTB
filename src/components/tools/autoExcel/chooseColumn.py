from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox, QDialogButtonBox, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt


class ChooseColumn(QDialog):
    def __init__(self, column_names: list):
        super().__init__()

        self.column_names = column_names
        print("got column names:", column_names)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Choose Column")
        layout = QVBoxLayout(self)

        choose_column_label = QLabel("Choose columns to execute the function:")

        # add a QListWidget to allow multiple selection of columns
        self.choose_column_listwidget = QListWidget()

        for column_name in self.column_names:
            column_item = QListWidgetItem(column_name)
            column_item.setFlags(column_item.flags() | Qt.ItemIsUserCheckable)
            column_item.setCheckState(Qt.Checked)
            # check item state change

            self.choose_column_listwidget.addItem(column_item)

        # check if all items are checked
        self.choose_column_listwidget.itemChanged.connect(self.check_all_selected)

        # add a checkbox for select/deselect all
        self.select_all_checkbox = QCheckBox("Select All")
        self.select_all_checkbox.setCheckState(Qt.Checked)
        self.select_all_checkbox.stateChanged.connect(self.select_all)

        result_buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        result_buttonBox.accepted.connect(self.accept)
        result_buttonBox.rejected.connect(self.reject)

        layout.addWidget(choose_column_label)
        layout.addWidget(self.choose_column_listwidget)
        layout.addWidget(self.select_all_checkbox)
        layout.addWidget(result_buttonBox)

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

    def get_chosen_columns(self) -> list:
        chosen_columns = []
        for i in range(self.choose_column_listwidget.count()):
            item = self.choose_column_listwidget.item(i)
            if item.checkState() == Qt.Checked:
                chosen_columns.append(self.column_names[i])
        return chosen_columns
