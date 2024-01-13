import deck
import time

class GameActions:

    def __init__(self, force_player_hand: [] = None, force_dealer_hand: [] = None, action: [] = None, size: int = 1):
        self.deck = deck.Deck(size)
        self.player_cards = []
        self.player_ace_count = 0
        self.dealer_cards = []
        self.dealer_ace_count = 0

        # we have this conditional to allow forced hands for testing and data analysis
        # it conditionally fills a hand with the cards aforementioned, and randomly deals the rest
        if force_player_hand == None and force_dealer_hand == None:
            self.deal()
        elif force_player_hand == None and force_dealer_hand != None:
            self.dealer_cards = force_dealer_hand
            self.player_cards.append(self.deck.deal())
            self.player_cards.append(self.deck.deal())
        elif force_player_hand != None and force_dealer_hand == None:
            self.player_cards = force_player_hand
            self.dealer_cards.append(self.deck.deal())
            self.dealer_cards.append(self.deck.deal())
        else:
            self.player_cards = force_player_hand; self.dealer_cards = force_dealer_hand
        
        force_player_hand = [] if force_player_hand is None else force_player_hand
        force_dealer_hand = [] if force_dealer_hand is None else force_dealer_hand

        # removes the cards from the deck that are in the forced hands
        for player_forced_cards in force_player_hand:
            self.deck.force_deal(player_forced_cards)
        for dealer_forced_cards in force_dealer_hand:
            self.deck.force_deal(dealer_forced_cards)

    """
    Plays a game of blackjack for a user. Happens slowly and prints values for the user to see.
    Returns: an integer multiplier of the bet
    """
    def play_game(self):

        print(f"Player: {self.player_cards}")
        print(f"Dealer: [{self.dealer_cards[0]}, ??]")

        # if the dealers visible card is an ace, ask for insurance
        # for ease, we play insurance similar to surrender, where the player gets half their bet back. This will change with the bot
        insurance_taken = False
        if(self.dealer_cards[0][0] == "A"):
            player_input = input("Dealer shows an ace. Insurance? Y/N:")

            while(player_input not in ["Y", "N"]):
                player_input = input("Invalid input. Dealer shows an ace. Insurance? Y/N:")
                player_input = player_input.upper()
            if(player_input == "Y"):
                return 0.5

        check_blackjack = self.check_blackjack(insurance_taken)
        if(check_blackjack != -1):
            if(check_blackjack == 1):
                print("Push!")
            elif(check_blackjack == 2.5):
                print("Blackjack!")
            elif(check_blackjack == 0):
                print("Dealer wins!")
            return check_blackjack
        
        while(self.get_player_number() < 21):
            while True:
                player_input = input("Enter your move. H for hit, S for stand: ")
                player_input = player_input.upper()
                if player_input in ["H", "S"]:
                    break
                else:
                    print("Invalid input.")
            
            if(player_input == "H"):
                self.hit("player")
                print(f"You hit: {self.player_cards[-1]}")
                print(f"Your current hand: {self.player_cards}")
                time.sleep(2)
            
            if(player_input == "S"):
                break

            if(self.get_player_number() > 21):
                print("You bust!")
                return 0

        print(f"Your final hand: {self.player_cards}")
        print(f"Dealer's hand: {self.dealer_cards} {self.dealer_ace_count}")

        time.sleep(2)

        self.play_dealer()

        if(self.get_dealer_number() > 21):
            print("You win!")
            return 2

        print(f"Dealer's final hand: {self.dealer_cards}")

        if(self.get_dealer_number() == self.get_player_number()):
            print("Push!")
            return 1
        elif(self.get_dealer_number() > self.get_player_number()):
            print("Dealer wins!")
            return 0
        else:
            print("You win!")
            return 2
   
    def play_simulated_game(self, action: str):
        pass

    def play_dealer(self):
        dealer_number = self.get_dealer_number()
        while(dealer_number < 17 or (dealer_number >= 17 and self.dealer_ace_count > 0)):
            self.hit("dealer")
            print(f"Dealer hits: {self.dealer_cards[-1]}")
            time.sleep(1)
            print(f"Dealer's current hand: {self.dealer_cards}")
            time.sleep(1)
            dealer_number = self.get_dealer_number()
            print(self.get_dealer_number())
        if(dealer_number > 21):
            print("Dealer bust!")
            return 2


    """
    Calculates the value of a players hand
    Returns the value of the player's hand, liberably accounting for aces"""
    def get_player_number(self):
        player_number = 0
        for card in self.player_cards:
            player_number += card.get_value()
        player_ace_copy = self.player_ace_count
        while(player_number > 21 and player_ace_copy > 0):
            player_number -= 10
            player_ace_copy -= 1
        return player_number
    
    def get_dealer_number(self):
        dealer_number = 0
        for card in self.dealer_cards:
            dealer_number += card.get_value()
        dealer_ace_copy = self.dealer_ace_count
        while(dealer_number > 21 and dealer_ace_copy > 0):
            dealer_number -= 10
            dealer_ace_copy -= 1
        return dealer_number

    def hit(self, person: str):
        if(person == "player"):
            card_append_copy = self.deck.deal()
            if(card_append_copy[0] == "A"):
                self.player_ace_count += 1
            self.player_cards.append(card_append_copy)
        elif(person == "dealer"):
            card_append_copy = self.deck.deal()
            if(card_append_copy[0] == "A"):
                self.dealer_ace_count += 1
            self.dealer_cards.append(card_append_copy)


    def deal(self):
        for num in range(2):
            self.player_cards.append(self.deck.deal())
            self.dealer_cards.append(self.deck.deal())

    def check_blackjack(self, insurance_taken: bool):
        player_blackjack = self.get_player_number() == 21
        dealer_blackjack = self.get_dealer_number() == 21

        if(player_blackjack and dealer_blackjack): return 1
        if(player_blackjack): return 2.5
        if(dealer_blackjack): return 0
        return -1

    def __str__(self):
        return f"Player: {self.playerCards}\nDealer: {self.dealerCards}"
    
def main():
    game = GameActions()
    game.play_game()

if __name__ == "__main__":
    main()