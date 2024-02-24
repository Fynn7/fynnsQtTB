from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel,QSpinBox, QComboBox, QDialogButtonBox


class DiceSettings(QDialog):
    def __init__(self, last_dim_of_dice:int, last_amount_of_dice:int):
        super().__init__()

        self.last_dim_of_dice=last_dim_of_dice
        self.last_amount_of_dice=last_amount_of_dice
        print("got last settings: last dim of dice:",last_dim_of_dice,"last amount of dice:",last_amount_of_dice)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Game Settings")
        layout = QVBoxLayout(self)

        amount_of_dice_label = QLabel("Set the amount of dices:")
        self.set_dice_amount_spinBox=QSpinBox()
        # set default value
        self.set_dice_amount_spinBox.setValue(self.last_amount_of_dice)
        self.set_dice_amount_spinBox.setRange(1,10)

        dim_of_dice_label = QLabel("Set the dimension of dices:")
        self.set_dice_dim_comboBox=QComboBox()
        # set default value
        self.set_dice_dim_comboBox.addItems(['4','6','8','10','12','20'])
        self.set_dice_dim_comboBox.setCurrentText(str(self.last_dim_of_dice))

        result_buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        result_buttonBox.accepted.connect(self.accept)
        result_buttonBox.rejected.connect(self.reject)


        layout.addWidget(amount_of_dice_label)
        layout.addWidget(self.set_dice_amount_spinBox)

        layout.addWidget(dim_of_dice_label)
        layout.addWidget(self.set_dice_dim_comboBox)

        layout.addWidget(result_buttonBox)

    def get_dice_amount(self) -> int:
        return self.set_dice_amount_spinBox.value()

    def get_dice_dim(self) -> int:
        return int(self.set_dice_dim_comboBox.currentText())