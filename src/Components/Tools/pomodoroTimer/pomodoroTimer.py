import sys
import ctypes
import traceback

try:
    from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLCDNumber, QMessageBox, QWidget, QDialog
    from PySide6.QtCore import QTimer, QTime, Signal
    from PySide6.QtGui import QAction

    from .setTime import SetTimeDialog
    from baseWindow import BaseWindow

except ImportError as ie:
    ctypes.windll.user32.MessageBoxW(0, str(ie), "Import Error",0x10)
    print(traceback.format_exc())
    sys.exit()

except Exception as e:
    ctypes.windll.user32.MessageBoxW(0, str(e), "Unknown Error", 0x10)
    print(traceback.format_exc())
    sys.exit()

class PomodoroTimer(BaseWindow):
    WINDOW_TITLE = "Pomodoro Timer"
    isClosed = Signal(bool)
    costumTime = (0, 25, 0)  # user input

    def __init__(self) -> None:
        super().__init__()
        self.WINDOW_SIZE = (400, 200)
        self.setupLayout()
        self.setupMenu()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(*self.WINDOW_SIZE)

    def closeEvent(self, event) -> None:
        '''Override the close event to perform custom actions'''
        reply = QMessageBox.question(self, self.WINDOW_TITLE,
                                     "Are you sure to quit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print(self.WINDOW_TITLE, "closed.")  # DEBUGGER
            event.accept()
        else:
            event.ignore()

    def setupLayout(self) -> None:
        # 初始化计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # 初始化变量
        self.time_left = QTime(0, 25, 0)
        self.is_running = False

        # 创建布局
        layout = QVBoxLayout()

        # 显示计时器的标签
        self.timer_display = QLCDNumber()
        # to show hour:minute:second, otherwise without this line it will show only minute:second
        self.timer_display.setDigitCount(8)
        self.timer_display.display(self.time_left.toString("hh:mm:ss"))
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

    def setupMenu(self) -> None:
        self.addBasicMenus(withFile=True, withConfig=False)
        # get current menubar
        menubar = self.menuBar()

        # setting menu
        config_menu = menubar.addMenu("Setting")

        setTime_action = QAction("Time", self)
        setTime_action.triggered.connect(self.setTime)
        config_menu.addAction(setTime_action)

    def setTime(self) -> None:
        dialog = SetTimeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            time = dialog.get_time()
            # check if the time is valid (>0)
            print("Got time:", time)
            if time == (0, 0, 0):
                QMessageBox.warning(self, "Failed to set time", "Time cannot be 0. Please set a valid time.")
                return
            else:  # time is valid, set the time
                self.costumTime = time  # save it into attribute to use in reset_timer()
                self.time_left = QTime(time[0], time[1], time[2])
                self.timer_display.display(self.time_left.toString("hh:mm:ss"))

    def update_timer(self) -> None:
        if self.time_left > QTime(0, 0, 0):
            self.time_left = self.time_left.addSecs(-1)
            self.timer_display.display(self.time_left.toString("hh:mm:ss"))
        else:
            # 计时结束，停止计时器
            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("↓↓↓")
            self.start_pause_button.setDisabled(True)
            self.reset_button.setText("Rerun Timer")
            self.timer_display.setStyleSheet("color: red")

    def start_pause_timer(self) -> None:
        if not self.is_running:
            # 如果计时器未运行，启动计时器
            self.timer.start(1000)  # 以1秒为单位更新
            self.is_running = True
            self.start_pause_button.setText("Pause")
        else:
            # 如果计时器正在运行，暂停计时器
            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("Continue")

    def reset_timer(self) -> None:
        # 重置计时器为初始状态
        self.timer_display.setStyleSheet("color: black")
        self.start_pause_button.setEnabled(True)
        self.timer.stop()
        self.is_running = False
        h, m, s = self.costumTime
        self.time_left = QTime(h, m, s)
        self.timer_display.display(self.time_left.toString("hh:mm:ss"))
        self.start_pause_button.setText("Start")
