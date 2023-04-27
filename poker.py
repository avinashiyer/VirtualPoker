from enum import Flag, IntEnum, auto, Enum
from itertools import product
from random import shuffle, randint
from typing import Dict, Iterable, List, Tuple
from functools import total_ordering
from copy import deepcopy


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


'''
    For use in search hand to 
'''


class Hands(Flag):
    PAIR = auto()
    TWO_PAIR = auto()
    THREE_O_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_O_KIND = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_FLUSH = auto()

    '''
    Idempotently disable a flag
    '''

    def disable_flag(self, flag):
        return self & ~flag

    '''
    Use to eliminate FLUSH, STRAIGHT FLUSH, ROYAL FLUSH
    '''

    def no_flush(self):
        self.disable_flag(Hands.FLUSH)
        self.disable_flag(Hands.STRAIGHT_FLUSH)
        self.disable_flag(Hands.ROYAL_FLUSH)

    '''
    Use to eliminate straights
    '''

    def no_straight(self):
        self.disable_flag(Hands.STRAIGHT)
        self.disable_flag(Hands.STRAIGHT_FLUSH)
        self.disable_flag(Hands.ROYAL_FLUSH)

    @classmethod
    def get_multis(cls):
        multis = {
            cls.TWO_PAIR: 2,
            cls.THREE_O_KIND: 3,
            cls.STRAIGHT: 4,
            cls.FLUSH: 6,
            cls.FULL_HOUSE: 9,
            cls.FOUR_O_KIND: 25,
            cls.STRAIGHT_FLUSH: 50,
            cls.ROYAL_FLUSH: 250
        }
        return multis


class Card():
    __slots__ = ("value", "suit")

    _values = frozenset(Values)
    _suits = frozenset(Suit)

    def __init__(self, value, suit) -> None:
        if value not in Card._values or suit not in Card._suits:
            raise ValueError

        self.value = value
        self.suit = suit

    def __repr__(self) -> str:
        return f'Card(Values.{self.value}, {self.suit})'

    def __str__(self):
        return f'{Values(self.value).name} of {Suit(self.suit).name}S'

    @total_ordering
    def __lt__(self, other):
        if not isinstance(other, Card):
            raise NotImplementedError()
        return self.value < other.value

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise NotImplementedError()
        return self.value == other.value


class Deck():
    # list(Suit X Value). Constant list to be cloned by each new deck
    _deck = [Card(val, suit) for suit, val in product(Suit, Values)]

    def __init__(self):
        self.deck = deepcopy(Deck._deck)

    def shuffle_deck(self):
        'O(|Deck|) shuffle in place'
        shuffle(self.deck)

    def deal(self, n) -> List[Card]:
        'O(n) Returns n cards popped from back of deck in a list'
        assert isinstance(n, int) and n > 0 and n <= len(self.deck)
        hand = []
        for x in range(n):
            hand.append(self.deck.pop())
        return hand

    def trade_in(self, trade_ins) -> List[Card]:
        'O(|Deck|) Returns trade_ins to deck shuffles then deals |trade_ins| cards back'
        n = len(trade_ins)
        if n == 0:
            return []
        while (trade_ins):
            self.deck.append(trade_ins.pop())
        self.shuffle_deck()
        return self.deal(n)

    @staticmethod
    def pairs_search(hand: Iterable[Card], pairs: Dict[Values:int]):
        assert len(hand) == 5
        keys = pairs.keys()
        # pairs' max length is two, assuming five card limit in hand
        if len(pairs) == 1:
            relavant = [crd for crd in hand if crd.value == keys[0]]
            if len(relavant) == 4:
                return (Hands.FOUR_O_KIND, relavant)
            elif len(relavant) == 3:
                return (Hands.THREE_O_KIND, relavant)
        elif len(pairs) == 2:
            big_un = max(pairs.values())
            if big_un == 3:
                return (Hands.FULL_HOUSE, hand)
            else:
                relavant = [crd for crd in hand if crd.value in keys]
                return (Hands.TWO_PAIR, relavant)
        else:
            return None

    @staticmethod
    def search_hand(hand: Iterable[Card]) -> Tuple(Hands, Iterable[Card]):
        assert len(hand) == 5
        # Start with all flags set to 1
        flags = Hands(-1)
        sHand = sorted(hand)
        pairs = dict()
        # Main loop
        idx = 0
        while (idx < 4):
            cur = sHand[idx]
            nxt = sHand[idx + 1]
            if nxt.value == cur.value:
                try:
                    pairs[cur.value] += 1
                except KeyError:
                    pairs[cur.value] = 2
            elif nxt.value != cur.value + 1:
                if nxt.value == Values.ACE and cur.value == Values.FIVE and Hands.STRAIGHT in flags:
                    # Handle special case of [2,3,4,5,A]
                    pass
                else:
                    flags.no_straight()

            if cur.suit != nxt.suit:
                flags.no_flush()
            idx += 1
        # Correct special case: [A,2,3,4,5]

        if Hands.STRAIGHT_FLUSH in flags:
            if sHand[0].value == Values.JACK:
                return (Hands.ROYAL_FLUSH, sHand)
            else:
                return (Hands.STRAIGHT_FLUSH, sHand)
        elif Hands.STRAIGHT in flags:
            return (Hands.STRAIGHT, sHand)
        elif Hands.FLUSH in flags:
            return (Hands.FLUSH, sHand)
        
        
        res = Deck.pairs_search(pairs, hand)
        return res

    def __str__(self) -> str:
        return str([str(card) for card in self.deck])


def main():
    h = [Card(Values.EIGHT, Suit.DIAMOND),
         Card(Values.ACE, Suit.CLUB),
         Card(Values.NINE, Suit.HEART),
         Card(Values.TWO, Suit.HEART),
         Card(Values.EIGHT, Suit.CLUB)]
    print((sorted(h)))


if __name__ == '__main__':
    main()
