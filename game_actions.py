import deck
import time
from game_actor import GameActor 
from game_actor import Dealer

class Game:

    """
    This is the constructor for the Game class
    We have 2 kinds of constructors, if num_of_players is defined, we will play a user game
    Otherwise, we will play a data game"""
    def __init__(self, player: GameActor = None, dealer: Dealer = None, shoe_size: int = 1, num_of_players: int = None):
        if num_of_players is not None:
            if(num_of_players < 1):
                raise ValueError("Must have at least 1 player")
            if(num_of_players > 5):
                raise ValueError("Cannot have more than 5 players")
            if(shoe_size < 1):
                raise ValueError("Must have at least 1 deck")
            if(shoe_size > 8):  
                raise ValueError("Cannot have more than 8 decks")
            
            #initialize a list of players
            self.players = []
            for num in range(num_of_players):
                self.players.append(GameActor())
            self.dealer = Dealer() # intialize the dealer
            self.deck = deck.Deck(shoe_size) # Initialize the deck
            self.deck.shuffle()

            self.play_user_game() # play the user input game game
        else: 
            self.play_user_game() # play the user input game game
            if(player is None):
                self.player = GameActor()
                self.deal(player)
            else:
                self.player = player
            if(dealer is None):
                self.dealer = Dealer()
            else:
                self.dealer = dealer
            self.deck = deck.Deck(shoe_size)
            self.deck.shuffle()

    def play_user_game(self):
        pass
    
    def starting_moves(self):
        pass
    

    def deal(self, game_user: GameActor or Dealer):
        game_user.add_card(self.deck.deal())
        game_user.add_card(self.deck.deal())

    def hit(self, game_user: GameActor or Dealer):
        game_user.add_card(self.deck.deal())

def main():
    game = Game()
    game.play_user_game()

if __name__ == "__main__":
    main()