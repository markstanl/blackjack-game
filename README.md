# Blackjack Game
Blackjack is a simply gambling game popular among casinos worldwide. I am recreating it in
python using object-oriented programming. But, my eventual goal is to make a blacjack bot.
I will start off by just making a functional blackjack game. Then, I will confirm basic strategy with
a Monte Carlo simulation, by testing different hand setups with different strategy and seeing the best result.
I also then want to mathematically confirm using some computer algorithm (calculating the number of winn/losing
cards in the shoe)

I want all of this to be able to quickly run, and allow for different starting values, like different shoe size.
I then want it to consider different optimal count strategies, and maybe even eventually strategy when the dealer
cards are known

Overall, I want this to be a very fun way to visualize complex data

# Deck Class
A simple class that creates instances of the card class. A better name is probably the shoe, as it can have multiple
decks inside of it. Alas, it keeps track of the played cards, and remaining cards.

# Game Actions Class
The game actions class is where the game is played. It allows for a user input game to be played, as well as put in arrays in
to force hands, and I eventually intend on allowing a bot to play in-line with an array of dependencies

# Blackjack Analysis
I am about to verbalize what I want to do with the dependency arrays
I want to simply simulate a Hit, Stand, or Double Down, but double down later