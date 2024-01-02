from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QWidget, QMessageBox, QLabel,QLineEdit,QScrollArea,QSpinBox,QWidgetAction,QDoubleSpinBox,QCheckBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction
from Components.Tools.mlToolBox.fynns_tool_model_v2_0 import *
import traceback
from baseWindow import BaseWindow


class MlToolBox(BaseWindow):
    WINDOW_TITLE = "机器学习工具包"
    selected_algorithm = "RandomForestRegression" # Default as Random Forest Regression
    selected_plot_style = "sp" # Default as Scatter plot
    isClosed=pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def closeEvent(self, event)->None:
        '''Override the close event to perform custom actions if hasCloseEvent is True.'''
        reply = QMessageBox.question(self, self.WINDOW_TITLE,
                                    "Are you sure to quit?",QMessageBox.StandardButton.Yes |QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply ==QMessageBox.StandardButton.Yes:
            self.isClosed.emit(True)
            print(self.WINDOW_TITLE,"closed.") # DEBUGGER
            event.accept()
        else:
            event.ignore()
        event.accept()

    def setup_ui(self): # 用PyQt6原生编程，因为要保存text input box的内容
        self.create_menu_bar()

        layout = QVBoxLayout()

        self.select_file_button = QPushButton("选择文件")
        self.select_file_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_button)

        # Label for displaying the selected file path
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

    def create_menu_bar(self):
        self.addBasicMenus(withFile=True,withConfig=True)
        menubar = self.menuBar()

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
        line_plot_action.triggered.connect(lambda: self.select_plot_style("lp"))
        style_menu.addAction(line_plot_action)


        # Add Scatter Plot action
        scatter_plot_action = QAction("散点图 (默认)", self)
        scatter_plot_action.triggered.connect(lambda: self.select_plot_style("sp"))
        style_menu.addAction(scatter_plot_action)

        self.parameters_menu= menubar.addMenu("参数")

        # 创建 QSpinBox 用于设置参数 "cv"
        self.cv_spinbox = QSpinBox()

        self.cv_spinbox.setMinimum(0)
        self.cv_spinbox.setValue(2)
        cv_widget_action = QWidgetAction(self)
        cv_widget_action.setDefaultWidget(self.cv_spinbox)
        self.parameters_menu.addAction(cv_widget_action)

        # 创建 QSpinBox 用于设置参数 "random_state"
        
        self.random_state_spinbox = QSpinBox()

        self.random_state_spinbox.setMinimum(0)
        self.random_state_spinbox.setMaximum(100)
        self.random_state_spinbox.setValue(42)
        random_state_widget_action = QWidgetAction(self)
        random_state_widget_action.setDefaultWidget(self.random_state_spinbox)
        self.parameters_menu.addAction(random_state_widget_action)

        # 创建 QDoubleSpinBox 用于设置参数 "test_size"
        self.test_size_spinbox = QDoubleSpinBox()


        self.test_size_spinbox.setMinimum(0.0)
        self.test_size_spinbox.setMaximum(1.0)
        self.test_size_spinbox.setValue(0.25)
        test_size_widget_action = QWidgetAction(self)
        test_size_widget_action.setDefaultWidget(self.test_size_spinbox)
        self.parameters_menu.addAction(test_size_widget_action)

        # 创建 QDoubleSpinBox 用于设置参数 "train_size"
        self.train_size_spinbox = QDoubleSpinBox()


        self.train_size_spinbox.setMinimum(0.0)
        self.train_size_spinbox.setMaximum(1.0)
        self.train_size_spinbox.setValue(0.75)
        train_size_widget_action = QWidgetAction(self)
        train_size_widget_action.setDefaultWidget(self.train_size_spinbox)
        self.parameters_menu.addAction(train_size_widget_action)

        # 创建 QCheckBox 用于设置参数 "plotPred"
        self.plot_pred_checkbox = QCheckBox("Plot Prediction")
        self.plot_pred_checkbox.setChecked(True)
        plot_pred_widget_action = QWidgetAction(self)
        plot_pred_widget_action.setDefaultWidget(self.plot_pred_checkbox)
        self.parameters_menu.addAction(plot_pred_widget_action)

        # 添加分隔符
        self.parameters_menu.addSeparator()

        # 创建 QCheckBox 用于设置参数 "printInfo"
        self.print_info_checkbox = QCheckBox("Print Info")
        self.print_info_checkbox.setChecked(True)
        print_info_widget_action = QWidgetAction(self)
        print_info_widget_action.setDefaultWidget(self.print_info_checkbox)
        self.parameters_menu.addAction(print_info_widget_action)


        # result menu
        self.result_menu = menubar.addMenu("结果展示")

        # 展示关联矩阵
        self.plot_correlation_map_checkbox = QCheckBox("输出关联矩阵")
        self.plot_correlation_map_checkbox.setChecked(True)
        plot_correlation_map_widget_action = QWidgetAction(self)
        plot_correlation_map_widget_action.setDefaultWidget(self.plot_correlation_map_checkbox)
        self.result_menu.addAction(plot_correlation_map_widget_action)


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

    def select_algorithm(self, algorithm:str):
        self.selected_algorithm = algorithm
        self.run_ml_button.setText(f"运行{algorithm}算法")

    def select_plot_style(self, plot_style:str):
        self.selected_plot_style = plot_style
        abbr = {"lp":"折线图", "sp":"散点图"}
        QMessageBox.information(self, "提示", f"已选择 {abbr[plot_style]} 样式")

    def run_ml_algorithm(self)->None: # ycol: user input it in a text input box
        # values from user settings: saved as class attributes
        random_state = self.random_state_spinbox.value()
        test_size = self.test_size_spinbox.value()
        train_size = self.train_size_spinbox.value()
        plot_pred = self.plot_pred_checkbox.isChecked()
        cv=self.cv_spinbox.value()
        print_info=self.print_info_checkbox.isChecked()
        plot_style=self.selected_plot_style

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
            self.info_label.setText(f"y column name not found: \"{ycol}\".\nAll columns are:\n{list(df.columns)}")
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
            try:
                result=fitModel(train_test_split(X,y,train_size=train_size,test_size=test_size,random_state=random_state),modelName=selected_algorithm,printInfo=print_info,plotPred=plot_pred,cv=cv,plotStyle=plot_style,**model_args)
            except Exception:
                self.info_label.setText(f"An Error Occurred:\n{traceback.format_exc()}")
                return
            
        except Exception:
            self.info_label.setText(f"An Error Occurred:\n{traceback.format_exc()}")
            return
        
        # draw confusion matrix
        if self.plot_correlation_map_checkbox.isChecked():
            cleaned_df = X.copy()
            cleaned_df[ycol] = y
            try:
                plot_correlation_map(data=cleaned_df)
            except Exception:
                self.info_label.setText(f"An Error Occurred:\n{traceback.format_exc()}")
                return
            
        # display result
        self.info_label.setText(str(result[:-1])+f"\n\n{result[-1]}")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ml_toolbox = MlToolBox()
    ml_toolbox.show()
    sys.exit(app.exec())
