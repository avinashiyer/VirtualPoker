
from collections import Counter
from copy import deepcopy
from functools import total_ordering
from itertools import product
from random import shuffle
from typing import Iterable, List, Tuple

from card_enums import Hands, Suit, Values


class Card():
    '''
    Essentially a wrapper for Tuple(Value,Suit). Comparison is suit agnostic  
    '''
    __slots__ = ("value", "suit")

    _values = frozenset(Values)
    _suits = frozenset(Suit)

    def __init__(self, value, suit) -> None:
        if value not in Card._values or suit not in Card._suits:
            raise ValueError(f"Value={value}, Suit={suit}")

        self.value = value
        self.suit = suit

    def __repr__(self) -> str:
        return f'Card(Values.{self.value}, Suit.{self.suit})'

    def __str__(self):
        return f'{Values(self.value).name} of {Suit(self.suit).name}S'

    @total_ordering  # type: ignore
    def __lt__(self, other: 'Card') -> bool:
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

    def __init__(self, card=None):
        # list(Suit X Value)
        self.deck = [Card(val, suit) for suit, val in product(Suit, Values)]

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
        for left, right in zip(self.deck, other.deck):
            if left.value != right.value or left.suit != right.suit:
                return False
        return True

    def sort(self, key=None, reverse=False):
        self.deck.sort(key=key, reverse=reverse)

    def shuffle_deck(self):
        '''
        O(|Deck|) shuffle in place
        '''
        shuffle(self.deck)

    def pop(self):
        return self.deck.pop()

    def append(self, card):
        self.deck.append(card)

    def extend(self, cards):
        self.deck.extend(cards)

    def __str__(self) -> str:
        return f'[{", ".join(str(c) for c in self.deck)}]'

    def __repr__(self):
        return f'[{", ".join(repr(c) for c in self.deck)}]'

    if __name__ == '__main__':
        exit()
