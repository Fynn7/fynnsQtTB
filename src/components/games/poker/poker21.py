from baseWindow import BaseWindow
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtCore import (
    Slot,
    QTimer,
)
import random
import time

class Poker21(BaseWindow):
    def __init__(self)->None:
        self.WINDOW_TITLE = "Poker 21"
        super(Poker21, self).__init__()
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_score,self.dealer_score=0,0
        
        self.setup_ui()

    def setup_ui(self)->None:
        self.setLayout(QGridLayout())
        self.addWidgetToLayout("QLabel", "Dealer's hand:")
        self.dealer_cards_label=self.addWidgetToLayout("QLabel", "")
        self.info_label=self.addWidgetToLayout("QLabel", "")  # add a separate line
        self.addWidgetToLayout("QLabel", "Player's hand:")
        self.player_cards_label=self.addWidgetToLayout("QLabel", "")

        self.start_game_button=self.addWidgetToLayout("QPushButton", "Deal cards", self.start_game)

        self.hit_button=self.addWidgetToLayout("QPushButton", "Hit", self.hit)
        self.stand_button=self.addWidgetToLayout("QPushButton", "Stand", self.stand)
        self.split_card_button=self.addWidgetToLayout("QPushButton", "Split", self.split_card)

        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.split_card_button.setEnabled(False)

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
            self.info_label.setText("Player busts! Dealer wins.")
            self.show_dealer_cards_ui()
            self.start_game_button.setEnabled(True)
            self.hit_button.setEnabled(False)
            self.stand_button.setEnabled(False)
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

        result=""   
        if self.dealer_score > 21:
            result="Dealer busts! Player wins."
        elif self.player_score > self.dealer_score:
            result="Player wins."
        elif self.player_score < self.dealer_score:
            result="Dealer wins."
        else:
            result="It's a tie."
        self.info_label.setText(result)
        self.start_game_button.setEnabled(True)
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)

    def split_card(self)->None:
        pass
            

    def reset_game_data(self)->None:
        self.dealer_cards_label.setText("")
        self.player_cards_label.setText("")
        self.info_label.setText("")

        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_score,self.dealer_score=0,0

    def update_player_cards_ui(self)->None:
        self.player_cards_label.setText("\t".join([f"{card[0]}{card[1]}" for card in self.player_hand]))

    def update_dealer_cards_ui(self)->None:
        # only shows dealer's first card, the rest are hidden as "?" shown
        self.dealer_cards_label.setText(f"{self.dealer_hand[0][0]}{self.dealer_hand[0][1]}"+("\t?")*(len(self.dealer_hand)-1))

    def show_dealer_cards_ui(self)->None:
        self.dealer_cards_label.setText("\t".join([f"{card[0]}{card[1]}" for card in self.dealer_hand]))