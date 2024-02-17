from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QDialogButtonBox


class SetTimeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("设置时间")
        layout = QVBoxLayout(self)

        label_hour = QLabel("请输入h数:")
        self.spinBox_setHour = QSpinBox()
        self.spinBox_setHour.setRange(0, 99)

        label_min = QLabel("请输入分钟数:")
        self.spinBox_setMin = QSpinBox()
        self.spinBox_setMin.setRange(0, 59)

        label_sec = QLabel("请输入sec数:")
        self.spinBox_setSec = QSpinBox()
        self.spinBox_setSec.setRange(0, 59)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(label_hour)
        layout.addWidget(self.spinBox_setHour)
        layout.addWidget(label_min)
        layout.addWidget(self.spinBox_setMin)
        layout.addWidget(label_sec)
        layout.addWidget(self.spinBox_setSec)

        layout.addWidget(button_box)

    def get_time(self) -> tuple[int, int, int]:
        return self.spinBox_setHour.value(), self.spinBox_setMin.value(), self.spinBox_setSec.value()
