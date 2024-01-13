from card import Card
import deck
from deck import Deck
import game_actions
import os

os.system('cls' if os.name == 'nt' else 'clear')

def card_class_tester():
    card1 = Card(1, "Hearts")
    if(card1.__str__() != "AH"):
        print("card_class_tester test 1 failed")
        print("expected string: AH")
        print("actual string: " + card1.__str__())
        return False
    try:
        card2 = Card(0, "Hearts")
        print("card_class_tester test 2 failed")
        print("expected ValueError")
        return False
    except ValueError:
        pass
    
    try:
        card3 = Card(10, "hakdasfasd")
        print("card_class_tester test 3 failed")
        print("expected ValueError")
        return False
    except:
        pass

    return True

def deck_class_tester():
    deck1 = deck.Deck()
    if(len(deck1.cards) != 52):
        print("deck_class_tester test 1 failed")
        print("expected undealt length: 52")
        print("actual undealt length: " + len(deck1.cards))
        return False
    if(len(deck1.dealt_cards) != 0):
        print("deck_class_tester test 2 failed")
        print("expected dealt length: 0")
        print("actual dealt length: 0" + len(deck1.cards))
        return False
    
    deck1.deal()

    if(len(deck1.cards) != 51):
        print("deck_class_tester test 3 failed")
        print("expected undealt length: 51")
        print("actual undealt length: " + len(deck1.cards))
        return False
    if(len(deck1.dealt_cards) != 1):
        print("deck_class_tester test 4 failed")
        print("expected dealt length: 1")
        print("actual dealt length: 0" + len(deck1.cards))
        return False
    
    test_card = deck1.dealt_cards[0]
    deck1.shuffle()

    if(test_card == deck1.cards[0]):
        print("deck_class_tester test 5 failed")
        print("expected first card to not be " + test_card)
        print("actual first card: " + deck1.cards[0])
        return False
    
    test_card2 = deck1.cards[0]
    deck1.force_deal(test_card2)
    if(test_card2 in deck1.cards):
        print("deck_class_tester test 6 failed")
        print("expected card to be dealt")
        print("actual card not dealt")
        return False
    
    deck2 = Deck(2)
    card_list = deck2.find_cards_to_num(12)
    if(card_list[0].get_value() + card_list[1].get_value() != 12):
        print("deck_class_tester test 7 failed")
        print("expected card values to add to 12")
        print("actual card values add to " + card_list[0].get_value() + card_list[1].get_value())
        print("card 1: " + card_list[0]+ " card 2: " + card_list[1])
        return False
    
    return True

def game_actions_tester_playing():
    Ace1 = Card(1, "Hearts")
    Ace2 = Card(1, "Spades")
    King = Card(13, "Hearts")
    Nine = Card(9, "Diamonds")
    player_hand1 = [Ace1, King]
    dealer_hand1 = [Nine, Ace2]

    #test for blackjack
    game1 = game_actions.GameActions(player_hand1, dealer_hand1)
    game1_return = game1.play_game()
    if(game1_return != 2.5):
        print("game_actions_tester_playing blackjack test 1 failed")
        print("expected game return value: 2.5")
        print("actual game return value: " + game1_return)
        return False
    
    #test dealer draws to 17 when handed an ace
    

def run_all_tests():
    card_class_tester_bool = card_class_tester()
    deck_class_tester_bool = deck_class_tester()

    card_class_tester_result = "pass" if card_class_tester_bool else "fail"
    print("card_class_tester: " + card_class_tester_result)

    deck_class_tester_result = "pass" if deck_class_tester_bool else "fail"
    print("deck_class_tester: " + deck_class_tester_result)

    return card_class_tester_bool and deck_class_tester_bool

def main():
    run_all_tests()
    ##game_actions_tester_playing()

if __name__ == "__main__":
    main()