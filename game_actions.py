import deck
import time
from game_actor import GameActor 
from game_actor import Dealer

class Game:

    """
    This is the constructor for the Game class
    We have 2 kinds of constructors, if num_of_players is defined, we will play a user game
    Otherwise, we will play a data game"""
    def __init__(self, player: GameActor = None, dealer: Dealer = None, 
                 shoe_size: int = 1, num_of_players: int = None, flat_bet_spread: bool = False,
                 bet_size: int = None):
        if num_of_players is not None: # If we are playing a user game
            if(num_of_players < 1):
                raise ValueError("Must have at least 1 player")
            if(num_of_players > 5):
                raise ValueError("Cannot have more than 5 players")
            if(shoe_size < 1):
                raise ValueError("Must have at least 1 deck")
            if(shoe_size > 8):  
                raise ValueError("Cannot have more than 8 decks")
            if bet_size is not None:
                if(bet_size < 0 or bet_size > 1000):
                    raise ValueError("Bet size must be between 0 and 1000")
            
            self.bet_size = bet_size
            self.flat_bet_spread = flat_bet_spread # if we the player wants the same bet for each person
            #initialize a list of players
            self.players = []

            #little array we have that keeps track of if a player has blackjack
            self.blackjack_player = [False for _ in range(num_of_players+1)] 
            
            for num in range(num_of_players):
                self.players.append(GameActor(player_name = f"Player {num+1}"))
            self.dealer = Dealer() # intialize the dealer
            self.deck = deck.Deck(shoe_size) # Initialize the deck
            self.deck.shuffle()

            self.bet_list = [] # initialize the bet list
            self.insurance_bet_list = [] # initialize the insurance bet list

            self.play_user_game() # play the user input game game
        else: # If we are playing a data game
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
            self.play_data_game() # play the data game

    def play_user_game(self):
        # DEALS THE PLAYERS
        for player in self.players:
            self.deal(player)
        self.deal(self.dealer)


        #TAKES PLAYERS BETS
        if self.bet_size is None:
            self.take_player_bet_spread() # Take the player bets
        else:
            for player in self.players:
                self.bet_list.append(player.make_bet(self.bet_size))

        # SHOWS THE USERS HANDS
        for num in range(len(self.players)): # For each player
            print(f"{self.players[num].player_name} hand:")
            self.print_player_hand_info(player)
            time.sleep(2)

        print("Dealer's hand:")
        print(self.dealer.visualize_before_dealer_show())

        time.sleep(2)

        # OFFERS INSURANCE
        if(self.dealer.dealer_show_ace()): #if the dealer shows an ace we offer insurance
            for player in self.players:
                self.offer_insurance(player)
        
        #CHECKS FOR BLACKJACK
        self.check_for_blackjack() # Check for blackjack


        #PLAYS THE GAME
        if self.blackjack_player[-1]: # If the dealer has blackjack
            print("Dealer has blackjack")
            #prints results
            for num in range(len(self.players)):
                print(f"{self.players[num].player_name}'s bust") if self.blackjack_player[num] else print(f"{self.players[num].player_name}'s Push") 
                #prints bust if the player doesnt have a blackjack, push otherwise
                if self.insurance_bet_list[num] > 0:
                    #returns the insurance bet if blackjack has been hit
                    print(f"{self.players[num].player_name}'s insurance bet won")
                    self.players[num].collect_winnings(self.insurance_bet_list[num]*2)
        else: # if the dealer does not have blackjack we want to play through the other hands
            for player in self.players:
                print(player.__str__)
                if not self.blackjack_player[self.players.index(player)]:
                    while(player.can_split()):
                        self.split_option(player)
                    self.play_hand(player)
                else:
                    print(f"{self.players[num].player_name}'s blackjack")
        
        #at this point, all players should be done, we want the dealer to show, and then hit until 16, and soft 17
        print("Dealer's Hand:")
        self.print_player_hand_info(self.dealer)

        time.sleep(3)

        self.dealer_draw(self.dealer)

        for player in self.players:
            if(player.get_hand_value() == self.dealer.get_hand_value()):
                print(f"{self.players[num].player_name} push")
                player.collect_winnings(self.bet_list[self.players.index(player)]) # return the amount bet to the player

            elif(player.get_hand_value() > self.dealer.get_hand_value()):
                print(f"{self.players[num].player_name} wins")
                player.collect_winnings(self.bet_list[self.players.index(player)]*2) # return double the amount
            
            else:
                print(f"{self.players[num].player_name} lose")


    def dealer_draw(self, dealer: Dealer):
        #the dealer hits until they get to 17+ and that that 17 is not soft
        while dealer.get_hand_value() < 17 and dealer.get_hand_value() == 17 and dealer.ace_count > 0:
            self.hit(dealer) # hit the dealer
            print("Dealer's current hand")
            self.print_player_hand_info(dealer) # print the dealer info
        if(dealer.get_hand_value() > 21):
            print("Dealer bust!")

    def check_for_blackjack(self):
        for player in self.players:
            if(player.get_hand_value() == 21):
                self.blackjack_player[self.players.index(player)] = True
    
        if(self.dealer.get_hand_value() == 21):
            self.blackjack_player[-1] = True

    def take_player_bet_spread(self):
        if self.flat_bet_spread:  # If we are using the same bet for each player
            print("Enter your flat bet size")
            print("It is recommended to bet less than half of each of your stack size, to allow you to split or double down ")
            player_info = ""
            for num in range(len(self.players)):
                player_info += f"Player {num+1}'s stack: {self.players[num].stack_size}\n"
            print(player_info)
            while True:                 
                player_input = input("Enter bet size: ")
                try:
                    bet_size = int(player_input)  # if the input is not an integer, this will throw an error
                    if bet_size < 0:  # check the bet is positive
                        raise ValueError("Bet size must be positive")
                    for player in self.players:  # check the bet is less than the stack size for each player
                        if bet_size > player.stack_size:
                            raise ValueError("Bet size cannot be greater than stack size")
                    for player in self.players:
                        self.bet_list.append(player.make_bet(bet_size))
                    break
                except ValueError as e:
                    print(e)
        else:  # if the bets differ per player
            for num in range(len(self.players)):
                print(f"Player {num+1}'s stack: {self.players[num].stack_size}")
                while True:
                    player_input = input("Enter bet size: ")
                    try:
                        bet_size = int(player_input)
                        if bet_size < 0:
                            raise ValueError("Bet size must be positive")
                        if bet_size > self.players[num].stack_size:
                            raise ValueError("Bet size cannot be greater than stack size")
                        self.bet_list.append(self.players[num].make_bet(bet_size))
                        break
                    except ValueError as e:
                        print(e)

    def play_data_game(self):
        pass
    
    def play_hand(self, player: GameActor):
        print(f"{player.player_name}'s turn")
        print("Current hand: ")
        print(player.visualize())
        print("Current bet: "+str(self.bet_list[self.players.index(player)]))
        time.sleep(3)
        finished = False
        while not finished:
            self.print_player_hand_value(player)
            player_input = input("Do you want to hit, stand, or double down? (H/S/D): ")
            #Quick conditional for valid input, and check that the player can doubel down
            while player_input.upper() not in ["H", "S", "D"] or (player_input.upper() == "D" and player.stack_size < self.bet_list[self.players.index(player)]):
                if player_input.upper() == "D" and player.stack_size < self.bet_list[self.players.index(player)]:
                    player_input = input("You do not have enough money to double down. Do you want to hit or stand? (H/S): ")
                else: 
                    player_input = input("Invalid input. Do you want to hit, stand, or double down? (H/S/D): ")
                    
            if player_input.upper() == "H": #the hit option
                self.hit(player)
                print("You hit. Current hand: ")
                self.print_player_hand_info(player)
                time.sleep(1)
                if player.get_hand_value() > 21:
                    print("You bust")
                    break
                time.sleep(1)
                #you can hit again after hitting, we allow for this  
                player_input = input("Do you want to hit, stand:")
                while player_input.upper() != "S":
                    while player_input.upper() not in ["H", "S"]:
                        player_input = input("Invalid input. Do you want to hit, stand: ")
                    if player_input.upper() == "H":
                        self.hit(player)
                        print("You hit. Current hand: ")
                        self.print_player_hand_info(player)
                        time.sleep(1)
                        if player.get_hand_value() > 21:
                            print("You bust")
                            finished = True
                            break
                        finished = True
                        time.sleep(1)
                    else: #stand option
                        print("You stand. Current hand: ")
                        self.print_player_hand_info(player)
                        finished = True
                        break
            elif(player_input.upper() == "S"): #stand option
                print("You stand. Current hand: ")
                self.print_player_hand_info(player)
                time.sleep(1)
                finished = True
                break
            else: #double down
                self.hit(player)
                print("You double down. Current hand: ")
                self.print_player_hand_info(player)
                #doubles the bet
                self.bet_list[self.players.index(player)] += player.make_bet(self.bet_list[self.players.index(player)]) 
                print("current bet: "+str(self.bet_list[self.players.index(player)]))
                if player.get_hand_value() > 21:
                    print("You bust")
                finished = True
                break

    #@ TODO: make sure the stack sizes combine when a player is split
    def split_option(self, player: GameActor):
        if player.stack_size >= self.bet_list[self.players.index(player)]: # they need to have enough money to split to split
            player_input = input("Do you want to split? (Y/N): ")
            while player_input.upper() not in ["Y", "N"]:
                player_input = input("Invalid input. Do you want to split? (Y/N): ")
            
            if player_input.upper() == "Y":
                # make the new actor
                split_game_actor = GameActor(stack_size = player.stack_size, bet_size = self.bet_list[self.players.index(player)], 
                                            player_name = player.player_name+" split")
                # add the actor to the player list
                self.players.insert(self.players.index(player)+1, split_game_actor)
                # add the bet to the bet list
                self.bet_list.insert(self.players.index(player)+1, split_game_actor.bet_size())
                #add the removed card to the new player
                split_game_actor.add_card(self.split(player))
                #hit them both to put them at a new hand
                self.hit(split_game_actor)
                self.hit(player)

                #print the current hand after hit
                print(player.player_name+"'s new hand:")
                self.print_player_hand_info(player)

                print(split_game_actor.player_name+"'s new hand:")
                self.print_player_hand_info(split_game_actor)


    def offer_insurance(self, player: GameActor):
        print(f"Player {self.players.index(player)+1}'s turn")
        while True:
            player_input = input("Do you want insurance? (Y/N): ")
            if player_input.upper() == "Y":
                self.insurance_bet_list.append(player.make_bet(self.bet_list[self.players.index(player)]))
                break
            elif player_input.upper() == "N":
                self.insurance_bet_list.append(0)
                break
            else:
                print("Invalid input")

    def deal(self, game_user: GameActor or Dealer):
        game_user.add_card(self.deck.deal())
        game_user.add_card(self.deck.deal())

    def hit(self, game_user: GameActor or Dealer):
        game_user.add_card(self.deck.deal())

    def print_player_hand_info(self, user: GameActor or Dealer):
        if isinstance(user, GameActor):
            print(user.visualize())
            print("current bet: "+str(self.bet_list[self.players.index(user)]))
            self.print_player_hand_value(user)
        else:
            print(user.visualize())
            user.print_dealer_hand_value()

    def print_player_hand_value(self, player: GameActor):
        if player.get_hand_ace_count() >= 1:
            print(f"You have {player.get_hand_value()} or {player.get_hand_value()-10}")
        else:
            print(f"You have {player.get_hand_value()}")

def main():
    game = Game(num_of_players=2, flat_bet_spread=True, bet_size = 100)

if __name__ == "__main__":
    main()