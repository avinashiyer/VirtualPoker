
from collections import Counter
from copy import deepcopy
from functools import total_ordering
from itertools import product
from random import shuffle
from typing import Iterable, List, Tuple

from VirtualPoker.card_enums import Hands, Suit, Values


class Card():
    '''
    Essentially a wrapper for Tuple(Value,Suit). Comparison is suit agnostic  
    '''
    __slots__ = ("value", "suit")

    _values = frozenset(Values)
    _suits = frozenset(Suit)

    def __init__(self, value, suit) -> None:
        if value not in Card._values or suit not in Card._suits:
            raise ValueError

        self.value = value
        self.suit = suit

    def __repr__(self) -> str:
        return f'Card(Values.{self.value}, Suit.{self.suit})'

    def __str__(self):
        return f'{Values(self.value).name} of {Suit(self.suit).name}S'

    @total_ordering
    def __lt__(self, other):
        if not isinstance(other, Card):
            raise TypeError()
        return self.value < other.value

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise TypeError()
        return self.value == other.value


class Deck():
    '''
    Models a physical deck, i.e. a bag (cards are choosen without replacement)
    '''
    # list(Suit X Value). Constant list to be cloned by each new deck
    _deck = [Card(val, suit) for suit, val in product(Suit, Values)]

    # Special case due to ace's duality as low|high
    _low_straight = [
        Card(Values.ACE, Suit.SPADE),
        Card(Values.TWO, Suit.DIAMOND),
        Card(Values.THREE, Suit.HEART),
        Card(Values.FOUR, Suit.CLUB),
        Card(Values.FIVE, Suit.SPADE)
    ]
    # Used for testing for royal flush
    _high_straight = [
        Card(Values.TEN, Suit.CLUB),
        Card(Values.JACK, Suit.DIAMOND),
        Card(Values.QUEEN, Suit.SPADE),
        Card(Values.KING, Suit.HEART),
        Card(Values.ACE, Suit.SPADE)
    ]

    def __init__(self):
        self.deck = deepcopy(Deck._deck)
    
    def __iter__(self):
        return self.deck.__iter__()
    
    
    
    def __eq__(self, other):
        '''
        Equality defined as decks same length and same order 
        ''' 
        if not isinstance(other, Deck):
            return NotImplementedError
        if len(self.deck) != len(other.deck):
            return False   
        for left,right in zip(self.deck,other.deck):
            if left.value != right.value or left.suit != right.suit:
                return False
        return True
            
    def sort(self,key=None,reverse=False):
        self.deck.sort(key=key,reverse=reverse)

    def shuffle_deck(self):
        '''
        O(|Deck|) shuffle in place
        '''
        shuffle(self.deck)

    def deal(self, n) -> List[Card]:
        '''
        O(n) Returns n cards popped from back of deck in a list
        '''
        assert isinstance(n, int) and n > 0 and n <= len(self.deck)
        hand = []
        for x in range(n):
            hand.append(self.deck.pop())
        return hand

    def trade_in(self, trade_ins) -> List[Card]:
        '''
        O(|Deck|) Returns trade_ins to deck shuffles then deals |trade_ins| cards back
        '''
        n = len(trade_ins)
        if n == 0:
            return []
        while (trade_ins):
            self.deck.append(trade_ins.pop())
        self.shuffle_deck()
        return self.deal(n)

    

    def __str__(self) -> str:
        return str([str(card) for card in self.deck])
    
    if __name__ == '__main__':
        exit()