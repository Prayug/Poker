from Card import Card, Suit, Value
import random

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Value]
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def reset(self):
        self.__init__()

    def remove(self, card):
        self.cards.remove(card)
    