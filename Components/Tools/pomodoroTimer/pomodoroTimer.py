from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QLCDNumber, QMenuBar, QMenu, QMessageBox, QWidget,QDialog,QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, QTime, pyqtSignal,QPropertyAnimation
from PyQt6.QtGui import QAction,QColor
from Components.Tools.pomodoroTimer.setTime import SetTimeDialog

class PomodoroTimer(QMainWindow):
    WINDOW_TITLE = "番茄时钟"
    WINDOW_SIZE = (400, 200)
    isClosed = pyqtSignal(bool)
    # time=pyqtSignal(tuple[int,int,int]) # got from "setTime" dialog
    costumTime = (0,25,0) # user input
    def __init__(self)->None:
        super().__init__()
        self.setup_ui()

    def setup_ui(self)->None:
        # 初始化计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        # 初始化变量
        self.time_left = QTime(0,25,0)
        self.is_running = False

        # 创建布局
        layout = QVBoxLayout()

        # 显示计时器的标签
        self.timer_display = QLCDNumber()
        self.timer_display.setDigitCount(8)  # to show hour:minute:second, otherwise without this line it will show only minute:second
        self.timer_display.display(self.time_left.toString("hh:mm:ss"))
        layout.addWidget(self.timer_display)

        # 创建按钮
        self.start_pause_button = QPushButton("启动")
        self.start_pause_button.clicked.connect(self.start_pause_timer)
        layout.addWidget(self.start_pause_button)

        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self.reset_timer)
        layout.addWidget(self.reset_button)

        # 设置布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setFixedSize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
        self.setWindowTitle(self.WINDOW_TITLE)
        self.create_menu()

    def create_menu(self)->None:
        menubar = self.menuBar()

        # 创建 File 菜单
        file_menu = menubar.addMenu("文件")

        # 添加退出动作
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 创建 Help 菜单
        help_menu = menubar.addMenu("帮助")

        # 添加关于动作
        about_action = QAction("关于", self)
        about_action.triggered.connect(lambda:QMessageBox.about(self, "About Pomodoro Timer", "Pomodoro Timer\n\nA simple timer application for the Pomodoro Technique."))
        help_menu.addAction(about_action)


        config_menu = menubar.addMenu("设置")

        setTime_action = QAction("时长", self)
        setTime_action.triggered.connect(lambda:self.setTime())
        config_menu.addAction(setTime_action)


    def setTime(self)->None:
        dialog = SetTimeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            time = dialog.get_time()
            # check if the time is valid (>0)
            print("Got time:",time)
            if time==(0,0,0):
                QMessageBox.warning(self, "设置时间失败", "时间不能为0")
                return
            else: # time is valid, set the time
                self.costumTime = time # save it into attribute to use in reset_timer()
                self.time_left = QTime(time[0],time[1],time[2])
                self.timer_display.display(self.time_left.toString("hh:mm:ss"))

    def update_timer(self)->None:
        if self.time_left > QTime(0, 0, 0):
            self.time_left = self.time_left.addSecs(-1)
            self.timer_display.display(self.time_left.toString("hh:mm:ss"))
        else:
            # 计时结束，停止计时器
            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("↓↓↓")
            self.start_pause_button.setDisabled(True)
            self.reset_button.setText("重新启动")
            self.timer_display.setStyleSheet("color: red")

    def start_pause_timer(self)->None:
        if not self.is_running:
            # 如果计时器未运行，启动计时器
            self.timer.start(1000)  # 以1秒为单位更新
            self.is_running = True
            self.start_pause_button.setText("暂停")
        else:
            # 如果计时器正在运行，暂停计时器
            self.timer.stop()
            self.is_running = False
            self.start_pause_button.setText("继续")

    def reset_timer(self)->None:
        # 重置计时器为初始状态
        self.timer_display.setStyleSheet("color: black")
        self.start_pause_button.setEnabled(True)
        self.timer.stop()
        self.is_running = False
        h,m,s = self.costumTime
        self.time_left = QTime(h,m,s)
        self.timer_display.display(self.time_left.toString("hh:mm:ss"))
        self.start_pause_button.setText("开始")

    def closeEvent(self, event)->None:
        # 重写(overwrite)关闭事件
        reply = QMessageBox.question(self, '提示',
                                     "确定退出吗?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print("PomodoroTimer closed.")
            event.accept()
        else:
            event.ignore()