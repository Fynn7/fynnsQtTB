from baseWindow import BaseWindow
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtCore import (
    Slot
)
import random

class Poker21(BaseWindow):
    def __init__(self):
        self.WINDOW_TITLE = "Poker 21"
        super(Poker21, self).__init__()
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        card = self.deck.pop()
        hand.append(card)

    def calculate_hand_value(self, hand):
        value = 0
        num_aces = 0
        for card in hand:
            rank = card[0]
            if rank == 'Ace':
                value += 11
                num_aces += 1
            elif rank in ['King', 'Queen', 'Jack']:
                value += 10
            else:
                value += int(rank)
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value

    def play_game(self):
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)

        player_score = self.calculate_hand_value(self.player_hand)
        dealer_score = self.calculate_hand_value(self.dealer_hand)

        print("Player's hand:", self.player_hand)
        print("Dealer's hand:", self.dealer_hand[0])

        while True:
            choice = input("Do you want to hit or stand? (h/s): ")
            if choice.lower() == 'h':
                self.deal_card(self.player_hand)
                player_score = self.calculate_hand_value(self.player_hand)
                print("Player's hand:", self.player_hand)
                if player_score > 21:
                    print("Player busts! Dealer wins.")
                    return
            elif choice.lower() == 's':
                break
            else:
                print("Invalid choice. Please enter 'h' or 's'.")

        while dealer_score < 17:
            self.deal_card(self.dealer_hand)
            dealer_score = self.calculate_hand_value(self.dealer_hand)

        print("Player's hand:", self.player_hand)
        print("Dealer's hand:", self.dealer_hand)
        print("Player's score:", player_score)
        print("Dealer's score:", dealer_score)

        if dealer_score > 21:
            print("Dealer busts! Player wins.")
        elif player_score > dealer_score:
            print("Player wins.")
        elif player_score < dealer_score:
            print("Dealer wins.")
        else:
            print("It's a tie.")