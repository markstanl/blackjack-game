import card
import random

class Deck:
    def __init__(self):
        self.cards = []
        self.dealt_cards = []
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(card.Card(suits[suit], rank))
        self.shuffle()
        
    def shuffle(self):
        for num in range(len(self.dealt_cards)):
            self.cards.append(self.dealt_cards.pop())
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards.pop()
        self.dealt_cards.append(card)
        return card
    
    def force_deal(self, card):
        self.cards.remove(card)
        self.dealt_cards.append(card)

