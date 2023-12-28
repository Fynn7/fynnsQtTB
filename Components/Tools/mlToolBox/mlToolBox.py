from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QWidget, QMessageBox, QLabel
from PyQt6.QtCore import pyqtSignal
import matplotlib.pyplot as plt  # For plotting function graphs
import numpy as np
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

        self.select_file_button = QPushButton("选择文件")
        self.select_file_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_button)

        # Placeholder for a button to run the ML algorithm
        self.run_ml_button = QPushButton(f"运行{'Linear Regression'}算法")
        self.run_ml_button.clicked.connect(self.run_ml_algorithm)
        layout.addWidget(self.run_ml_button)

        # Placeholder for displaying the selected algorithm and scores
        self.info_label = QLabel()
        layout.addWidget(self.info_label)

        # Placeholder for displaying file path
        self.file_path_label = QLabel()
        layout.addWidget(self.file_path_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setFixedSize(*self.WINDOW_SIZE)

    def create_menu_bar(self):
        menubar = self.menuBar()

        # Create File menu
        file_menu = menubar.addMenu("文件")

        # Add Exit action
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create Algorithm menu
        algorithm_menu = menubar.addMenu("算法")

        # Add Linear Regression action
        self.linear_regression_action = QAction("Linear Regression", self)
        self.linear_regression_action.triggered.connect(lambda: self.select_algorithm("Linear Regression"))
        algorithm_menu.addAction(self.linear_regression_action)

        # Add Decision Tree action
        self.decision_tree_action = QAction("Decision Tree", self)
        self.decision_tree_action.triggered.connect(lambda: self.select_algorithm("Decision Tree"))
        algorithm_menu.addAction(self.decision_tree_action)

        # Add Neural Network action
        self.neural_network_action = QAction("Neural Network", self)
        self.neural_network_action.triggered.connect(lambda: self.select_algorithm("Neural Network"))
        algorithm_menu.addAction(self.neural_network_action)

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
            print(f"已选择文件: {file_path}")
            self.file_path_label.setText(f"文件路径: {file_path}")
        else:
            print("未选择文件")

    def run_ml_algorithm(self):
        # Placeholder for running the selected ML algorithm
        selected_algorithm = getattr(self, 'selected_algorithm', None)
        selected_scores = getattr(self, 'selected_scores', [])

        if selected_algorithm:
            QMessageBox.information(self, "提示", f"正在运行 {selected_algorithm} 算法，评分方式为 {', '.join(selected_scores)}")
            self.info_label.setText(f"已选择算法: {selected_algorithm}，评分方式: {', '.join(selected_scores)}")
        else:
            QMessageBox.warning(self, "警告", "请先选择算法")

        # Placeholder for plotting a sample function graph
        self.plot_line_graph()  # Default to line plot

    def select_algorithm(self, algorithm):
        self.selected_algorithm = algorithm
        self.run_ml_button.setText(f"运行{algorithm}算法")

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

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ml_toolbox = MlToolBox()
    ml_toolbox.show()
    sys.exit(app.exec())
