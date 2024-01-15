from card import Card

class GameActor:

    def __init__(self, stack_size: int = 1000, hand: [] = None, bet_size: int = 100, player_name: str = "Player"):
        self.player_name = player_name
        self.ace_count = 0
        if hand is None:
            self.hand = []
        else:
            if len(hand) != 2 and len(hand) != 0:
                raise ValueError("Dealer must have 2 or 0 cards. Your hand has " + len(hand) + " cards")
            self.hand = hand
            for unique_card in self.hand:
                if unique_card.get_value() == 11:
                    self.ace_count += 1
        self.stack_size = stack_size
        self.bet_size = bet_size
    
    def set_hand(self, cards: []):
        if len(cards) != 2:
            raise ValueError("Dealer must have 2 cards")
        self.ace_count = 0
        for unique_card in cards:
            if unique_card.get_value() == 11:
                self.ace_count += 1
        self.hand = cards

    def add_card(self, card: Card):
        if not card:
            raise ValueError("Card must be valid and defined")
        if card.get_value() == 11:
            self.ace_count += 1
        self.hand.append(card)

    def get_hand_value(self):
        hand_value = 0
        ace_count = self.ace_count # we need a copy, as we can call this method multiple times
        for card in self.hand:
            if(card.get_value() == 1):
                ace_count = 0
            hand_value += card.get_value()
        while ace_count > 0 and hand_value > 21:
            hand_value -= 10
            ace_count -= 1
        return hand_value
    
    def get_hand_ace_count(self):
        ace_count = 0
        for card in self.hand:
            if(card.get_value() == 1):
                ace_count += 1
        return ace_count
    
    def get_name(self):
        return self.player_name
    
    def clear_hand(self):
        self.hand = []

    def can_split(self):
        if len(self.hand) != 2:
            return False
        return self.hand[0].get_value() == self.hand[1].get_value()
    
    def split(self):
        return_card = self.hand[1] # saves the returned card
        self.hand.pop() # removes the returned card
        return return_card # returns the removed card

    def visualize(self): # We have this ugly long method because we need to print the cards inline
        str_repr = ""
        for num in range(len(self.hand)):
            str_repr += f"┌─────────┐  "
        str_repr += "\n"
        for card in self.hand:
            if len(str(card)) == 2:
                str_repr += f"│ {str(card)[0]:<7} │  "
            else:
                str_repr += f"│ {str(card)[:2]:<7} │  "
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
            if len(str(card)) == 2:
                str_repr += f"│ {str(card)[0]:>7} │  "
            else:
                str_repr += f"│ {str(card)[:2]:>7} │  "
        str_repr += "\n"
        for num in range(len(self.hand)):
            str_repr += f"└─────────┘  "
        str_repr += "\n"
        return str_repr

    def __str__(self):
        return f"{self.player_name} {self.hand}"
    
    def __repr__(self):
        return self.__str__()

    
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

    def __init__(self, hand: [] = None):
        self.ace_count = 0
        if hand is None:
            self.hand = []
        else:
            if len(hand) != 2 and len(hand) != 0:
                raise ValueError("Dealer must have 2 or 0 cards")
            self.hand = hand
            for unique_card in hand:
                if unique_card.get_value() == 11:
                    self.ace_count += 1

    def set_hand(self, cards: []):
        if len(cards) != 2:
            raise ValueError("Dealer must have 2 cards")
        self.ace_count = 0
        for unique_card in cards:
            if unique_card.get_value() == 11:
                self.ace_count += 1
        self.hand = cards
    
    def add_card(self, card: Card):
        if not card:
            raise ValueError("Card must be valid and defined")
        if card.get_value() == 11:
            self.ace_count += 1
        self.hand.append(card)

    def clear_hand(self):
        self.hand = []
        self.ace_count = 0

    def get_hand_value(self):
        hand_value = 0
        ace_count = self.ace_count
        for card in self.hand:
            if(card.get_value() == 1):
                ace_count = 0
            hand_value += card.get_value()
        while ace_count > 0 and hand_value > 21:
            hand_value -= 10
            ace_count -= 1
        return hand_value
    
    def dealer_show_ace(self):
        return self.hand[0].get_value() == 11
    
    def visualize_before_dealer_show(self):
        str_repr = ""
        card = self.hand[0]
        str_repr += "┌─────────┐  ┌─────────┐"
        str_repr += "\n"
        if len(str(card)) == 2:
            str_repr += f"│ {str(card)[0]:<7} │  │░░░░░░░░░│  "
        else:
            str_repr += f"│ {str(card)[:3]:<7} │  │░░░░░░░░░│  "
        str_repr += "\n"
        str_repr += f"│    {card.suit_icon}    │  │░░░░░░░░░│  "
        str_repr += "\n"
        str_repr += f"│   {card.suit_icon*3}   │  │░ CARDS ░│    "
        str_repr += "\n"
        str_repr += f"│    {card.suit_icon}    │  │░░░░░░░░░│  "
        str_repr += "\n"
        str_repr += f"│ {str(card)[0]:>7} │  │░░░░░░░░░│  "
        str_repr += "\n"
        str_repr += f"└─────────┘  └─────────┘"
        return str_repr

    def visualize(self): # We have this ugly long method because we need to print the cards inline
        str_repr = ""
        for num in range(len(self.hand)):
            str_repr += f"┌─────────┐  "
        str_repr += "\n"
        for card in self.hand:
            if len(str(card)) == 2:
                str_repr += f"│ {str(card)[0]:<7} │  "
            else:
                str_repr += f"│ {str(card)[:3]:<7} │  "
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
    
    def print_dealer_hand_value(self):
        print(f"Dealer's hand value: {self.get_hand_value()}")

    def __str__(self):
        return f"{self.hand}"
    
    def __repr__(self):
        return self.__str__()

