import card
import random

class Deck:
    def __init__(self, size: int = 1, seed: int = None):
        if seed is not None:
            random.seed(seed)
        self.cards = []
        self.dealt_cards = []
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        for num in range(size):   
            for suit in range(4):
                for rank in range(1, 14):
                    self.cards.append(card.Card(rank, suits[suit]))
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

    """
    Method we are defining to assist in finding numbers that bring the sum of the hand to the integer we input
    
    Args:
        num: the integer we want to find cards to add up to
        
    Returns:
        The array of cards
    
    Raises:
        ValueError: If no cards are found with an easy sum"""
    def find_cards_to_num(self, num: int):
        if(num > 10):
            index = 0
            while True:
                if(self.cards[index].get_value() == num-10):
                    break
                if(index == len(self.cards)-1):
                    raise ValueError("No cards found")
                index += 1
            card1 = self.cards[index]
            self.force_deal(card1)

            index = 0
            while True:
                if(self.cards[index].get_value() == 10):
                    break
                if(index == len(self.cards)-1):
                    raise ValueError("No cards found")
                index += 1
            card2 = self.cards[index]
            return [card1, card2]
        else:
            index = 0
            while True:
                if(self.cards[index].get_value() == num-2):
                    break
                if(index == len(self.cards)-1):
                    raise ValueError("No cards found")
                index += 1
            card1 = self.cards[index]
            self.force_deal(card1)

            index = 0
            while True:
                if(self.cards[index].get_value() == 2):
                    break
                if(index == len(self.cards)-1):
                    raise ValueError("No cards found")
                index += 1
            return [card1, card2]

    def __str__(self):
        return f"Cards: {len(self.cards)}\nDealt Cards: {len(self.dealt_cards)} "