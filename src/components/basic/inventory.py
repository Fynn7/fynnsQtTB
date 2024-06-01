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

    def setupUi(self) -> None:
        self.layout = QVBoxLayout()

        first_row_layout = QHBoxLayout()
        item_name_label = QLabel("Name")
        item_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        price_label = QLabel("Value")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount_label = QLabel("Amount")
        amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        consume_label = QLabel("")
        sell_label = QLabel("")

        first_row_layout.addWidget(item_name_label)
        first_row_layout.addWidget(price_label)
        first_row_layout.addWidget(amount_label)
        first_row_layout.addWidget(consume_label)
        first_row_layout.addWidget(sell_label)

        self.layout.addLayout(first_row_layout)

        self.item_list_widget = QListWidget()
        self.layout.addWidget(self.item_list_widget)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def setupMenubar(self) -> None:
        pass

    def add_item(self, item: dict) -> None:
        '''
        Add an item to the inventory

        item
        ```
        {"id": int, "name": str, "price": float, "amount": int}
        ```
        '''
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

        sell_button = QPushButton("Sell")
        sell_button.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred)
        sell_button.clicked.connect(lambda: self.sell_item(item))

        row_layout = QHBoxLayout()
        row_layout.addWidget(item_name_label)
        row_layout.addWidget(item_price_label)
        row_layout.addWidget(item_amount_label)
        row_layout.addWidget(consume_button)
        row_layout.addWidget(sell_button)
        
        container_widget = QWidget()
        container_widget.setLayout(row_layout)

        list_item = QListWidgetItem()
        self.item_list_widget.addItem(list_item)

        # 设置 QListWidgetItem 的大小以适应自定义小部件的大小
        list_item.setSizeHint(container_widget.sizeHint())

        self.item_list_widget.setItemWidget(list_item, container_widget)

        # Update data structure
        self.items.append(item)

    def remove_item(self, item: dict):
        raise NotImplementedError()
        # find the element id
        ...

        # then remove the whole ListWidgetItem from the ListWidget
        ...

    def update_item_amount(self, item_id: int, amount: int)->None:
        '''
        Change the amount of an item in the inventory
        '''
        # find the element by id
        for i in range(len(self.items)): # must get i for updating the item in the list widget
            if self.items[i]["id"] == item_id:
                # update the amount
                self.items[i]["amount"] = amount
                # update the item in the list widget
                item_widget = self.item_list_widget.item(i)
                item_widget_widget = self.item_list_widget.itemWidget(
                    item_widget)
                item_amount_label = item_widget_widget.children()[3]
                item_amount_label.setText(str(self.items[i]["amount"]))
                return

    def init_inventory(self) -> None:
        inventory = self.load_data()["inventory"]
        for item in inventory:
            self.add_item(item)

    def consume_item(self, item: dict):
        # send a signal to main and change emoji_thread.emoji_obj 's attribute
        self.consume_item_signal.emit(item)

    def sell_item(self, item: dict):
        raise NotImplementedError()