from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QLCDNumber, QMenuBar, QMenu, QMessageBox,QWidget
from PyQt6.QtCore import QTimer, QTime,pyqtSignal
from PyQt6.QtGui import QAction

class PomodoroTimer(QMainWindow):
    isClosed=pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 初始化计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # 初始化变量
        self.time_left = QTime(0, 25, 0)  # 初始时间设为 25 分钟
        self.is_running = False

        # 创建布局
        layout = QVBoxLayout()

        # 显示计时器的标签
        self.timer_display = QLCDNumber()
        self.timer_display.display(self.time_left.toString("mm:ss"))
        layout.addWidget(self.timer_display)

        # 创建按钮
        self.start_pause_button = QPushButton("Start")
        self.start_pause_button.clicked.connect(self.start_pause_timer)
        layout.addWidget(self.start_pause_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        layout.addWidget(self.reset_button)

        # 设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 设置窗口初始大小
        self.setFixedSize(400, 200)

        # 设置窗口标题
        self.setWindowTitle("Pomodoro Timer")

        # 添加菜单栏
        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()

        # 创建 File 菜单
        file_menu = menubar.addMenu("File")

        # 添加退出动作
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 创建 Help 菜单
        help_menu = menubar.addMenu("Help")

        # 添加关于动作
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def update_timer(self):
        if self.time_left > QTime(0, 0):
            self.time_left = self.time_left.addSecs(-1)
            self.timer_display.display(self.time_left.toString("mm:ss"))
        else:
            # 计时结束，停止计时器
            self.timer.stop()
            self.is_running = False

    def start_pause_timer(self):
        if not self.is_running:
            # 如果计时器未运行，启动计时器
            self.timer.start(1000)  # 以1秒为单位更新
            self.is_running = True
            self.start_pause_button.setText("Pause")
        else:
            # 如果计时器正在运行，暂停计时器
            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("Start")

    def reset_timer(self):
        # 重置计时器为初始状态
        self.timer.stop()
        self.is_running = False
        self.time_left = QTime(0, 25, 0)
        self.timer_display.display(self.time_left.toString("mm:ss"))
        self.start_pause_button.setText("Start")

    def show_about_dialog(self):
        # 弹出关于对话框
        about_text = "Pomodoro Timer\n\nA simple timer application for the Pomodoro Technique."
        QMessageBox.about(self, "About Pomodoro Timer", about_text)

    def closeEvent(self,event):
        # 重写(overwrite)关闭事件
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print("PomodoroTimer closed.")
            event.accept()
        else:
            event.ignore()
# if __name__ == "__main__":
#     app = QApplication([])

#     pomodoro_timer = PomodoroTimer()
#     pomodoro_timer.show()

#     app.exec()
