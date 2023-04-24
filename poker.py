from enum import IntEnum,auto,Enum
from itertools import product
from random import shuffle, randint


class Suit(Enum):
    SPADE = auto()
    HEART = auto()
    CLUB = auto()
    DIAMOND = auto()


class Values(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Card():
    __slots__ = ("value","suit")
    
    _values = frozenset(Values)
    _suits = frozenset(Suit)
    
    def __init__(self, value, suit) -> None:
        if value not in Card._values or suit not in Card._suits:
            raise ValueError

        self.value = value
        self.suit = suit
    
    def __str__(self):
        return f'{Values(self.value).name} of {Suit(self.suit).name}S'

class Deck():
    
    def __init__(self):
        _deck = list(product(Suit,Values))
        self.deck = [Card(val, suit) for suit,val in _deck]
    
    def shuffle_deck(self):
        shuffle(self.deck)
    
    def deal(self, n):
        assert isinstance(n,int) and n > 0 and n <= len(self.deck)
        hand = []
        for x in range(n):
            hand.append(self.deck.pop())
        return hand
    
    def trade_in(self,trade_ins):
        n = len(trade_ins)
        if n == 0:
            return []
        while(trade_ins):
            self.deck.append(trade_ins.pop())
        self.shuffle_deck()
        return self.deal(n)
    
    @staticmethod
    def search_hand(hand):
        pass
    
    def __str__(self) -> str:
        return str([str(card) for card in self.deck])
    

def main():
    d = Deck()
    

if __name__ == '__main__':
    main()