from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QDialogButtonBox,
    QLabel,
)

class FynnsLoginDialog(QDialog):
    '''
    Login dialog prototype

    How to use:

    Connection:
    ```
    def open_login_dialog(self, ARGS=...) -> str | None:
        login_dialog = FynnsLogin()
        # if the dialog is accepted, get login data
        if dialog.exec() == QDialog.DialogCode.Accepted:
            got_login_data:tuple[str,str]=login_dialog.get_login_info()
    ```
    '''
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self)->None:
        self.setWindowTitle("Fynns Login Prototype")
        layout = QVBoxLayout(self)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("background-color: yellow; color: black;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)


        result_buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        result_buttonBox.accepted.connect(self.accept)
        result_buttonBox.rejected.connect(self.reject)

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(result_buttonBox)

        
    def get_login_info(self)->tuple[str,str]:
        return self.username_input.text(), self.password_input.text()