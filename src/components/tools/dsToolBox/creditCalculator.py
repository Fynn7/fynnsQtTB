from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QSpinBox,
    QComboBox,
    QPushButton
)
from PySide6.QtCore import (
    Slot
)
from PySide6.QtGui import (
    QAction,
)

from baseWindow import BaseWindow

class CreditCalculator(BaseWindow):
    '''
    Excel Handling Tool
    '''

    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "Credit Calculator"
        super().__init__()
        self.setupUi()
        self.setupMenubar()
        self.credit_calculator_window=None

    def setupUi(self):
        self.layout=QVBoxLayout()
        self.total_credits_label=QLabel("Total Credits")
        self.layout.addWidget(self.total_credits_label)
        
        self.total_credits_line_edit=QLineEdit()
        self.total_credits_line_edit.setPlaceholderText("Enter a valid number")
        self.layout.addWidget(self.total_credits_line_edit)

        self.exam_result_scroll_area=QScrollArea()
        self.layout.addWidget(self.exam_result_scroll_area)
    

        # create a layout for the first column for 3 labels
        # column_layout=QVBoxLayout()
        # exam_name_label=QLabel("Exam Name")
        # exam_result_label=QLabel("Score")
        # exam_credit_label=QLabel("Credits")
        # column_layout.addWidget(exam_name_label)
        # column_layout.addWidget(exam_result_label)
        # column_layout.addWidget(exam_credit_label)
        # self.exam_result_scroll_area.setLayout(column_layout)
        # self.layout.addWidget(self.exam_result_scroll_area)

        # self.add_exam_result_button=QPushButton("Add Exam Result", self)
        # self.add_exam_result_button.clicked.connect(self.add_exam_result)
        # self.layout.addWidget(self.add_exam_result_button)
        
    def setupMenubar(self):
        pass

    @Slot()
    def add_exam_result(self):
        '''
        Create a new exam result input field
        '''
        pass
        # column_layout=QVBoxLayout()
        # exam_name_line_edit=QLineEdit()
        # exam_name_line_edit.setPlaceholderText("Enter the exam name")
        # exam_score_combobox=QComboBox()
        # exam_score_combobox.addItems(["1,0", "1,3", "1,7", "2,0", "2,3", "2,7", "3,0", "3,3", "3,7", "4,0", "5,0"])
        # exam_credit_spinbox=QSpinBox()
        # exam_credit_spinbox.setRange(1, 30)

        
        # self.exam_result_scroll_area.setLayout(column_layout)