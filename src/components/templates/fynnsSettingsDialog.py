from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox, QDialogButtonBox, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt


class FynnsSettingsDialog(QDialog):
    '''
    Minimal Example for settings dialog
    
    ## How to build a settings dialog:
    ```
    class ChildSettingsDialogFromFynnsSettingsDialog(FynnsSettingsDialog):
        def __init__(self,saved_settings:dict=None):
            super().__init__()
            self.setup_ui()
            self.saved_settings=saved_settings # optional: load the saved settings from the main window

        def setup_ui(self):
            self.setWindowTitle("XXX Configurations")
            # self.layout=QVBoxLayout(self) # optional: already inherited from FynnsSettingsDialog, but can also set a new layout like QGridLayout
            settings_checkbox = QCheckBox("Check me")
            settings_checkbox.setChecked(True)
            self.layout.addWidget(settings_checkbox) # self.layout is already inherited from FynnsSettingsDialog
            
            # NOTE: here you must call the add_result_buttonBox() method to add the OK and Cancel buttons
            self.add_result_buttonBox()

        def get_XXX_data(self)->dict:
            \'''transmit the settings data to the main window\'''
            return {
                "checked":settings_checkbox.isChecked()
                }
    ```

    ## How to use the built dialog who inherits from `FynnsSettingsDialog` class:

    in main window there should be a function like this to open the dialog:

    ```
    @Slot()
    def open_settings_dialog(self):
        settings_dialog = ChildSettingsDialogFromFynnsSettingsDialog(saved_settings={
                ...
            }
        ) # your settings dialog class inherited from FynnsSettingsDialog

        # check if the user accepted the dialog
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            got_settings_data= settings_dialog.get_XXX_data()
    '''
    def __init__(self):
        super().__init__()
        self.layout:QVBoxLayout = QVBoxLayout(self)
        self.setWindowTitle("Fynns Settings Dialog Prototype")

    def add_result_buttonBox(self):
        '''
        add the OK and Cancel buttons to the dialog
        '''
        result_buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        result_buttonBox.accepted.connect(self.accept)
        result_buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(result_buttonBox)

    def get_settings_data(self)->dict:
        '''transmit the settings data to the main window'''
        ...