from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QWidget, QMessageBox, QLabel,QLineEdit,QScrollArea
from PyQt6.QtCore import pyqtSignal
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtGui import QAction
from Components.Tools.mlToolBox.fynns_tool_model_v2_0 import *
import traceback
class MlToolBox(QMainWindow):
    WINDOW_TITLE = "机器学习工具包"
    WINDOW_SIZE = (800, 600)
    isClosed = pyqtSignal(bool)
    selected_algorithm = "RandomForestRegression"
    selected_plot_style = "Scatter Plot" # Default as Scatter plot

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.create_menu_bar()

        layout = QVBoxLayout()

        self.select_file_button = QPushButton("选择文件")
        self.select_file_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_button)

        # Placeholder for displaying file path
        self.file_path_label = QLabel()
        layout.addWidget(self.file_path_label)

        # 文本输入框用于用户输入y列的名称
        self.ycol_input = QLineEdit()
        self.ycol_input.setPlaceholderText("输入y列的名称")
        layout.addWidget(self.ycol_input)

        # 文本输入框用于用户输入其他参数
        self.model_args_input = QLineEdit()
        self.model_args_input.setPlaceholderText("（可选）输入其他fitModel参数（以逗号分隔，例如: arg1=value1, arg2=value2）")
        layout.addWidget(self.model_args_input)

        self.run_ml_button = QPushButton(f"运行{self.selected_algorithm}算法")
        self.run_ml_button.clicked.connect(self.run_ml_algorithm)
        layout.addWidget(self.run_ml_button)

        # Placeholder for displaying the selected algorithm and scores
        self.info_label = QLabel("尚无结果")

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.info_label)
        scroll_area.setWidgetResizable(True)  # 使得内容可以调整大小

        layout.addWidget(scroll_area)  # 将 QScrollArea 放入布局

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
        self.linear_regression_action.triggered.connect(lambda: self.select_algorithm("LinearRegression"))
        algorithm_menu.addAction(self.linear_regression_action)

        # Add Decision Tree action
        self.decision_tree_action = QAction("Random Forest Regression", self)
        self.decision_tree_action.triggered.connect(lambda: self.select_algorithm("RandomForestRegression"))
        algorithm_menu.addAction(self.decision_tree_action)

        # Add Neural Network action
        self.neural_network_action = QAction("-", self)
        self.neural_network_action.triggered.connect(lambda: self.select_algorithm("-"))
        algorithm_menu.addAction(self.neural_network_action)

        # Create Style menu
        style_menu = menubar.addMenu("样式")

        # Add Line Plot action
        line_plot_action = QAction("折线图", self)
        line_plot_action.triggered.connect(lambda: self.select_plot_style("Line Plot"))
        style_menu.addAction(line_plot_action)

        # Add Scatter Plot action
        scatter_plot_action = QAction("散点图", self)
        scatter_plot_action.triggered.connect(lambda: self.select_plot_style("Scatter Plot"))
        style_menu.addAction(scatter_plot_action)
    def reset_info_label(self)->None:
        self.info_label.setText("尚无结果")

    def select_file(self)->None:
        options = QFileDialog.Option.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择csv文件", ".csv", "csv文件(*.csv)",options=options)

        if file_path:
            print(f"已选择文件: {file_path}")
            self.file_path_label.setText(f"{file_path}")
            self.reset_info_label()
        else:
            print("未选择文件")

    def run_ml_algorithm(self)->None: # ycol: user input it in a text input box
        selected_algorithm = getattr(self, 'selected_algorithm', None) # NOTE: Default as Linear Regression, already set in global class attribute
        selected_plot_style = getattr(self, 'selected_plot_style', None) # NOTE: Default as Scatter plot, already set in global class attribute
        ycol=self.ycol_input.text()
        # data processing
        try:
            df=pd.DataFrame(pd.read_csv(self.file_path_label.text()))

        except FileNotFoundError:
            self.info_label.setText(f"File not found:{self.file_path_label.text()}")
            return
        except Exception:
            self.info_label.setText(f"An Error Occurred:\n{traceback.format_exc()}")

            return
        try:
            X=df.drop(ycol,axis=1)
            y=df[ycol]        
        except KeyError:
            self.info_label.setText(f"y column name not found: {ycol}. All columns are:\n{list(df.columns)}")

            return
        except Exception:
            self.info_label.setText(f"An Error Occurred:\n{traceback.format_exc()}")
            return

        # model training
        X,y=cleanData(X,y)
        # for other arguments for fitModel(), let user input in a text input box
        try:
            model_args = self.model_args_input.text()
            model_args = model_args.split(",")
            model_args = [arg.split("=") for arg in model_args]
            print(model_args)
            try:
                model_args = {arg[0]:(int(arg[1]) if arg[1].isnumeric() else arg[1]) for arg in model_args} if model_args!=[['']] else {}
            except Exception:
                self.info_label.setText(f"Invalid model_args: {model_args}\nModel Arguments set to empty")
                model_args={}
            result=fitModel(train_test_split(X,y),selected_algorithm,printInfo=True,plotPred=True,cv=2,**model_args)
        except Exception:
            self.info_label.setText(f"An Error Occurred:\n{traceback.format_exc()}")

            return
        
        QMessageBox.information(self, "提示", f"正在运行 {selected_algorithm} 算法")
        self.info_label.setText(str(result))


        # Placeholder for plotting a sample function graph
        self.plot_line_graph()  # Default to line plot

    def select_algorithm(self, algorithm:str):
        self.selected_algorithm = algorithm
        self.run_ml_button.setText(f"运行{algorithm}算法")

    def select_plot_style(self, plot_style:str):
        self.selected_plot_style = plot_style
        QMessageBox.information(self, "提示", f"已选择 {plot_style} 样式")

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
