import csv
from faker import Faker
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
)
from ...templates.fynnsSettingsDialog import FynnsSettingsDialog
from ...templates.fynnsComponents import _save_file
from ...templates.fynnsProgressbar import FynnsProgressbar

class FakeDataGenerator(FynnsSettingsDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fake Data Generator")
        self.faker = Faker()
        self.setup_ui()
        
        # self.progressbar = FynnsProgressbar()

    def setup_ui(self):
        self.layout.addWidget(QLabel("Amount of data to generate:"))

        self.sample_amount_combobox=QComboBox()
        self.sample_amount_combobox.addItems(["10","20","50","100","1000","10_000","100_000"])
        self.sample_amount_combobox.setCurrentIndex(5)
        self.layout.addWidget(self.sample_amount_combobox)

        self.layout.addWidget(QLabel("Amount of columns to generate:"))
        self.column_amount_combobox=QComboBox()
        self.column_amount_combobox.addItems(["1","5","10","20","50","100","1000","10_000","100_000"])
        self.column_amount_combobox.setCurrentIndex(2)
        self.layout.addWidget(self.column_amount_combobox)

        select_path_label=QLabel("Select the directory to save the fake data\n")
        self.layout.addWidget(select_path_label)


        self.add_result_buttonBox()
    
    def generate_fake_data(self)->None:
        save_path=_save_file("CSV Files (*.csv)")
        if not save_path: # if the user cancels the file dialog
            return
        
        sample_amount = int(self.sample_amount_combobox.currentText())
        column_amount = int(self.column_amount_combobox.currentText())
        
        data = [[f"column {i}" for i in range(1,column_amount+1)]]  # Add more column names here

        with open(save_path, 'w', newline='') as file:
            # generate fake data INSIDE WITH STATEMENT: in case the path raises an permission error
            for _ in range(sample_amount):
                sample= [self.faker.word() for _ in range(column_amount)]
                data.append(sample)
            writer = csv.writer(file)
            writer.writerows(data)

        print("Fake data generated and saved to", save_path)