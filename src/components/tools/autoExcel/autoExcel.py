from PySide6.QtWidgets import (
    QFileDialog,
    QApplication,
    QDialog,
    QTableWidgetItem
)
from PySide6.QtCore import (
    Qt,
    QEvent,
    Slot,
)
from PySide6.QtGui import (
    QWheelEvent,
)
import pandas as pd

from baseWindow import BaseWindow
from .tableHandler import *
from .chooseTable import ChooseTable


class AutoExcel(BaseWindow):
    '''
    Excel Handling Tool
    '''

    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "Auto Excel"
        super().__init__()
        self.setupUi()
        self.setupMenubar()

        # 添加事件过滤器到表格的视口
        self.table.viewport().installEventFilter(self)

        self.chosen_table: str = ""

    def setupUi(self):
        self.file_path_label = self.addWidgetToLayout(
            "QLabel", text="click the button to select file")
        self.select_file_button = self.addWidgetToLayout(
            "QPushButton", text="select file", clickedConn=self.select_file)
        # setup a field to show the table
        # self.table = self.addWidgetToLayout("QTableWidget", rowCount=5, columnCount=5)
        self.table = self.addWidgetToLayout("QTableWidget")

        self.hint_label = self.addWidgetToLayout(
            "QLabel", text="Use Ctrl + Mouse Wheel to zoom in/out")

    def setupMenubar(self):
        self.addBasicMenus(withConfig=False)
        menubar = self.getCurrentMenubar()

    def update_table(self, df: pd.DataFrame) -> None:
        '''
        update the table with the given dataframe

        TODO: it is better to only update the diff (later work)
        '''
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                # if the cell is empty, it will be NaN, so we need to convert it to empty string
                if pd.isna(df.iloc[i, j]):
                    self.table.setItem(i, j, QTableWidgetItem(""))
                else:
                    self.table.setItem(
                        i, j, QTableWidgetItem(str(df.iloc[i, j])))

    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Excel Files (*.xlsx *.xls)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.file_path_label.setText(file_path)
                print("Selected files:", selected_files)

                # get all tables from the excel file
                tables = pd.read_excel(file_path, sheet_name=None)

                table_names = list(tables.keys())
                # create a dialog to select the table with a combo box
                self.chosen_table = self.open_choose_table_dialog(table_names)

                # show the selected table
                self.update_table(tables[self.chosen_table])

            else:
                self.file_path_label.setText("file unselected")
                print("No file selected")

    def open_choose_table_dialog(self, table_names: list) -> str:
        # send last settings of dim and amount of dices to the dialog
        dialog = ChooseTable(table_names)
        # if the dialog is accepted, get the time from the dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # get the time from the dialog
            got_chosen_table = dialog.get_chosen_table()
            print("got_chosen_table:", got_chosen_table)
            return got_chosen_table

    def eventFilter(self, obj, event):
        '''
        使用了 eventFilter 方法来捕获表格视口的滚轮事件。在这个事件过滤器中，检查了Ctrl键的状态，如果Ctrl键被按下，则进行缩放操作，并返回 True 来拦截事件，以阻止其传递给表格。这样，即使鼠标位于表格内部，Ctrl+滚动也会生效。
        '''
        if obj == self.table.viewport():
            if event.type() == QWheelEvent.Wheel:
                modifiers = QApplication.keyboardModifiers()
                if modifiers == Qt.ControlModifier:
                    # Ctrl键被按下
                    delta = event.angleDelta().y() / 120.0  # 获取滚动的角度，正数表示向前滚动，负数表示向后滚动
                    zoom_factor = 1.2  # 缩放因子

                    for col in range(self.table.columnCount()):
                        current_width = self.table.columnWidth(col)
                        new_width = int(
                            current_width * zoom_factor) if delta > 0 else int(current_width / zoom_factor)
                        self.table.setColumnWidth(col, new_width)

                    for row in range(self.table.rowCount()):
                        current_height = self.table.rowHeight(row)
                        new_height = int(
                            current_height * zoom_factor) if delta > 0 else int(current_height / zoom_factor)
                        self.table.setRowHeight(row, new_height)

                    return True  # 拦截事件，不传递给表格

        return super(AutoExcel, self).eventFilter(obj, event)

    # def wheelEvent(self, event: QWheelEvent):
    #     modifiers = QApplication.keyboardModifiers()
    #     if modifiers == Qt.ControlModifier:
    #         # Ctrl键被按下
    #         delta = event.angleDelta().y() / 120.0  # 获取滚动的角度，正数表示向前滚动，负数表示向后滚动
    #         zoom_factor = 1.2  # 缩放因子

    #         for col in range(self.table.columnCount()):
    #             current_width = self.table.columnWidth(col)
    #             new_width = int(current_width * zoom_factor) if delta > 0 else int(current_width / zoom_factor)
    #             self.table.setColumnWidth(col, new_width)

    #         for row in range(self.table.rowCount()):
    #             current_height = self.table.rowHeight(row)
    #             new_height = int(current_height * zoom_factor) if delta > 0 else int(current_height / zoom_factor)
    #             self.table.setRowHeight(row, new_height)

    #     else:
    #         # 如果Ctrl键未被按下，则使用默认的滚动事件处理
    #         super(AutoExcel,self).wheelEvent(event)
