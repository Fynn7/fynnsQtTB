from baseWindow import BaseWindow
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtCore import (
    Slot,
    QTimer,
)
import random
# from ...basic.shop import Shop

class Poker21(BaseWindow):
    def __init__(self)->None:
        self.WINDOW_TITLE = "Poker 21"
        super(Poker21, self).__init__()
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_score,self.dealer_score=0,0
        self.current_balance=self.load_data()["balance"]
        self.bet_amount=0.0
        self.setup_ui()
        self.setup_menubar()
        # check balance status and update bet buttons
        self.update_bet_buttons()

    def setup_ui(self)->None:
        # use original coding since the layout is NOT simple
        layout=QVBoxLayout()
        dealers_hand_label=QLabel("Dealer's hand:")
        layout.addWidget(dealers_hand_label)

        self.dealer_cards_label=QLabel("")
        layout.addWidget(self.dealer_cards_label)

        self.info_label=QLabel("")
        layout.addWidget(self.info_label)

        players_hand_label=QLabel("Player's hand:")
        layout.addWidget(players_hand_label)
        
        self.player_cards_label=QLabel("")
        layout.addWidget(self.player_cards_label)

        self.bet_amount_label=QLabel(f"Current Bet: 0€")
        layout.addWidget(self.bet_amount_label)
        # sublayout for bet buttons
        bet_buttons_layout=QHBoxLayout()

        self.bet_buttons = {
            1: QPushButton("Bet 1€"),
            5: QPushButton("Bet 5€"),
            10: QPushButton("Bet 10€"),
            50: QPushButton("Bet 50€"),
            100: QPushButton("Bet 100€"),
            1000: QPushButton("Bet 1.000€"),
            10000: QPushButton("Bet 10.000€"),
        }
        self.bet_buttons[1].clicked.connect(lambda: self.bet(1))
        self.bet_buttons[5].clicked.connect(lambda: self.bet(5))
        self.bet_buttons[10].clicked.connect(lambda: self.bet(10))
        self.bet_buttons[50].clicked.connect(lambda: self.bet(50))
        self.bet_buttons[100].clicked.connect(lambda: self.bet(100))
        self.bet_buttons[1000].clicked.connect(lambda: self.bet(1000))
        self.bet_buttons[10000].clicked.connect(lambda: self.bet(10000))
        bet_buttons_layout.addWidget(self.bet_buttons[1])
        bet_buttons_layout.addWidget(self.bet_buttons[5])
        bet_buttons_layout.addWidget(self.bet_buttons[10])
        bet_buttons_layout.addWidget(self.bet_buttons[50])
        bet_buttons_layout.addWidget(self.bet_buttons[100])
        bet_buttons_layout.addWidget(self.bet_buttons[1000])
        bet_buttons_layout.addWidget(self.bet_buttons[10000])

        self.allin_button = QPushButton(f"ALL IN")
        self.allin_button.clicked.connect(self.allin)
        bet_buttons_layout.addWidget(self.allin_button)

        self.clear_bet_button=QPushButton("Clear Bet")
        self.clear_bet_button.clicked.connect(lambda: self.bet(-self.bet_amount))
        bet_buttons_layout.addWidget(self.clear_bet_button)

        layout.addLayout(bet_buttons_layout)




        self.start_game_button=QPushButton("Start Game")
        self.start_game_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_game_button)

        # sublayout for action buttons
        action_buttons_layout=QHBoxLayout()
        self.hit_button=QPushButton("Hit")
        self.hit_button.clicked.connect(self.hit)
        self.stand_button=QPushButton("Stand")
        self.stand_button.clicked.connect(self.stand)
        self.split_card_button=QPushButton("Split")
        self.split_card_button.clicked.connect(self.split_card)
        action_buttons_layout.addWidget(self.hit_button)
        action_buttons_layout.addWidget(self.stand_button)
        action_buttons_layout.addWidget(self.split_card_button)
        layout.addLayout(action_buttons_layout)

        self.setLayout(layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.split_card_button.setEnabled(False)

    def setup_menubar(self)->None:
        menubar=self.menuBar()
        # add balance menu, just for display
        balance_display = menubar.addAction(str(self.current_balance)+" €")
        balance_display.setEnabled(False)

    def create_deck(self)->list[tuple[str,str]]:
        suits = ['❤', '♦', '♣', '♠']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand:list[tuple[str,str]])->None:
        card = self.deck.pop()
        hand.append(card)

    def calculate_hand_value(self, hand)->int:
        value = 0
        num_aces = 0
        for card in hand:
            rank = card[0]
            if rank == 'A':
                value += 11
                num_aces += 1
            elif rank in ['K', 'Q', 'J']:
                value += 10
            else:
                value += int(rank)
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value

    def start_game(self)->None:
        self.reset_game_data()
        self.close_betting()
        self.start_game_button.setEnabled(False)

        self.deal_card(self.player_hand)
        self.update_player_cards_ui()
        self.deal_card(self.dealer_hand)
        self.update_dealer_cards_ui()
        self.deal_card(self.player_hand)
        self.update_player_cards_ui()
        self.deal_card(self.dealer_hand)
        self.update_dealer_cards_ui()

        self.player_score = self.calculate_hand_value(self.player_hand)
        self.dealer_score = self.calculate_hand_value(self.dealer_hand)

        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)

        if len(self.player_hand)==2 and self.player_hand[0][0]==self.player_hand[1][0]:
            self.split_card_button.setEnabled(True)
            
    def hit(self)->None:
        self.deal_card(self.player_hand)
        self.update_player_cards_ui()
        self.player_score = self.calculate_hand_value(self.player_hand)
        print("Player's hand:", self.player_hand)
    
        if self.player_score > 21:
            self.info_label.setText(f"Sorry, you busted! You lost {self.bet_amount}€.")
            self.cash_out(False)
            self.show_dealer_cards_ui()
        elif self.player_score == 21:
            self.info_label.setText("Player got 21! Dealer's turn.")
            self.hit_button.setEnabled(False)
            self.stand_button.setEnabled(False)
            self.stand()

    def stand(self)->None:
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        while self.dealer_score < 17:
            # use QTimer.singleShot() to simulate dealer's thinking time
            ...
            self.show_dealer_cards_ui()
            self.deal_card(self.dealer_hand)
            self.dealer_score = self.calculate_hand_value(self.dealer_hand)
        self.show_dealer_cards_ui()
        print("Player's hand:", self.player_hand)
        print("Dealer's hand:", self.dealer_hand)
        print("Player's score:", self.player_score)
        print("Dealer's score:", self.dealer_score)
 
        if self.dealer_score > 21:
            self.info_label.setText(f"Dealer busts! You win {self.bet_amount}€.")
            self.cash_out(True)
        elif self.player_score > self.dealer_score:
            if self.player_score==21 and len(self.player_hand)==2:
                self.info_label.setText(f"Blackjack! Player wins x2 bet: {self.bet_amount*2}€.")
                self.cash_out(True,True)
            else:
                self.info_label.setText(f"Player wins {self.bet_amount}€.")
                self.cash_out(True)
        elif self.player_score < self.dealer_score:
            self.info_label.setText(f"Dealer wins. You lost {self.bet_amount}€.")
            self.cash_out(False)
        else:
            self.info_label.setText("It's a tie.")
            self.cash_out(True)
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

    def split_card(self)->None:
        pass
                
    def bet(self,bet:float)->None:
        self.bet_amount+=bet
        self.bet_amount_label.setText(f"Current Bet: {self.bet_amount}€")
        self.update_bet_buttons()
    
    def allin(self)->None:
        print("Player goes all in!")
        self.bet_amount=self.current_balance
        self.bet_amount_label.setText(f"Current Bet: {self.bet_amount}€")
        self.update_bet_buttons()

    def update_bet_buttons(self)->None:
        # disable buttons if the bet amount is more than the current balance
        if self.current_balance==0:
            self.allin_button.setDisabled(True)
            self.start_game_button.setDisabled(True)
            self.clear_bet_button.setDisabled(True)
        else: # has money
            self.allin_button.setDisabled(False)
            if self.bet_amount==0:
                self.start_game_button.setDisabled(True)
                self.clear_bet_button.setDisabled(True)
            else:
                self.start_game_button.setDisabled(False)
                self.clear_bet_button.setDisabled(False)

        diff=self.current_balance-self.bet_amount
        for bet_amount,button in self.bet_buttons.items():
            button.setDisabled(bet_amount>diff)

    def reset_game_data(self)->None:
        self.dealer_cards_label.setText("")
        self.player_cards_label.setText("")
        self.info_label.setText("")

        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_score,self.dealer_score=0,0

    def close_betting(self)->None:
        self.clear_bet_button.setDisabled(True)
        self.allin_button.setDisabled(True)
        for button in self.bet_buttons.values():
            button.setDisabled(True)

    def cash_out(self,won:bool,blackjack:bool=False)->None:
        if won:
            if blackjack:
                self.current_balance=self.current_balance+self.bet_amount*2
            else:
                self.current_balance=self.current_balance+self.bet_amount
        else:
            self.current_balance=self.current_balance-self.bet_amount
        # send a signal to main.py to update the balance
        self.changed_balance.emit(self.current_balance)
        # update GUI balance in poker21.py
        self.getCurrentMenubar().actions()[0].setText(str(self.current_balance)+" €")
        self.allin_button.setText(f"ALL IN")
        # reset bet amount and update bet buttons
        self.bet_amount=0.0
        self.bet_amount_label.setText(f"Current Bet: 0€")
        self.update_bet_buttons()
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

    def update_player_cards_ui(self)->None:
        self.player_cards_label.setText("\t".join([f"{card[0]}{card[1]}" for card in self.player_hand]))

    def update_dealer_cards_ui(self)->None:
        # only shows dealer's first card, the rest are hidden as "?" shown
        self.dealer_cards_label.setText(f"{self.dealer_hand[0][0]}{self.dealer_hand[0][1]}"+("\t?")*(len(self.dealer_hand)-1))

    def show_dealer_cards_ui(self)->None:
        self.dealer_cards_label.setText("\t".join([f"{card[0]}{card[1]}" for card in self.dealer_hand]))