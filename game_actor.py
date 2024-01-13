from card import Card

class GameActor:

    def __init__(self, stack_size: int = 1000, hand: [] = [], bet_size: int = 100):
        if len(hand) != 2 and len(hand) != 0:
            raise ValueError("Dealer must have 2 or 0 cards. Your hand has " + len(hand) + " cards")
        self.hand = hand
        self.stack_size = stack_size
        self.bet_size = bet_size
    
    def set_hand(self, cards: []):
        if len(cards) != 2:
            raise ValueError("Dealer must have 2 cards")
        self.hand = cards

    def add_card(self, card: Card):
        if not card:
            raise ValueError("Card must be valid and defined")
        self.hand.append(card)

    def visualize(self): # We have this ugly long method because we need to print the cards inline
        str_repr = ""
        for num in range(len(self.hand)):
            str_repr += f"┌─────────┐  "
        str_repr += "\n"
        for card in self.hand:
            str_repr += f"│ {str(card)[0]:<7} │  "
        str_repr += "\n"
        for card in self.hand:
            str_repr += f"│    {card.suit_icon}    │  "
        str_repr += "\n"
        for card in self.hand:
            str_repr += f"│   {card.suit_icon*3}   │  "
        str_repr += "\n"
        for card in self.hand:
            str_repr += f"│    {card.suit_icon}    │  "
        str_repr += "\n"
        for card in self.hand:
            str_repr += f"│ {str(card)[0]:>7} │  "
        str_repr += "\n"
        for num in range(len(self.hand)):
            str_repr += f"└─────────┘  "
        str_repr += "\n"
        return str_repr

    def __str__(self):
        return f"{self.hand}"
    
    def make_bet(self, bet_size: int = None):
        if bet_size is None:
            bet_size = self.bet_size
        if bet_size < 0:
            raise ValueError("Bet size cannot be negative")
        self.stack_size -= bet_size
        return bet_size
    
    def collect_winnings(self, winnings: int):
        if winnings < 0:
            raise ValueError("Winnings cannot be negative")
        self.stack_size += winnings

class Dealer:

    def __init__(self, hand: [] = []):
        if len(hand) != 2 or len(hand) != 0:
            raise ValueError("Dealer must have 2 or 0 cards")
        self.hand = hand

    def set_hand(self, cards: []):
        if len(cards) != 2:
            raise ValueError("Dealer must have 2 cards")
        self.hand = cards
    
    def add_card(self, card: Card):
        if not card:
            raise ValueError("Card must be valid and defined")
        self.hand.append(card)
