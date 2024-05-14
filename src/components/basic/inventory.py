from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QPushButton
)

from PySide6.QtCore import (
    Slot, Qt
)

from baseWindow import BaseWindow


class Inventory(BaseWindow):
    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "My Inventory"
        super().__init__()
        self.setupUi()
        self.setupMenubar()

        self.items: list[dict] = []
        self.init_inventory()

    def setupUi(self):
        self.layout = QVBoxLayout()

        first_row_layout = QHBoxLayout()
        item_name_label = QLabel("Name")
        item_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        price_label = QLabel("Value")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount_label = QLabel("Amount")
        amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        consume_label = QLabel("Consume")

        first_row_layout.addWidget(item_name_label)
        first_row_layout.addWidget(price_label)
        first_row_layout.addWidget(amount_label)
        first_row_layout.addWidget(consume_label)

        self.layout.addLayout(first_row_layout)

        self.item_list_widget = QListWidget()
        self.layout.addWidget(self.item_list_widget)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def setupMenubar(self):
        pass

    def add_item(self, item: dict):
        '''
        Add an item to the inventory
        '''
        self.items.append(item)

        item_name_label = QLabel(item["name"])
        item_name_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)
        item_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        item_price_label = QLabel(str(item["price"]))
        item_price_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)
        item_price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        item_amount_label = QLabel(str(item["amount"]))
        item_amount_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)
        item_amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        consume_button = QPushButton("Consume")
        consume_button.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)
        consume_button.clicked.connect(lambda: self.consume_item(item))

        row_layout = QHBoxLayout()
        row_layout.addWidget(item_name_label)
        row_layout.addWidget(item_price_label)
        row_layout.addWidget(item_amount_label)
        row_layout.addWidget(consume_button)
        
        container_widget = QWidget()
        container_widget.setLayout(row_layout)

        list_item = QListWidgetItem()
        self.item_list_widget.addItem(list_item)

        # 设置 QListWidgetItem 的大小以适应自定义小部件的大小
        list_item.setSizeHint(container_widget.sizeHint())

        self.item_list_widget.setItemWidget(list_item, container_widget)

    def edit_item(self, index: int, item: dict):
        '''
        Edit an item of the inventory
        '''
        self.items[index] = item
        item_name = self.item_list_widget.itemWidget(
            self.item_list_widget.item(index)).layout().itemAt(0).widget()
        item_name.setText(item["name"])
        item_price = self.item_list_widget.itemWidget(
            self.item_list_widget.item(index)).layout().itemAt(1).widget()
        item_price.setText(str(item["price"]))
        item_amount = self.item_list_widget.itemWidget(
            self.item_list_widget.item(index)).layout().itemAt(2).widget()
        item_amount.setText(str(item["amount"]))

    def init_inventory(self):
        '''
        Initialize the inventory with a list of items
        '''
        inventory = self.load_data()["inventory"]
        for item in inventory:
            self.add_item(item)

    def consume_item(self, item: dict):
        '''
        Consume an item
        '''
        raise NotImplementedError()
            