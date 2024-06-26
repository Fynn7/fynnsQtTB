import sys
import ctypes
import traceback

from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLCDNumber,
    QMessageBox,
    QWidget,
    QDialog,
    QTimeEdit,
)
from PySide6.QtCore import (
    QTimer,
    QTime,
    Slot
)
from PySide6.QtGui import (
    QAction,
)

from .setTime import SetTimeDialog
from baseWindow import BaseWindow


class PomodoroTimer(BaseWindow):
    costumTime = (0, 25, 0)  # user input

    def __init__(self) -> None:
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "Pomodoro Timer"
        super().__init__()
        self.WINDOW_SIZE = (400, 200)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_left = QTime(0, 25, 0)
        self.is_running = False

        # instead of local variable, save the object into class attribute to avoid garbage collection
        self.time_up_msgBox = QMessageBox()
        self.time_up_msgBox.setWindowTitle("Congratulations!")
        self.setup_ui()
        self.setupMenu()
        self.resize(*self.WINDOW_SIZE)

    def setup_ui(self) -> None:

        layout = QVBoxLayout()

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

    @Slot()  # syntax sugar for slot connector function
    def setTime(self) -> None:
        dialog = SetTimeDialog(self)
        # if the dialog is accepted, get the time from the dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # get the time from the dialog
            time = dialog.get_time()
            # check if the time is valid (>0)
            print("Got time:", time)
            if time == (0, 0, 0):
                QMessageBox.warning(self, "Failed to set time",
                                    "Time cannot be 0. Please set a valid time.")
            else:  # time is valid, set the time
                self.costumTime = time  # save it into attribute to use in reset_timer()
                self.time_left = QTime(time[0], time[1], time[2])
                self.timer_display.display(self.time_left.toString("hh:mm:ss"))

    @Slot()  # syntax sugar for slot connector function
    def update_timer(self) -> None:
        if self.time_left > QTime(0, 0, 0):
            self.time_left = self.time_left.addSecs(-1)
            self.timer_display.display(self.time_left.toString("hh:mm:ss"))
        else:
            # Time is up, finish the timer
            # load the data and update the balance
            original_balance: float = self.load_data()["balance"]
            # for each 1 min get 1€
            earned: int = self.costumTime[0]*60 + self.costumTime[1]

            if earned:  # inplicitly, only update balance if the time is more than 1 min
                # emit signal to main.py
                self.changed_balance.emit(original_balance+earned)

                self.time_up_msgBox.setText(
                    "Time is up! You have earned " + str(earned) + "€! Keep it up!")
                self.time_up_msgBox.open()
                # close the information msgBox after 3 seconds automatically
                QTimer.singleShot(3000, self.time_up_msgBox.close)

            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("↓↓↓")
            self.start_pause_button.setDisabled(True)
            self.reset_button.setText("Rerun Timer")
            self.timer_display.setStyleSheet("color: red")

    @Slot()  # syntax sugar for slot connector function
    def start_pause_timer(self) -> None:
        if not self.is_running:
            # 如果计时器未运行，启动计时器
            self.timer.start(1000)  # 1 second interval for each update
            self.is_running = True
            self.start_pause_button.setText("Pause")
        else:
            # 如果计时器正在运行，暂停计时器
            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("Continue")

    @Slot()  # syntax sugar for slot connector function
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
