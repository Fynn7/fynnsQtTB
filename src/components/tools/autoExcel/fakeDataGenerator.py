import csv
from faker import Faker
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
)
from ...templates.fynnsSettingsDialog import FynnsSettingsDialog
from ...templates.fynnsComponents import _select_dir
from ...templates.fynnsProgressbar import FynnsProgressbar

class FakeDataGenerator(FynnsSettingsDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fake Data Generator")
        self.faker = Faker()
        self.setup_ui()
        
        # self.progressbar = FynnsProgressbar()

    def setup_ui(self):
        amount_label=QLabel("Amount of data to generate:")
        self.layout.addWidget(amount_label)

        self.amount_combobox=QComboBox()
        self.amount_combobox.addItems(["10","20","50","100","1000","10000","100000"])
        self.amount_combobox.setCurrentIndex(5)
        self.layout.addWidget(self.amount_combobox)

        select_path_label=QLabel("Select the directory to save the fake data\n↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ")
        self.layout.addWidget(select_path_label)


        self.add_result_buttonBox()
    
    def generate_fake_data(self)->None:
        save_path=_select_dir()+'/fake_data.csv'
        if not save_path: # if the user cancels the file dialog
            return

        data = [['Name', 'Email', 'Phone', 'Address']]
        amount = int(self.amount_combobox.currentText())

        with open(save_path, 'w', newline='') as file:
            # generate fake data INSIDE WITH STATEMENT: in case the path raises an permission error
            for _ in range(amount):
                name = self.faker.name()
                email = self.faker.email()
                phone = self.faker.phone_number()
                address = self.faker.address()

                data.append([name, email, phone, address])

            writer = csv.writer(file)
            writer.writerows(data)
        print("Fake data generated and saved to", save_path)