import random

Trump = None
Curr_hand = None


class Card:
    suits = ['\u2666', '\u2665', '\u2663', '\u2660']  # ["Clubs", "Diamonds", "Hearts", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit=0, rank=0):
        """Default constructor """
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a human-readable string representation """
        return '%s %s' % (Card.suits[self.suit], Card.ranks[self.rank])
        # return '%s of %s' % (Card.rank_names[self.rank], Card.suit_names[self.suit])

    def __lt__(self, other):
        """Overriding < operator """
        if self is None:
            return True
        elif other is None:
            return False
        elif self.suit == Trump and other.suit == Trump:
            t1 = self.rank
            t2 = other.rank
            return t1 < t2
        elif self.suit == Trump:
            return False
        elif other.suit == Trump:
            return True
        elif self.suit == Curr_hand and other.suit == Curr_hand:
            t1 = self.rank
            t2 = other.rank
            return t1 < t2
        elif self.suit == Curr_hand:
            return False
        elif other.suit == Curr_hand:
            return True
        else:
            t1 = self.rank, self.suit
            t2 = other.rank, other.suit
            return t1 < t2


class Deck:
    def __init__(self):
        """Initializes the Deck with 52 cards."""
        self.cards = []
        for suit in range(4):
            for rank in range(13):
                card = Card(suit, rank)
                self.cards.append(card)
        self.shuffle()

    def __str__(self):
        """Returns a string representation of the deck."""
        res = []
        for card in self.cards:
            res.append(str(card))
        return ', '.join(res)

    def __len__(self):
        """Overriding len operator"""
        return len(self.cards)

    def add_card(self, card):
        """Adds a card to the deck."""
        self.cards.append(card)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.
        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def pop_high_card(self):
        """Removes and returns the highest card from the deck.
        """
        return self.cards.pop(self.cards.index(max(self.cards)))

    def pop_high_fv_card(self):
        """Removes and returns the highest face value card from the deck.
        """
        curr_rank = -1
        max_index = 0
        for i, c in enumerate(self.cards):
            curr_rank = max(c.rank, curr_rank)
            if curr_rank == c.rank:
                max_index = i
        return self.cards.pop(max_index)

    def pop_optimal_card(self, winner_card):
        """Removes and returns the optimal move card from the deck.
        """
        if winner_card is None:
            return self.pop_high_fv_card()
        else:
            pop_out = None
            pop_out_max = None
            pop_out_min = None
            for c in self.cards:
                if c.suit == Curr_hand:
                    if pop_out_max is None:
                        pop_out_max = c
                    else:
                        pop_out_max = max((c, pop_out_max), default=None)
                    if pop_out_min is None:
                        pop_out_min = c
                    else:
                        pop_out_min = min((c, pop_out_min), default=None)
                    if pop_out_max > winner_card:
                        pop_out = pop_out_max
                    else:
                        pop_out = pop_out_min
            if pop_out is None:
                best_card = max(self.cards, default=None)
                worst_card = min(self.cards, default=None)
                if best_card > winner_card:
                    pop_out = best_card
                else:
                    pop_out = worst_card
            # print(winner_card, Card.suits[Curr_hand], Card.suits[Trump], list(map(Card.__str__, self.cards)), pop_out)
            return self.cards.pop(self.cards.index(pop_out))

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self, *args, **kwargs):
        """Sorts the cards in ascending order."""
        self.cards.sort(*args, **kwargs)

    def wincard(self, cards):
        """Get the highest winner card from list"""
        winner = cards[0]
        for card in cards:
            if winner < card:
                winner = card
        return winner


class Hand(Deck):
    """Represents a hand of playing cards."""

    def __init__(self, label=''):
        super().__init__()
        self.cards = []
        self.label = label
        self.wincount = 0

    def getlabel(self):
        """ Store players name """
        return self.label

    def roundwinner(self):
        """ increasing the win count for player """
        self.wincount += 1

    def getwincount(self):
        """ get the winner count finally """
        return self.wincount

    def __str__(self):
        Deck.sort(self, reverse=True)
        return "Card for " + self.label + " is " + Deck.__str__(self)


class Game:

    @staticmethod
    def play():
        global Trump, Curr_hand
        deck = Deck()  # initialize deck
        hands = []
        for i in range(1, 5):
            player = 'Player %d' % i  # default player name
            hands.append(Hand(player))  # add player

        while len(deck) > 0:
            for hand in hands:
                hand.add_card(deck.pop_card())  # remove card from deck and add to hand

        for i in range(4):
            print(hands[i])

        Trump = random.randrange(4)  # random trump
        trump_suit = Card.suits[Trump]

        print("The Trump suit is: ", trump_suit)

        starting_player = random.randrange(4) + 1  # random starting player
        print("The starting player is: ", 'Player %d' % starting_player)

        input("Lets start playing. Press any key to continue : ")  # wait for keypress

        last_winner_hand = (starting_player - 1) % 4
        for i in range(1, 14):
            cards = []  # collect card in a round
            floors = []  # get string representation for display in each round
            for k in range(4):
                hand_i = (last_winner_hand + k) % 4
                card = hands[hand_i].pop_optimal_card(max(cards, default=None))
                if k == 0:  # starting the round
                    Curr_hand = card.suit
                cards.append(card)  # collect individual card
                floors.append(hands[hand_i].getlabel() + " : " + str(card))  # add string format for individual card

            winner_card = deck.wincard(cards)  # check for winner card
            last_winner = ((last_winner_hand + cards.index(winner_card)) % 4) + 1
            last_winner_hand = (last_winner - 1) % 4
            winner_hand = hands[last_winner_hand]  # find the winner hand from winner card
            winner_hand.roundwinner()  # add score for winner hand
            print("Round", i, ":-", ", ".join(floors), ", Winner :- ", winner_hand.getlabel(), ":", winner_card)

        for hand in hands:  # display the individual hand score after the 13 rounds of play
            print("Score for", hand.getlabel(), "is", hand.getwincount())


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
