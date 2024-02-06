from baseWindow import BaseWindow
from PySide6 import QtWidgets,QtGui
import random

from .diceSettings import DiceSettings

class Dice(BaseWindow):
    def __init__(self):
        self.WINDOW_TITLE = "Dice Game" # overwriting the parent class attribute before parent calling its __init__
        super(Dice, self).__init__()
        self.setup_ui()
        self.setup_menubar()

        # override the QVBoxlayout to a Grid layout
        self.updateLayout(QtWidgets.QGridLayout())

        self.dices = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
        self.dim_of_dice=len(self.dices)
        self.amount_of_dice=1
        self.reset_dice_labels()

    def setup_ui(self):
        self.resize(300, 200)

    def setup_menubar(self):
        self.addBasicMenus(withConfig=False)
        menubar= self.getCurrentMenubar()
        game_settings_dialog = QtGui.QAction("Game Settings", self)
        game_settings_dialog.triggered.connect(self.game_settings)
        menubar.addAction(game_settings_dialog)

    def reset_dice_labels(self):
        '''
        used in init and game_settings to reset the labels

        i know it's harsh, i can do it with 2 separate layouts for fixed layout and dice layout instead of 1 whole 
        '''
        
        # remove labels first
        self.clear_layout()

        # TODO: make the game more interesting
        self.addWidgetToLayout("QLabel", text="0€")
        self.addWidgetToLayout("QLabel", text="Your current bet: 0€")
        
        # add new init labels
        # fixed labels
        self.addWidgetToLayout("QLabel", text="Amount of dices: "+str(self.amount_of_dice))
        self.addWidgetToLayout("QLabel", text="Dimension of dices: "+str(self.dim_of_dice))
        
        # dice labels
        amount=self.amount_of_dice
        for i in range(1,amount+1):
            exec(f'self.dice_label_{i}=self.addWidgetToLayout("QLabel", text="⚀")')
            print(f'self.dice_label_{i}','generated')
        
        # roll button
        self.addWidgetToLayout("QPushButton", text="Roll Dice", clickedConn=self.roll_dice)
        
    def roll_dice(self):
        amount=self.amount_of_dice
        # choose a random dice
        rolled_dice = random.choices(self.dices, k=amount)
        
        for i in range(1,amount+1):
            exec(f'self.dice_label_{i}.setText("{rolled_dice[i-1]}")')
            print(f'self.dice_label_{i}','rolled a',rolled_dice[i-1])
    

    def game_settings(self):
        # send last settings of dim and amount of dices to the dialog
        dialog = DiceSettings(self.dim_of_dice, self.amount_of_dice)
        # if the dialog is accepted, get the time from the dialog
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            # get the time from the dialog
            got_amount=dialog.get_dice_amount()
            print("Got amount of dices:", got_amount)
            self.amount_of_dice=got_amount

            got_dim=dialog.get_dice_dim()
            full_dice_list=["⚀", "⚁", "⚂", "⚃", "⚄", "⚅", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
            self.dices=full_dice_list[:got_dim]
            self.dim_of_dice=got_dim
            print("Got dimension of dices:", got_dim)


            self.reset_dice_labels() # set labels according to user settings

    def clear_layout(self):
        layout=self.getLayout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        
            