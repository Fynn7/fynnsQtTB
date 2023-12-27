from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog,QComboBox,QMessageBox,QWidget
from PyQt6.QtCore import pyqtSignal
from Components.Tools.mlToolBox.fynns_tool_model_v2_0 import *
from PyQt6.QtGui import QAction

class MlToolBox(QMainWindow):
    WINDOW_TITLE = "机器学习工具包"
    WINDOW_SIZE = (800, 600)
    isClosed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.create_menu_bar()

        layout = QVBoxLayout()

        self.label = QLabel("机器学习工具包")
        layout.addWidget(self.label)

        self.select_file_button = QPushButton("选择文件")
        self.select_file_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_button)

        # Placeholder for a dropdown to select ML algorithm
        self.algorithm_label = QLabel("选择机器学习算法:")
        self.algorithm_combobox = QComboBox()
        self.algorithm_combobox.addItems(["Linear Regression", "Decision Tree", "Neural Network"])
        layout.addWidget(self.algorithm_label)
        layout.addWidget(self.algorithm_combobox)

        # Placeholder for a button to run the ML algorithm
        self.run_ml_button = QPushButton("运行机器学习算法")
        self.run_ml_button.clicked.connect(self.run_ml_algorithm)
        layout.addWidget(self.run_ml_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setFixedSize(*self.WINDOW_SIZE)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # Create Style menu
        style_menu = menubar.addMenu("样式")

        # Add Line Plot action
        line_plot_action = QAction("折线图", self)
        line_plot_action.triggered.connect(self.plot_line_graph)
        style_menu.addAction(line_plot_action)

        # Add Scatter Plot action
        scatter_plot_action = QAction("散点图", self)
        scatter_plot_action.triggered.connect(self.plot_scatter_graph)
        style_menu.addAction(scatter_plot_action)

    def select_file(self):
        options = QFileDialog.Option.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", "", "All Files (*)", options=options)

        if file_path:
            self.label.setText(f"已选择文件: {file_path}")
        else:
            self.label.setText("未选择文件")

    def run_ml_algorithm(self):
        # Placeholder for running the selected ML algorithm
        selected_algorithm = self.algorithm_combobox.currentText()
        QMessageBox.information(self, "提示", f"正在运行 {selected_algorithm} 算法")

        # Placeholder for plotting a sample function graph
        self.plot_line_graph()  # Default to line plot

    def plot_line_graph(self):
        # Placeholder for plotting a sample line graph
        x = np.linspace(-5, 5, 100)
        y = x**2
        plt.plot(x, y)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Sample Line Graph')
        plt.show()

    def plot_scatter_graph(self):
        # Placeholder for plotting a sample scatter graph
        x = np.random.rand(50)
        y = np.random.rand(50)
        plt.scatter(x, y)
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Sample Scatter Plot')
        plt.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', "确定退出吗?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print("\"MlToolBox\" closed.")
            event.accept()
        else:
            event.ignore()