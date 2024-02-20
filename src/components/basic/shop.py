from PySide6 import QtWidgets, QtCore, QtGui
from baseWindow import BaseWindow

class Shop(BaseWindow):
    def __init__(self):
        # overwriting the parent class attribute before parent calling its __init__
        self.WINDOW_TITLE = "Shop"
        self.balance: float = self.load_data()["balance"]
        super().__init__()
        self.setupUi()
        self.setupMenubar()

    def setupUi(self):
        self.addWidgetToLayout("QLabel", text="Item A: 1 €")
        # TODO: add a "+" and "-" button to increase and decrease the quantity of the item;
        # TODO: add a QLineEdit to show the quantity of the item
        self.addWidgetToLayout("QPushButton", text="Purchase",
                               clickedConn=lambda: self.buyItem(1))

    def setupMenubar(self):
        self.addBasicMenus(withConfig=False)

        menubar = self.getCurrentMenubar()

        # add balance menu (just for display)

        balanceMenu = menubar.addMenu(str(self.balance)+" €")
        balanceMenu.setEnabled(False)

    @QtCore.Slot(float)
    def buyItem(self, price: float):
        if self.balance < price:
            QtWidgets.QMessageBox.warning(self, "Not enough balance", "You have only "+str(
                self.balance)+" €. You need "+str(price-self.balance)+" € more to buy this item.")
            return
        self.balance -= price
        # emit signal to notify the balance change in main.py, and call the update_balance method in main.py
        self.changed_balance.emit(self.balance)
        # update text of balance menu
        self.getCurrentMenubar().actions()[1].setText(str(self.balance)+" €")