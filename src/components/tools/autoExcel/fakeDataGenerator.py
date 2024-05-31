import csv
from faker import Faker
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
)
from ...templates.fynnsSettingsDialog import FynnsSettingsDialog
from ...templates.fynnsComponents import _save_file
from ...templates.fynnsProgressbar import FynnsProgressbar
import time


class FakeDataGenerator(FynnsSettingsDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fake Data Generator")
        self.faker = Faker()
        self.setup_ui()

        # self.progressbar = FynnsProgressbar()

    def setup_ui(self):
        self.layout.addWidget(QLabel("Amount of data to generate:"))

        self.sample_amount_combobox = QComboBox()
        self.sample_amount_combobox.addItems(
            ["10", "20", "50", "100", "1000", "10_000", "100_000"])
        self.sample_amount_combobox.setCurrentIndex(3)
        self.layout.addWidget(self.sample_amount_combobox)

        self.layout.addWidget(QLabel("Amount of columns to generate:"))
        self.column_amount_combobox = QComboBox()
        self.column_amount_combobox.addItems(
            ["1", "5", "10", "20", "50", "100", "1000", "10_000", "100_000"])
        self.column_amount_combobox.setCurrentIndex(2)
        self.layout.addWidget(self.column_amount_combobox)

        select_path_label = QLabel(
            "Select the directory to save the fake data\n")
        self.layout.addWidget(select_path_label)

        self.add_result_buttonBox()

    def generate_fake_data(self) -> None:
        save_path = _save_file("CSV Files (*.csv);;Text Files (*.txt);;Word Files (*.docx);;All Files (*)")
        if not save_path:  # if the user cancels the file dialog
            return

        sample_amount = int(self.sample_amount_combobox.currentText())
        column_amount = int(self.column_amount_combobox.currentText())

        # Add more column names here
        data = [[f"column {i}" for i in range(1, column_amount+1)]]

        with open(save_path, 'w', newline='') as file:
            # generate fake data INSIDE WITH STATEMENT: in case the path raises an permission error
            start_time = time.time()
            progress = 0
            for _ in range(sample_amount):
                sample = [self.faker.word() for _ in range(column_amount)]
                data.append(sample)
                progress += 1
                if progress % 10 == 0:
                    elapsed_time = time.time() - start_time
                    try:
                        generate_velocity = progress / elapsed_time
                        remaining_time = (sample_amount - progress) / generate_velocity
                        print(f"Generating data: {round((progress / sample_amount) * 100, 2)} %  ", time.strftime('%H:%M:%S', time.gmtime(remaining_time)))
                    except ZeroDivisionError:
                        pass
            if save_path.endswith('.csv'):
                print("Writing to csv file...")
                writer = csv.writer(file)
                writer.writerows(data)
                print("Data successfully written to", save_path)
            else:
                # unpack the data as a normal text file
                print("Writing to text file...")
                for row in data:
                    file.write(", ".join(row) + "\n")
                print("Data successfully written to", save_path)

        print("Fake data fully generated and saved to", save_path)
