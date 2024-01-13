import random

class Card:
    def __init__(self, value: int, suit: str):
        if(suit not in ["Hearts", "Diamonds", "Spades", "Clubs"]):
            raise ValueError("Invalid suit")
        if(suit == None):
            self.suit = random.choice(["Hearts", "Diamonds", "Spades", "Clubs"])
        elif(value not in range(1, 14)):
            raise ValueError("Invalid value")
        else:
            self.suit = suit
        self.value = value
    
    def get_value(self):
        if(self.value == 1):
            return 11
        elif(self.value in range(10, 14)):
            return 10
        else:
            return self.value

    def __str__(self):
        actual_value_array = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        return f"{actual_value_array[self.value-1]}{self.suit[0]}"
    
    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        return self.__str__()[key]