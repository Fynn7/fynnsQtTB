from PyQt6.QtWidgets import QApplication, QLCDNumber, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, QTime

class TimeDisplay(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # 初始化变量
        self.time_left = QTime(0, 0, 0)
        self.is_running = False

        # 创建布局
        layout = QVBoxLayout()

        # 创建一个 QLCDNumber 用于显示时、分、秒
        self.lcd_number = QLCDNumber()
        self.lcd_number.setDigitCount(8)  # 设置显示的位数

        layout.addWidget(self.lcd_number)

        # 设置布局
        self.setLayout(layout)

        # 启动计时器
        self.start_timer()

    def start_timer(self):
        self.timer.start(1000)  # 以1秒为单位更新

    def update_timer(self):
        if self.time_left < QTime(23, 59, 59):
            self.time_left = self.time_left.addSecs(1)
        else:
            self.time_left = QTime(0, 0, 0)

        # 直接显示时、分、秒
        self.lcd_number.display(self.time_left.toString("hh:mm:ss"))

if __name__ == "__main__":
    app = QApplication([])
    time_display = TimeDisplay()
    time_display.show()
    app.exec()
