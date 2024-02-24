from PySide6.QtWidgets import (
    QFileDialog,
    QApplication,
    QDialog,
    QTableWidgetItem,
    QMessageBox,
    QWidget,
)
from PySide6.QtCore import (
    Qt,
    Slot,
    QThread,
    Signal,
)
from PySide6.QtGui import (
    QWheelEvent,
    QAction,
)
import pandas as pd
import functools


from baseWindow import BaseWindow
from .tableHandler import TranslationThread
from .chooseTable import ChooseTable
from .chooseColumn import ChooseColumn
from .showProgressbar import ShowProgressbar


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
        self.table_field.viewport().installEventFilter(self)

        # as long as something in the table is changed, it will be marked as changed
        self.table_field.itemChanged.connect(self.mark_as_changed)
        self.table_changed: bool = False
        # chosen table: (table name, table dataframe)
        self.chosen_table_name: str = ""
        self.tables: dict[str, pd.DataFrame] = {}

    def setupUi(self):
        self.file_path_label = self.addWidgetToLayout(
            "QLabel", text="click the button to select file")

        # setup a field to show the table
        self.table_name_label = self.addWidgetToLayout(
            "QLabel", text="Table: -")
        
        self.table_field = self.addWidgetToLayout("QTableWidget")

        self.hint_label = self.addWidgetToLayout(
            "QLabel", text="Use Ctrl + Mouse Wheel to zoom in/out")

        # self.save_as_button = self.addWidgetToLayout(
        #     "QPushButton", text="Save As", clickedConn=self.save_as)
    def setupMenubar(self):
        self.addBasicMenus(False,False)
        menubar = self.getCurrentMenubar()
        file_menu = menubar.addMenu("File")

        self.select_file_action = QAction("Select File", self)
        file_menu.addAction(self.select_file_action)
        self.select_file_action.triggered.connect(self.select_file)
        

        self.switch_table_action = QAction("Switch Table", self)
        file_menu.addAction(self.switch_table_action)
        self.switch_table_action.triggered.connect(self.switch_table)
        self.switch_table_action.setDisabled(True)
        
        self.save_change_action = QAction("Save (Ctrl+S)", self)
        file_menu.addAction(self.save_change_action)
        self.save_change_action.triggered.connect(self.save_change)
        self.save_change_action.setDisabled(True)
        self.save_change_action.setShortcut("Ctrl+S")

        # add discard action
        self.discard_change_action = QAction("Discard (Ctrl+D)", self)
        file_menu.addAction(self.discard_change_action)
        self.discard_change_action.triggered.connect(self.confirm_save)
        self.discard_change_action.setDisabled(True)
        self.discard_change_action.setShortcut("Ctrl+D")
        function_menu = menubar.addMenu("Function")
        
        self.translate_table_action = QAction("Translate Table", self)
        function_menu.addAction(self.translate_table_action)
        self.translate_table_action.triggered.connect(self.translate_table)
        self.translate_table_action.setDisabled(True)

    def disable_signal(func):
        '''
        use when the table is being updated by the program, 
        so only when user changes the table, the signal will be emitted
        '''
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]  # Assuming the first argument is self
            self.table_field.itemChanged.disconnect(self.mark_as_changed)
            result = func(*args, **kwargs)
            self.table_field.itemChanged.connect(self.mark_as_changed)
            return result
        return wrapper
    
    @disable_signal
    def update_table_field_for_user(self, df: pd.DataFrame) -> None:
        '''
        update the table with the given dataframe

        TODO: it is better to only update the diff (later work)
        '''
        self.table_field.setRowCount(df.shape[0])
        self.table_field.setColumnCount(df.shape[1])
        self.table_field.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                # if the cell is empty, it will be NaN, so we need to convert it to empty string
                if pd.isna(df.iloc[i, j]):
                    self.table_field.setItem(i, j, QTableWidgetItem(""))
                else:
                    self.table_field.setItem(
                        i, j, QTableWidgetItem(str(df.iloc[i, j])))

    def update_table_field(self, df: pd.DataFrame) -> None:
        '''
        update the table with the given dataframe

        TODO: it is better to only update the diff (later work)
        '''
        self.table_field.setRowCount(df.shape[0])
        self.table_field.setColumnCount(df.shape[1])
        self.table_field.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                # if the cell is empty, it will be NaN, so we need to convert it to empty string
                if pd.isna(df.iloc[i, j]):
                    self.table_field.setItem(i, j, QTableWidgetItem(""))
                else:
                    self.table_field.setItem(
                        i, j, QTableWidgetItem(str(df.iloc[i, j])))
                    
    @Slot()
    def select_file(self) -> None:
        # first need to confirm if save the change before select a new file
        if self.confirm_save()==2: # if user pressed cancel
            return
        

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Excel Files (*.xlsx *.xls)")
        # file_dialog.setDirectory(QDir.current())
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                print("Selected files:", selected_files)

                # get all tables from the excel file
                tables: dict[str, pd.DataFrame] = pd.read_excel(
                    file_path, sheet_name=None)

                table_names = list(tables.keys())
                # create a dialog to select the table with a combo box
                
                # if there is only 1 table in the file, then directly use it
                if len(table_names) == 1:
                    chosen_table_name = table_names[0]
                else:
                    chosen_table_name = self.open_choose_table_dialog(table_names)
                if not chosen_table_name:  # user closed the dialog or pressed cancel, aka open_choose_table_dialog returned None
                    print("No table selected")
                    return
                else:
                    # display the file path
                    self.file_path_label.setText(file_path)
                    # save the chosen table AND the table name
                    self.chosen_table_name: str = chosen_table_name
                    # save all tables
                    self.tables: dict[str, pd.DataFrame] = tables
                    # update the table name label
                    self.table_name_label.setText(
                        f"Table: {chosen_table_name}")

                    # # ★ disconnect the signal to avoid the signal being emitted when updating the table
                    # self.table_field.itemChanged.disconnect(self.mark_as_changed)

                    # show the selected table
                    self.update_table_field_for_user(tables[chosen_table_name])

                    # # ★ connect the signal back
                    # self.table_field.itemChanged.connect(self.mark_as_changed)


                    # enable the switch table and save menu
                    if len(table_names) > 1:
                        self.switch_table_action.setEnabled(True)
                    self.save_change_action.setEnabled(True)
                    self.discard_change_action.setEnabled(True)
                    self.translate_table_action.setEnabled(True)
                    
            else:
                self.file_path_label.setText("file unselected")
                print("No file selected")

    def open_choose_table_dialog(self, table_names: list,default_table_name:str|None=None) -> str | None:
        # send last settings of dim and amount of dices to the dialog
        dialog = ChooseTable(table_names,default_table_name)
        # if the dialog is accepted, get the time from the dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            got_chosen_table = dialog.get_chosen_table()
            print("got_chosen_table:", got_chosen_table)
            return got_chosen_table
        
    def open_choose_column_dialog(self, column_names: list) -> list | None:
        dialog = ChooseColumn(column_names)
        # if the dialog is accepted, get the time from the dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            got_chosen_columns = dialog.get_chosen_columns()
            print("got_chosen_columns:", got_chosen_columns)
            return got_chosen_columns
    

    @Slot()
    def save_change(self):
        '''
        save the change to the current path of the original file
        '''
        # get data from current table
        df = self.get_current_table()
        # save the whole dataframe
        self.tables[self.chosen_table_name] = df
        print("saved the change to the table:", self.chosen_table_name)
        # save changes to the original file, aka overwrite the original file
        try:
            with pd.ExcelWriter(self.file_path_label.text()) as writer:
                for table_name, df in self.tables.items():
                    df.to_excel(writer, sheet_name=table_name, index=False)
        except PermissionError as e:
            print("PermissionError:", e)
            QMessageBox.critical(self, "Permission Error", "Permission Error: Please close the file before saving the change")
            return
        print("saved the tables to the file:", self.file_path_label.text())

        # resetting after saving:

        # remove the * in the window title
        self.setWindowTitle(self.WINDOW_TITLE)
        # reset the table changed flag
        self.table_changed = False

    def get_current_table(self) -> pd.DataFrame:
        data = []
        for row in range(self.table_field.rowCount()):
            data.append([])
            for col in range(self.table_field.columnCount()):
                data[row].append(self.table_field.item(row, col).text())
        df = pd.DataFrame(
            data, columns=self.tables[self.chosen_table_name].columns)
        return df

    @Slot()
    def switch_table(self):
        '''
        switch to another table
        '''
        if self.confirm_save()==2: # if user pressed cancel
            return
        # open choose table dialog
        chosen_table_name = self.open_choose_table_dialog(
            list(self.tables.keys()), self.chosen_table_name)
        if not chosen_table_name:
            print("No table selected")
            return
        self.chosen_table_name = chosen_table_name
        # update the table name label
        self.table_name_label.setText(f"Table: {chosen_table_name}")
        self.update_table_field_for_user(self.tables[chosen_table_name])
    
    @Slot()
    def translate_table(self):
        '''
        translate the table using google translator
        '''
        # get the current table
        if self.confirm_save()==2: # if user pressed cancel
            return
        df = self.get_current_table()
        # open a dialog to choose the columns to translate
        chosen_columns = self.open_choose_column_dialog(df.columns.tolist())
        if not chosen_columns:
            print("No column selected")
            return
        self.progress_dialog = ShowProgressbar()
        self.progress_dialog.show()
        

        self.progress_dialog.translation_thread = TranslationThread(df, chosen_columns)
        self.progress_dialog.translation_thread.progress_updated.connect(self.progress_dialog.update_progress)
        self.progress_dialog.translation_thread.current_translate_text.connect(self.progress_dialog.update_current_translate_label)
        
        # connect the cancel button to stop the translation
        self.progress_dialog.cancel_button.clicked.connect(self.progress_dialog.translation_thread.stop)
        # connect the canceled signal to close the dialog
        self.progress_dialog.translation_thread.canceled.connect(self.progress_dialog.close)
        
        # also reset the data when the translation is canceled
        self.progress_dialog.translation_thread.canceled.connect(lambda: self.update_table_field(self.tables[self.chosen_table_name]))

        self.progress_dialog.translation_thread.finished.connect(self.progress_dialog.close)
        self.progress_dialog.translation_thread.finished.connect(lambda: self.update_table_field(self.progress_dialog.translation_thread.df))
        self.progress_dialog.translation_thread.start()



        # # update the table field
        # self.update_table_field(df)

    def mark_as_changed(self):
        # print("table change detected")
        self.setWindowTitle(self.WINDOW_TITLE + " *")
        self.table_changed = True

    def eventFilter(self, obj, event):
        '''
        使用了 eventFilter 方法来捕获表格视口的滚轮事件。在这个事件过滤器中，检查了Ctrl键的状态，如果Ctrl键被按下，则进行缩放操作，并返回 True 来拦截事件，以阻止其传递给表格。这样，即使鼠标位于表格内部，Ctrl+滚动也会生效。
        '''
        if obj == self.table_field.viewport():
            if event.type() == QWheelEvent.Wheel:
                modifiers = QApplication.keyboardModifiers()
                if modifiers == Qt.ControlModifier:
                    # Ctrl键被按下
                    delta = event.angleDelta().y() / 120.0  # 获取滚动的角度，正数表示向前滚动，负数表示向后滚动
                    zoom_factor = 1.2

                    for col in range(self.table_field.columnCount()):
                        current_width = self.table_field.columnWidth(col)
                        new_width = int(
                            current_width * zoom_factor) if delta > 0 else int(current_width / zoom_factor)
                        self.table_field.setColumnWidth(col, new_width)

                    for row in range(self.table_field.rowCount()):
                        current_height = self.table_field.rowHeight(row)
                        new_height = int(
                            current_height * zoom_factor) if delta > 0 else int(current_height / zoom_factor)
                        self.table_field.setRowHeight(row, new_height)

                    return True  # 拦截事件，不传递给表格

        return super(AutoExcel, self).eventFilter(obj, event)

    def confirm_save(self)->int:
        '''
        confirm if save the change before close

        return:
        0: user choose to save the change before the next action
        1: user choose to discard the change before the next action
        2: user choose to cancel the next action

        '''
        if not self.table_changed:
            return -1
        # compare original saved data with current data, if changed, show a dialog to ask if save the change before close
        if not self.tables[self.chosen_table_name].equals(self.get_current_table()):
            reply = QMessageBox.question(self, 'Save Change', 'Do you want to save the change before further actions?',
                                         QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
            if reply == QMessageBox.Save:
                self.save_change()
                print("User choose to save the change before the next action")
                # reset the table changed flag
                self.table_changed = False
                # remove the * in the window title
                self.setWindowTitle(self.WINDOW_TITLE)
                return 0
            elif reply == QMessageBox.Discard:
                print("User choose to discard the change before the next action")
                # reset all the data
                self.update_table_field(self.tables[self.chosen_table_name])
                # reset the table changed flag
                self.table_changed = False
                # remove the * in the window title
                self.setWindowTitle(self.WINDOW_TITLE)
                return 1
            else:
                print("User choose to cancel the next action")
                # deal canceling outside this function by detecting the return value == 2
                return 2
            
    def _reset_gui(self):
        '''
        reset the table display (gui)
        '''
        # empty the file path label
        self.file_path_label.setText("")
        # empty the table name label
        self.table_name_label.setText("Table: -")
        # empty the table field
        self.table_field.setRowCount(0)
        self.table_field.setColumnCount(0)
        # reset the table changed flag
        self.table_changed = False
        # reset the chosen table name
        self.chosen_table_name = ""
        # reset the tables
        self.tables = {}
        # reset the window title
        self.setWindowTitle(self.WINDOW_TITLE)
        # disable the switch table and save menu
        self.switch_table_action.setDisabled(True)
        self.save_change_action.setDisabled(True)
        self.discard_change_action.setDisabled(True)
    # def keyPressEvent(self, event):
    #     # press Ctrl + S to save the file
    #     if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
    #         self.save_change()
    #     else:
    #         super().keyPressEvent(event)

    def closeEvent(self, event) -> None:
        r=self.confirm_save()
        if r==2:
            event.ignore()
        else:
            event.accept()
            super().closeEvent(event)