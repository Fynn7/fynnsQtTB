from PyQt6 import QtCore, QtGui, QtWidgets

from components.pomodoroTimer import PomodoroTimer


class Ui_ToolBox(object):
    def setupUi(self, ToolBox:QtWidgets.QMainWindow)->None:
        ToolBox.setObjectName("ToolBox")
        ToolBox.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=ToolBox)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget_lastUsedTools = QtWidgets.QListWidget(
            parent=self.centralwidget)
        self.listWidget_lastUsedTools.setObjectName("listWidget_lastUsedTools")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_lastUsedTools.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_lastUsedTools.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_lastUsedTools.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_lastUsedTools.addItem(item)
        self.gridLayout.addWidget(self.listWidget_lastUsedTools, 0, 0, 1, 1)
        ToolBox.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=ToolBox)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menu_files = QtWidgets.QMenu(parent=self.menubar)
        self.menu_files.setObjectName("menu_files")
        self.menu_edit = QtWidgets.QMenu(parent=self.menubar)
        self.menu_edit.setObjectName("menu_edit")
        self.menu_Alt_S = QtWidgets.QMenu(parent=self.menubar)
        self.menu_Alt_S.setObjectName("menu_Alt_S")
        self.menu_Alt_H = QtWidgets.QMenu(parent=self.menubar)
        self.menu_Alt_H.setObjectName("menu_Alt_H")
        self.menu_toolMenus = QtWidgets.QMenu(parent=self.menubar)
        self.menu_toolMenus.setObjectName("menu_toolMenus")
        self.menu_games = QtWidgets.QMenu(parent=self.menubar)
        self.menu_games.setObjectName("menu_games")
        ToolBox.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=ToolBox)
        self.statusbar.setObjectName("statusbar")
        ToolBox.setStatusBar(self.statusbar)
        self.action_language = QtGui.QAction(parent=ToolBox)
        self.action_language.setObjectName("action_language")
        self.action_pomodoroTimer = QtGui.QAction(parent=ToolBox)
        self.action_pomodoroTimer.setObjectName("action_pomodoroTimer")
        self.action_pdfTranslator = QtGui.QAction(parent=ToolBox)
        self.action_pdfTranslator.setObjectName("action_pdfTranslator")
        self.action_mlToolBox = QtGui.QAction(parent=ToolBox)
        self.action_mlToolBox.setObjectName("action_mlToolBox")
        self.action_font = QtGui.QAction(parent=ToolBox)
        self.action_font.setObjectName("action_font")
        self.menu_Alt_S.addAction(self.action_language)
        self.menu_Alt_S.addAction(self.action_font)
        self.menu_toolMenus.addAction(self.action_pomodoroTimer)
        self.menu_toolMenus.addAction(self.action_pdfTranslator)
        self.menu_toolMenus.addAction(self.action_mlToolBox)
        self.menubar.addAction(self.menu_files.menuAction())
        self.menubar.addAction(self.menu_edit.menuAction())
        self.menubar.addAction(self.menu_toolMenus.menuAction())
        self.menubar.addAction(self.menu_Alt_S.menuAction())
        self.menubar.addAction(self.menu_games.menuAction())
        self.menubar.addAction(self.menu_Alt_H.menuAction())

        # 连接番茄时钟的信号与槽
        self.action_pomodoroTimer.triggered.connect(
            lambda: self.show_widget("PomodoroTimer"))

        self.retranslateUi(ToolBox)
        QtCore.QMetaObject.connectSlotsByName(ToolBox)

        # Custom code
        self.widgets = {
            "PdfTranslator": None,
            "PomodoroTimer": None,
            "MlToolBox": None,
        }
    def warn(self, msg:str)->None:
        '''
        Directly call a default standard warning message box.
        '''
        QtWidgets.QMessageBox.warning(
            self.centralwidget,
            "警告",
            msg,
            QtWidgets.QMessageBox.StandardButton.Ok
        )
    def retranslateUi(self, ToolBox:QtWidgets.QMainWindow)->None:
        _translate = QtCore.QCoreApplication.translate
        ToolBox.setWindowTitle(_translate("ToolBox", "工具盒"))
        __sortingEnabled = self.listWidget_lastUsedTools.isSortingEnabled()
        self.listWidget_lastUsedTools.setSortingEnabled(False)
        item = self.listWidget_lastUsedTools.item(0)
        item.setText(_translate("ToolBox", "历史使用工具："))
        item = self.listWidget_lastUsedTools.item(1)
        item.setText(_translate("ToolBox", "tool1"))
        item = self.listWidget_lastUsedTools.item(2)
        item.setText(_translate("ToolBox", "tool2"))
        item = self.listWidget_lastUsedTools.item(3)
        item.setText(_translate("ToolBox", "tool3"))
        self.listWidget_lastUsedTools.setSortingEnabled(__sortingEnabled)
        self.menu_files.setTitle(_translate("ToolBox", "文件(Alt+F)"))
        self.menu_edit.setTitle(_translate("ToolBox", "编辑(Alt+E)"))
        self.menu_Alt_S.setTitle(_translate("ToolBox", "设置(Alt+S)"))
        self.menu_Alt_H.setTitle(_translate("ToolBox", "帮助(Alt+H)"))
        self.menu_toolMenus.setTitle(_translate("ToolBox", "菜单(Alt+M)"))
        self.menu_games.setTitle(_translate("ToolBox", "游戏(Alt+G)"))
        self.action_language.setText(_translate("ToolBox", "语言"))
        self.action_pomodoroTimer.setText(_translate("ToolBox", "番茄时间"))
        self.action_pdfTranslator.setText(_translate("ToolBox", "PDF翻译"))
        self.action_mlToolBox.setText(_translate("ToolBox", "机器学习工具集"))
        self.action_font.setText(_translate("ToolBox", "字体"))

    def create_and_save_widget(self, widget_name:str)->QtWidgets.QMainWindow:
        try:
            widget:QtWidgets.QMainWindow=eval(f"{widget_name}()")
            # save widget object, otherwise it will be deleted directly after opening this widget window
            self.widgets[widget_name] = widget
            return widget
        except Exception as e:
            self.warn(e)
            raise Exception(e)
        
    def reset_widget(self, widget_name:str)->None:
        self.widgets[widget_name] = None

    def add_resent_used(self, widget_name:str)->None:
        # append widget name into resent used list
        print("Widget", widget_name, "added into resent used list.")

    def show_widget(self, widget_name:str)->None:
        # 如果已经存在 widget 对象，则显示警告
        if self.widgets[widget_name]:
            self.warn(f"{widget_name} 已经打开")
        else:
            # 创建新的 widget 对象并显示
            widget = self.create_and_save_widget(widget_name)
            widget.show()
            print(widget_name, "opened")
            # append widget name into resent used list
            self.add_resent_used(widget_name)
            widget.isClosed.connect(lambda: self.reset_widget(widget_name))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    ToolBox = QtWidgets.QMainWindow()
    ui = Ui_ToolBox()
    ui.setupUi(ToolBox)
    ToolBox.show()
    app.exec()
