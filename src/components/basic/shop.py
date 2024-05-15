from PySide6.QtWidgets import (
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QScrollArea,
    QLabel,
    QPushButton,
    QListWidget,
    QLineEdit,
    QComboBox,
    QListWidgetItem,
    QSizePolicy,
    QSpinBox
)

from PySide6.QtCore import (
    Slot, Qt
)

from PySide6.QtGui import (
    QIcon
)

from baseWindow import BaseWindow


class Shop(BaseWindow):
    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "Shop"
        self.balance: float = self.load_data()["balance"]
        super().__init__()
        self.setupUi()
        self.setupMenubar()

        # shop items
        self.items: list[dict] = []

        self.add_item("Apple", 1)
        self.add_item("Pear", 3)
        self.add_item("Banana", 5)

    def setupUi(self):
        self.layout = QVBoxLayout()

        first_row_layout = QHBoxLayout()
        id_label = QLabel("ID")
        item_name_label = QLabel("Name")
        item_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        price_label = QLabel("Price")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount_label = QLabel("Amount")
        amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        first_row_layout.addWidget(id_label)
        first_row_layout.addWidget(item_name_label)
        first_row_layout.addWidget(price_label)
        first_row_layout.addWidget(amount_label)

        self.layout.addLayout(first_row_layout)

        self.item_list_widget = QListWidget()
        self.layout.addWidget(self.item_list_widget)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def setupMenubar(self):
        menubar = self.menuBar()
        balanceMenu = menubar.addMenu(str(self.balance)+" €")
        balanceMenu.setEnabled(False)

    def add_item(self, name: str, price: float):
        '''
        Add an item to the shop
        '''
        item_id = self.item_list_widget.count()+1
        item_id_label = QLabel(str(item_id))
        item_id_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)
        item_id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        item_name_label = QLabel(name)
        item_name_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)
        item_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        item_price_label = QLabel(str(price))
        item_price_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)
        item_price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        item_amount_spin_box = QSpinBox()
        item_amount_spin_box.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)
        item_amount_spin_box.setRange(0, 99)
        item_amount_spin_box.setValue(1)
        item_amount_spin_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buy_button = QPushButton("Buy")
        buy_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # set item dict data structure
        item = {
            "id": item_id,
            "name": name,
            "price": price
        }
        buy_button.clicked.connect(lambda: self.buyItem(
            item, item_amount_spin_box.value()))

        row_layout = QHBoxLayout()
        row_layout.addWidget(item_id_label)
        row_layout.addWidget(item_name_label)
        row_layout.addWidget(item_price_label)
        row_layout.addWidget(item_amount_spin_box)
        row_layout.addWidget(buy_button)

        container_widget = QWidget()
        container_widget.setLayout(row_layout)

        list_item = QListWidgetItem()
        self.item_list_widget.addItem(list_item)

        # 设置 QListWidgetItem 的大小以适应自定义小部件的大小
        list_item.setSizeHint(container_widget.sizeHint())

        self.item_list_widget.setItemWidget(list_item, container_widget)

        # update data structure
        self.items.append(item)

    @Slot(float)
    def buyItem(self, item: dict, amount: int):
        total_price = item["price"]*amount
        if self.balance < total_price:
            QMessageBox.warning(self, "Not enough balance", "You have only "+str(
                self.balance)+" €. You need "+str(total_price-self.balance)+" € more to buy this item.")
            return
        self.balance -= total_price
        # emit signal to notify the balance change in main.py, and call the update_balance method in main.py
        self.changed_balance.emit(self.balance)

        # add the "amount" attribute to the item dict
        item["amount"] = amount
        self.add_item_to_inventory_signal.emit(item)
        # update GUI
        menubar = self.menuBar()
        menubar.actions()[0].setText(str(self.balance)+" €")
