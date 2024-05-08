from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QComboBox,
    QPushButton,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QMessageBox
)
from PySide6.QtCore import (
    Slot,Qt
)
from PySide6.QtGui import (
    QAction,
)
import traceback
from baseWindow import BaseWindow

class GPACalculator(BaseWindow):
    '''
    Excel Handling Tool
    '''

    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "GPA Calculator"
        super().__init__()
        self.setupUi()
        self.setupMenubar()
        self.data_changed=False

    def setupUi(self):
        self.layout=QVBoxLayout()

        self.info_label=QLabel("")
        self.layout.addWidget(self.info_label)

        total_credits_layout=QHBoxLayout()
        self.total_credits_label=QLabel("Total Credits Needed")
        self.total_credits_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        total_credits_layout.addWidget(self.total_credits_label)

        self.total_credits_line_edit=QLineEdit()
        self.total_credits_line_edit.setPlaceholderText("Enter total credits")
        self.total_credits_line_edit.textChanged.connect(self.calculate_gpa)
        total_credits_layout.addWidget(self.total_credits_line_edit)

        ignored_credits_layout=QHBoxLayout()
        self.ignored_credits_label=QLabel("Ignored Credits/Unnoted Credits")
        self.ignored_credits_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        ignored_credits_layout.addWidget(self.ignored_credits_label)

        self.ignored_credits_line_edit=QLineEdit()
        self.ignored_credits_line_edit.setPlaceholderText("Enter ignored credits")
        self.ignored_credits_line_edit.textChanged.connect(self.calculate_gpa)
        ignored_credits_layout.addWidget(self.ignored_credits_line_edit)

        target_gpa_layout=QHBoxLayout()
        self.target_gpa_label=QLabel("Target GPA")
        target_gpa_layout.addWidget(self.target_gpa_label)

        self.target_gpa_combo_box=QComboBox()
        self.target_gpa_combo_box.addItems(["1.0","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","2.0","2.1","2.2","2.3","2.4","2.5","2.6","2.7","2.8","2.9","3.0","3.1","3.2","3.3","3.4","3.5","3.6","3.7","3.8","3.9","4.0"])
        self.target_gpa_combo_box.currentTextChanged.connect(self.calculate_gpa)
        target_gpa_layout.addWidget(self.target_gpa_combo_box)

        self.layout.addLayout(total_credits_layout)
        self.layout.addLayout(ignored_credits_layout)
        self.layout.addLayout(target_gpa_layout)

        
        first_row_layout=QHBoxLayout()
        id_label=QLabel("ID")
        exam_name_label=QLabel("Exam Name")
        exam_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        exam_score_label=QLabel("Exam Score")
        exam_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        exam_credit_label=QLabel("Exam Credit")
        exam_credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        first_row_layout.addWidget(id_label)
        first_row_layout.addWidget(exam_name_label)
        first_row_layout.addWidget(exam_score_label)
        first_row_layout.addWidget(exam_credit_label)
        self.layout.addLayout(first_row_layout)

        self.exam_result_list_widget=QListWidget()
        self.layout.addWidget(self.exam_result_list_widget)


        add_exam_result_button=QPushButton("Add Exam Result")
        add_exam_result_button.clicked.connect(self.add_exam_result)
        self.layout.addWidget(add_exam_result_button)

        clear_items_button=QPushButton("Clear Items")
        clear_items_button.clicked.connect(self.clear_items)
        self.layout.addWidget(clear_items_button)

        save_results_button=QPushButton("Save Results")
        save_results_button.clicked.connect(self.save_results)
        self.layout.addWidget(save_results_button)

        self.achieved_credits_label=QLabel("Achieved Credits: 0")
        self.layout.addWidget(self.achieved_credits_label)

        self.gpa_label=QLabel("GPA: 0.0")
        self.layout.addWidget(self.gpa_label)

        self.required_score_label=QLabel("Required score for the remaining score: 0.0")
        self.layout.addWidget(self.required_score_label)




        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)


        self.init_results_to_gui()
        # initial GPA calculation
        self.calculate_gpa()

    def setupMenubar(self):
        pass

    @Slot()
    def add_exam_result(self,exam_name:str="",exam_score:str="1.0",exam_credit:int=0):
        '''
        Add a new exam result row to the list widget
        '''
        exam_id=QLabel(str(self.exam_result_list_widget.count()+1))
        exam_id.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        exam_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        exam_name_line_edit = QLineEdit()
        exam_name_line_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        exam_name_line_edit.setText(exam_name)
        exam_name_line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        exam_name_line_edit.textChanged.connect(lambda: setattr(self,"data_changed",True))

        exam_score_combo_box = QComboBox()
        exam_score_combo_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        exam_score_combo_box.addItems(["1.0","1.3","1.7","2.0","2.3","2.7","3.0","3.3","3.7","4.0"])
        exam_score_combo_box.setCurrentText(exam_score)
        exam_score_combo_box.currentTextChanged.connect(self.calculate_gpa)

        exam_credit_spin_box = QSpinBox()
        exam_credit_spin_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        exam_credit_spin_box.setRange(0,200)
        exam_credit_spin_box.setValue(exam_credit)
        exam_credit_spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        exam_credit_spin_box.valueChanged.connect(self.calculate_gpa)

        row_layout = QHBoxLayout()
        row_layout.addWidget(exam_id)
        row_layout.addWidget(exam_name_line_edit)
        row_layout.addWidget(exam_score_combo_box)
        row_layout.addWidget(exam_credit_spin_box)


        container_widget = QWidget()
        container_widget.setLayout(row_layout)

        list_item = QListWidgetItem()
        self.exam_result_list_widget.addItem(list_item)

        # 设置 QListWidgetItem 的大小以适应自定义小部件的大小
        list_item.setSizeHint(container_widget.sizeHint())

        self.exam_result_list_widget.setItemWidget(list_item, container_widget)

    @Slot()
    def clear_items(self):
        '''
        Clear all items in the list widget
        '''
        self.exam_result_list_widget.clear()
        # clear the GPA
        self.gpa_label.setText("Current GPA: 0.0")
        self.required_score_label.setText("Required score for the remaining score: 0.0")
        self.info_label.setText("")

    @Slot()
    def save_results(self):
        '''
        Save the results to a file
        '''
        setattr(self,"data_changed",False)

        data=[]
        for i in range(self.exam_result_list_widget.count()):
            item=self.exam_result_list_widget.item(i)
            widget=self.exam_result_list_widget.itemWidget(item)
            exam_id=widget.layout().itemAt(0).widget().text()
            exam_name=widget.layout().itemAt(1).widget().text()
            exam_score=widget.layout().itemAt(2).widget().currentText()
            exam_credit=widget.layout().itemAt(3).widget().value()
            data.append({"exam_id":exam_id,"exam_name":exam_name,"exam_score":exam_score,"exam_credit":exam_credit})

        self.update_data_file({
            "gpa_calculator":{
                "target_gpa":self.target_gpa_combo_box.currentText(),
                "ignored_credits":self.ignored_credits_line_edit.text(),
                "total_credits_needed":self.total_credits_line_edit.text(),
                "exam_results":data
            }
            })

    def init_results_to_gui(self):
        '''
        Initialize the exam results to the GUI
        '''
        data:list=self.load_data()["gpa_calculator"]
        self.total_credits_line_edit.setText(data["total_credits_needed"])
        self.ignored_credits_line_edit.setText(data["ignored_credits"])
        self.target_gpa_combo_box.setCurrentText(data["target_gpa"])
        for exam_result in data["exam_results"]:
            self.add_exam_result(exam_result["exam_name"],exam_result["exam_score"],int(exam_result["exam_credit"]))

    def calculate_gpa(self)->None:
        '''
        Calculate the GPA
        As long as the widget changes, the GPA will be updated
        '''
        setattr(self,"data_changed",True)
        self.info_label.setText("")

        current_average_score=0
        achieved_credits=0
        self.gpa_label.setText("Calculating GPA...")
        try:
            for i in range(self.exam_result_list_widget.count()):
                item=self.exam_result_list_widget.item(i)
                widget=self.exam_result_list_widget.itemWidget(item)
                exam_score=float(widget.layout().itemAt(2).widget().currentText())
                exam_credit=int(widget.layout().itemAt(3).widget().value())
                current_average_score+=exam_score*exam_credit
                achieved_credits+=exam_credit
            if achieved_credits>0:
                self.achieved_credits_label.setText(f"Achieved Credits: {achieved_credits}")
                gpa = round(current_average_score/achieved_credits,1)
            else:
                raise Exception("The total credits of the exams should be greater than 0")
            self.gpa_label.setText(f"Current GPA: {gpa}")
        except Exception as e:
            self.gpa_label.setText("ERROR")
            self.info_label.setText(str(e))

        self.required_score_label.setText("Calculating required score...")
        # update to GUI
        try:
            target_gpa=float(self.target_gpa_combo_box.currentText())
            total_credits_needed=int(self.total_credits_line_edit.text())-int(self.ignored_credits_line_edit.text())
            # calculate the average score needed to reach the target GPA
            if total_credits_needed>achieved_credits:
                required_score=(target_gpa*total_credits_needed-current_average_score)/(total_credits_needed-achieved_credits)
            else:
                self.info_label.setText("The total credits should be greater than the total credits of the exams")
                raise Exception("The total credits should be greater than the total credits of the exams")
            if required_score>=1.0:
                self.required_score_label.setText(f"Required score for the remaining score: {round(required_score,1)}")
            else:
                self.required_score_label.setText("Not possible to achieve the target GPA")
        except Exception as e:
            self.required_score_label.setText("ERROR")
            self.info_label.setText(str(e))

    
    def closeEvent(self, event):
        '''
        Overwrite the closeEvent method to save the data before closing the window
        '''
        data=self.load_data()["gpa_calculator"]["exam_results"]
        if len(data)!=self.exam_result_list_widget.count() or self.data_changed:
            answer=QMessageBox.warning(self,"Warning","You have unsaved data. Do you want to save it?",QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No|QMessageBox.StandardButton.Cancel)
            if answer==QMessageBox.StandardButton.Yes:
                self.save_results()
                event.accept()
                super().closeEvent(event)
            elif answer==QMessageBox.StandardButton.No:
                event.accept()
                super().closeEvent(event)
            else:
                event.ignore()
        else:
            event.accept()
            super().closeEvent(event)