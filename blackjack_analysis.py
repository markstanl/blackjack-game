import game_actions
from card import Card
from deck import Deck

def hard_twenty_vs_all(num_of_decks: int = 1):
    temp_deck = Deck()
    player_cards = temp_deck.find_cards_to_num(20)
    dealer_cards = temp_deck.find_cards_to_num(19)
    # game1 = game_actions.GameActions()
    print(f"Player: {player_cards} Dealer: {dealer_cards}")



def run_all_tests(num_of_decks: int = 1):
    hard_twenty_vs_all(num_of_decks)

def main():
    run_all_tests(2)

if __name__ == "__main__":
    main()