# whist
Simulation of Whist Card Game

## Card Game 

There are 4 players 
Deck of 52 cards 
Shuffle the deck
Distribute the cards among players 
Choose a random trump suit before the start of the game 	
Choose a random starting player 

Start the game.

First player puts a card on table. 
Subsequently other players also put their cards on the table. 
At the end of 4 cards, one of the players is declared winner based on card evaluation. 

The winner of this round starts the next round and so on. 

### Evaluation logic 

Suit of the first card in a round is the suit of the hand. 

Trump suit > suit of the hand > others
A > K > Q > J > 10 > 9 > 8  …  > 3 > 2

### Rule of the game 
If a player has a card of suit of the hand, he has to put it irrespective of whether or not he is going to win. 

### Player logic : 

If player is starting the round, he puts the highest face value card that he has.
If not the starting player,  
  If he can win the round so far, put the card with highest chance of winning
  If he can’t win the round so far, put the card that minimizes the loss.

