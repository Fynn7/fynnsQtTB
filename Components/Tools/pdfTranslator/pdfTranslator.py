from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget, QMessageBox, QInputDialog,QMenu
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction

class Translator:
    @staticmethod
    def translate_pdf(file_path):
        # 在这里添加 Deepl 或其他服务的 PDF 翻译实现
        print(f"Translating PDF file: {file_path}")

class PdfTranslator(QMainWindow):
    WINDOW_TITLE = "PDF OCR识别翻译"
    WINDOW_SIZE = (600, 400)
    TOOLS=["DeepL","Google Translate"]
    LANGUAGES=[]
    isClosed = pyqtSignal(bool)
    translateSource="DeepL"
    selected_file_path = ""
    translated_file_path = ""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.select_path_button = QPushButton("选择PDF文件")
        self.select_path_button.clicked.connect(self.select_pdf_path)
        layout.addWidget(self.select_path_button)

        self.path_label = QLabel("未选择文件")
        layout.addWidget(self.path_label)

        self.translate_button = QPushButton("翻译PDF")
        self.translate_button.clicked.connect(self.translate_pdf)
        layout.addWidget(self.translate_button)

        self.download_button = QPushButton("下载翻译结果")
        self.download_button.clicked.connect(self.download_translated_pdf)
        layout.addWidget(self.download_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setFixedSize(self.WINDOW_SIZE[0], self.WINDOW_SIZE[1])
        self.setWindowTitle(self.WINDOW_TITLE)
        self.create_menu()
    
    def create_menu(self)->None:
        # base menu
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
        change_tool_menu = QMenu("切换翻译源", self)

        # 添加 DeepL 动作
        deepl_action = QAction("DeepL翻译 (默认)", self)
        deepl_action.triggered.connect(lambda: self.set_translation_tool("DeepL")) # directly set a variable
        change_tool_menu.addAction(deepl_action)

        # 添加 Google Translate 动作
        google_translate_action = QAction("谷歌翻译", self)
        google_translate_action.triggered.connect(lambda: self.set_translation_tool("Google Translate"))
        change_tool_menu.addAction(google_translate_action)

        config_menu.addMenu(change_tool_menu)

    def set_translation_tool(self, tool:str):
        if tool in self.TOOLS:
            self.translateSource = tool
            QMessageBox.information(self, "成功", f"已切换到 {self.translateSource}")
            print("Tool switched to:", self.translateSource)
        else:
            QMessageBox.information(self, "失败", f"找不到工具 {self.translateSource}")
            print("Failed to switch tool")
    
    def select_pdf_path(self):
        options = QFileDialog.Option.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择PDF文件", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if file_path:
            self.selected_file_path = file_path
            self.path_label.setText(f"{file_path}")
        else:
            print("用户取消选择文件")

    def translate_pdf(self):
        if self.selected_file_path:
            try:
                # TODO: 调用实际的 PDF 翻译功能
                Translator.translate_pdf(self.selected_file_path)
                self.translated_file_path = "/path/to/translated/file.pdf"  # 替换为实际的翻译文件路径
                QMessageBox.information(self, "成功", "翻译成功！")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"翻译失败：{str(e)}")
        else:
            QMessageBox.warning(self, "警告", "请先选择PDF文件")

    def download_translated_pdf(self):
        if self.translated_file_path:
            # 提示用户输入保存路径
            save_path, _ = QFileDialog.getSaveFileName(self, "保存翻译结果", "", "PDF Files (*.pdf);;All Files (*)")
            if save_path:
                # TODO: 将翻译结果文件复制到用户选择的保存路径
                print(f"Downloading translated PDF to: {save_path}")
                QMessageBox.information(self, "成功", "下载成功！")
        else:
            QMessageBox.warning(self, "警告", "请先翻译PDF文件")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示',
                                     "确定退出吗?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print("\"PdfTranslator\" closed.")
            event.accept()
        else:
            event.ignore()
